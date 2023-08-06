from pkg_resources import get_distribution, DistributionNotFound
try:
    __version__ = get_distribution(__name__).version
except DistributionNotFound:
    # package is not installed
    pass

import grpc
import os
from contextlib import redirect_stdout
from threading import Thread
import json

from google.protobuf.message_factory import MessageFactory
from google.protobuf import descriptor_pool

try:
    from nrp_protobuf.nrp_server_pb2 import ResetMessage, EmptyMessage, RunLoopMessage, JsonMessage
    from nrp_protobuf.nrp_server_pb2_grpc import NrpCoreStub
except ImportError as e:
    raise ImportError(
        'NRP-Core protobuf Python bindings for client-server communication could not be found.') from e

from nrp_protobuf.engine_grpc_pb2 import DataPackMessage
from nrp_protobuf.proto_modules import proto_modules as nrp_proto_modules

from importlib import import_module

from .nrp_server_launchers import *

_dockerEnabled = True
try:
    from .nrp_server_docker_launchers import *
except ImportError:
    _dockerEnabled = False


class NrpCore:

    def __init__(self, address, experiment_folder="", config_file="simulation_config.json", args="",
                 log_output=".console_output.log", server_timeout=10, docker_daemon_address="unix:///var/run/docker.sock", image_name="",
                 get_archives=[], compose_file="") -> None:
        """
        Spawns an NRPCoreSim process in server mode and connects to it

        :param str address: the address that will be used by NRPCoreSim server
        :param str experiment_folder: path to the folder containing all files needed to execute the experiment.
                                        By default, is an empty string, which is interpreted as the current folder.
        :param str config_file: path to the experiment configuration file. It can be an absolute path or
                                relative to `experiment_folder`.
                                By default, "simulation_config.json"
        :param str args: additional NRPCoreSim command line parameters
        :param str log_output: if not empty, console output from NRPCoreSim process will be logged into a file
                                with the given name, relative to the experiment directory
        :param int server_timeout: time in seconds for waiting for connection with the NRPCoreSim grpc server.
                                    10 seconds by default.
        :param str docker_daemon_address: IP address of the docker daemon used
                                            to launch the experiment in a docker container (more detail below).
                                            'unix:///var/run/docker.sock' by default.
        :param str image_name: name of the docker image which will be used to run the experiment (more detail below).
                                Empty by default.

        :param list get_archives: list of archives (files or folders) that should be retrieved from the docker container
                                when shutting down the simulation (e.g. folder containing logged simulation data)
        :param compose_file: List[Union[str, pathlib.Path]]: Docker compose yaml file for Compose Launcher
        """
        self._json_datapack_out_buffer = []
        self._proto_datapack_out_buffer = []

        self._init_protobuf_classes()

        self._devnull = open(os.devnull, 'w')
        self._server_timeout = server_timeout

        # Initialize variables in case NRPServer launching fails
        self._sim_state = "None"
        self._is_open = False
        self._channel = None
        self._stub = None

        # Spawn NRP Core server process with chosen launcher
        server_args = ["-c", config_file, "-m", "server", "--server_address", address]
        if args:
            server_args += args.split(" ")
        if log_output:
            server_args += ["--logoutput=all", f"--logfilename={log_output}"]

        self._launcher = None

        if image_name:
            self._launcher = NRPCoreDockerLauncher(server_args,
                                                   experiment_folder,
                                                   docker_daemon_address,
                                                   image_name,
                                                   log_output,
                                                   get_archives)
        elif compose_file:
            self._launcher = NRPCoreComposeLauncher(compose_file,
                                                    log_output,
                                                    get_archives,
                                                    address=address)
        else:
            self._launcher = NRPCoreForkLauncher(server_args, experiment_folder)

        # Connect to server
        self._channel = grpc.insecure_channel(address)
        self._stub = NrpCoreStub(self._channel)

        # Wait for the server to start
        n = self._wait_until_server_ready(self._channel, self._launcher.is_alive_nrp_process)
        if n > self._server_timeout:

            with redirect_stdout(self._devnull):
                report = self._launcher.get_exit_report()

            if report['exit_code'] or report['logs']:
                # print report
                msg = f"NRP Process has exit with code: {report['exit_code']}.\n"
                msg += "Logs from process:\n"
                if type(report['logs']==str):
                    msg += f"{report['logs']}\n"
                else:
                    for l in report['logs']:
                        msg += f"{l}\n"

                print(msg)

            self._launcher.kill_nrp_process()

            if n >= self._server_timeout:
                raise TimeoutError("Timeout while connecting to NRP Server.")
            else:
                raise ChildProcessError("Error during NRP Server startup.")

        # Set simulation state
        self._sim_state = "Created"
        self._is_open = True


    def _init_protobuf_classes(self) -> None:
        # Import all proto modules that are on the proto_modules list generated by CMake

        self.proto_modules = []
        for module_name in nrp_proto_modules:
            module = import_module(module_name)
            self.proto_modules.append(module.DESCRIPTOR.name)

        # Create a protobuf message factory. It is able to dynamically
        # generate protobuf messages based on the provided pool of protobuf file descriptors
        # The default descriptor pool should contain all imported protobuf files and,
        # by extension, all necessary definitions of protobuf messages

        message_factory = MessageFactory(descriptor_pool.Default())

        # Retrieve all proto message classes available in our proto files
        self.proto_message_classes = message_factory.GetMessages(self.proto_modules)

    def __del__(self) -> None:
        """Deletes the NRP Core objects and kills the server"""
        try:
            with redirect_stdout(self._devnull):
                self.shutdown()
                self._close_client()
        except Exception:
            # it's ok, we are shutting down
            pass

        self._devnull.close()


    def _close_client(self):

        if self._channel:
            self._channel.close()
            self._channel = None
            self._is_open = False

        print("NRP Server is closed now. This object can be deleted.")

    def _wait_until_server_ready(self, channel, is_server_alive) -> int:
        """Waits for the gRPC server of the NRP Core process to start"""
        n = 1
        while n <= self._server_timeout:
            if not is_server_alive():
                return n

            try:
                grpc.channel_ready_future(channel).result(timeout=1)
                return n
            except grpc.FutureTimeoutError:
                if n > 5:
                    print(f"Waiting for NRP Server connection: {n} out of {self._server_timeout} seconds")

            n += 1

        return n

    def _call_rpc_async(self, sim_rpc, message, response) -> Thread:
        t = Thread(target=self._call_rpc, args=(sim_rpc, message, response))
        t.start()
        return t

    def unpack_thread_results(self, response):
        return response.doneFlag, self._read_trajectory(response.trajectory)


    def _call_rpc(self, sim_rpc, message, thread_response = None):
        """Processes calls to RPCs of the NRP Core Server"""
        if not self._is_open:
            raise ChildProcessError("This NRP Server is closed. Please delete this object and create a new one")

        try:
            response = sim_rpc(message)

            # Extract the state message from the RPC response
            self._sim_state = response.simState.currentState

            if self._sim_state == "Failed":
                raise RuntimeError(f"Request failed with error \"{response.simState.errorMsg}\". The only possible action now is \"shutdown()\".")

        except grpc.RpcError as rpc_error:
            if rpc_error.code() == grpc.StatusCode.CANCELLED:
                raise ConnectionError(f"Can't process request") from rpc_error
            elif rpc_error.code() == grpc.StatusCode.UNAVAILABLE:
                raise ConnectionError(f"NRP Server is unavailable") from rpc_error
            else:
                # TODO: depending on the error, maybe the server process should be killed?
                raise
        except ValueError as e:
            raise ConnectionError("Channel has been closed already") from e

        if thread_response is not None:
            thread_response.append(response)
        else:
            return response


    def current_state(self):
        return self._sim_state

    def initialize(self):
        """Calls the initialize() RPC of the NRP Core Server"""
        response = self._call_rpc(self._stub.initialize, EmptyMessage())

        return self._read_trajectory(response.trajectory)


    def _clear_datapack_out_buffers(self):
        self._json_datapack_out_buffer = []
        self._proto_datapack_out_buffer = []


    def _read_trajectory(self, response) -> list:
        trajectory_data = []
        total_messages = len(response.jsonTrajectoryMessages) + len(response.protoTrajectoryMessages)
        json_message_index = 0
        proto_message_index = 0

        # Assemble proto and json messages into a single trajectory list

        for i in range(total_messages):
            if json_message_index < len(response.jsonTrajectoryMessages) and \
               response.jsonTrajectoryMessages[json_message_index].dataIndex == i:

                # Unpack the content of Any field into a proper protobuf message
                proto_message = JsonMessage()
                response.jsonTrajectoryMessages[json_message_index].data.Unpack(proto_message)

                # Parse the JSON string of the message
                json_object = json.loads(proto_message.data)

                # Append the new JSON object into the trajectory
                trajectory_data.append(json_object)

                json_message_index += 1
            else:
                # Extract the class that matched the trajectory message type and instantiate it
                proto_message = self.proto_message_classes[response.protoTrajectoryMessages[proto_message_index].data.TypeName()]()

                # Unpack the content of Any field into the message created above
                response.protoTrajectoryMessages[proto_message_index].data.Unpack(proto_message)

                # Append the new proto object to the trajectory
                trajectory_data.append(proto_message)

                proto_message_index += 1

        return trajectory_data


    def run_loop(self, num_iterations, run_async=False, response=None):
        """
        Calls the runLoop() RPC of the NRP Core Server

        param int num_iterations: Number of simulation iterations to execute
        param bool run_async: Flag that makes the call to be executed asynchronously. When True, the method
                              will return a Thread object, and the execution results (done flag, observations)
                              will be put in the response parameter.
        param List response: Mutable variable to hold results of the call in asynchronous mode. Assumed to be an empty list.
        """

        # Prepare the message for the RPC
        message = RunLoopMessage()
        message.numIterations = num_iterations
        message.dataPacks.jsonDataPacks.extend(self._json_datapack_out_buffer)
        message.dataPacks.protoDataPacks.extend(self._proto_datapack_out_buffer)

        # Clean the user's message buffer, all messages should be copied to the RPC message
        self._clear_datapack_out_buffers()

        if run_async:
            return self._call_rpc_async(self._stub.runLoop, message, response)
        else:
            response = self._call_rpc(self._stub.runLoop, message)
            return response.doneFlag, self._read_trajectory(response.trajectory)


    def run_until_timeout(self, run_async=False, response=None):
        """
        Calls the runUntilTimeout() RPC of the NRP Core Server

        param bool run_async: Flag that makes the call to be executed asynchronously. When True, the method
                              will return a Thread object, and the execution results (done flag, observations)
                              will be put in the response parameter.
        param List response: Mutable variable to hold results of the call in asynchronous mode. Assumed to be an empty list.
        """
        if run_async:
            return self._call_rpc_async(self._stub.runUntilTimeout, EmptyMessage(), response)
        else:
            response = self._call_rpc(self._stub.runUntilTimeout, EmptyMessage())
            return response.doneFlag, response.timeoutFlag, self._read_trajectory(response.trajectory)

    def stop(self):
        """Calls the stopLoop() RPC of the NRP Core Server"""
        self._call_rpc(self._stub.stopLoop, EmptyMessage())

    def reset(self):
        """Calls the reset() RPC of the NRP Core Server"""

        # Prepare the message for the RPC
        message = ResetMessage()
        message.dataPacks.jsonDataPacks.extend(self._json_datapack_out_buffer)
        message.dataPacks.protoDataPacks.extend(self._proto_datapack_out_buffer)

        # Clean the user's message buffer, all messages should be copied to the RPC message
        self._clear_datapack_out_buffers()

        response = self._call_rpc(self._stub.reset, message)

        return self._read_trajectory(response.trajectory)

    def shutdown(self):
        """Calls the shutdown() RPC of the NRP Core Server"""
        with redirect_stdout(self._devnull):
            if self._stub:
                self._call_rpc(self._stub.shutdown, EmptyMessage())

        if self._launcher:
            self._launcher.kill_nrp_process()


    def set_proto_datapack(self, datapack_name: str, engine_name: str, payload) -> None:
        """
        Prepares a DataPack that will be sent to NRP Core (and later to an engine)
        on the next call to run_loop().

        :param str datapack_name: Name of the DataPack
        :param str engine_name: Name of the engine to which the DataPack will be passed
        :param protobuf.Any payload: Payload of the DataPack, a protobuf message
        """
        # Prepare a proto DataPack object
        datapack = DataPackMessage()
        datapack.dataPackId.dataPackName = datapack_name
        datapack.dataPackId.engineName = engine_name
        datapack.data.Pack(payload)

        # Save the DataPack in the buffer
        self._proto_datapack_out_buffer.append(datapack)


    def set_json_datapack(self, datapack_name: str, engine_name: str, payload: dict) -> None:
        """
        Prepares a DataPack that will be sent to NRP Core (and later to an engine)
        on the next call to run_loop().

        :param str datapack_name: Name of the DataPack
        :param str engine_name: Name of the engine to which the DataPack will be passed
        :param dict payload: Payload of the DataPack, a JSON-serializable python dictionary
        """
        # Create a proto object with the payload serialized as a JSON string
        proto_json = JsonMessage()
        proto_json.data = json.dumps(payload)

        # Prepare a JSON DataPack object
        datapack = DataPackMessage()
        datapack.dataPackId.dataPackName = datapack_name
        datapack.dataPackId.engineName = engine_name
        datapack.data.Pack(proto_json)

        # Save the DataPack in the buffer
        self._json_datapack_out_buffer.append(datapack)

# EOF
