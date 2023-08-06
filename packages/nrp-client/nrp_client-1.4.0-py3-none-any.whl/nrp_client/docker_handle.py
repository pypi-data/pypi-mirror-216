import docker
import os
import tarfile
from io import BytesIO
import socket
from typing import Optional


def container_put_archive(container: docker.models.containers.Container,
                          archive_path: str, container_path: str) -> (bool, str):
    """Put archive in container from host filesystem

    :param container: docker container where the archive will be put
    :param archive_path archive path in the host filesystem
    :param container_path path in the container where the archive will be extracted
    :returns a bool indicating whether the operation succeed or not and an error msg if it didn't
    """

    # tar folder
    if not os.path.exists(archive_path):
        return False, f"Path {archive_path} could not be found in host"

    tar_fileobj = BytesIO()
    with tarfile.open(fileobj=tar_fileobj, mode="w|gz") as tar:
        tar.add(archive_path, arcname=os.path.basename(archive_path))

    tar_fileobj.seek(0)
    tar_data = tar_fileobj.read()

    # put in container
    try:
        container.put_archive(container_path, tar_data)
    except docker.errors.NotFound:
        return False, f"Path {container_path} could not be found in container"

    return True, ""


def container_get_archive(container: docker.models.containers.Container,
                          archive_path: str, host_path: str) -> (bool, str):
    """Get archive from a container and extract it in the host filesystem

   :param container: docker container containing the archive to be retrieved
   :param archive_path archive path in the container
   :param host_path path in the host filesystem where the archive will be extracted
   :returns a bool indicating whether the operation succeed or not and an error msg if it didn't
   """

    if not os.path.exists(host_path):
        return False, f"Path {host_path} could not be found in host"

    try:
        stream, stat = container.get_archive(archive_path, encode_stream=True)
        file_obj = BytesIO()
        for i in stream:
            file_obj.write(i)
        file_obj.seek(0)

        with tarfile.open(fileobj=file_obj, mode='r') as tar:
            tar.extractall(host_path)
    except docker.errors.NotFound:
        return False, f"Path {archive_path} could not be found in container"

    return True, ""


class NRPDockerHandle(object):
    """
    This class runs an NRPCore process (NRPCoreSim or Engine process) in a docker container. It provides methods
    for monitoring the process status or stopping it. The container will always be stopped and removed after the
    related NRPDockerHandle object is deleted.

    Args:
        docker_daemon_ip: IP of the docker daemon which will create and run the container
        image_name: name of the docker image from which the container will be created
        experiment_folder: path to the folder containing the necessary files to run the NRPCore process. It will be
            put in the container and set as work directory when running the NRPCore process.
        proc_cmd: command used to run in the NRPCore process
        exec_env: list of strings containing environment variables to be used for running the NRPCore process
    """

    # Home folder inside of the docker container. In NRP containers this is '/home/nrpuser'
    DOCKER_HOME = '/home/nrpuser'

    def __init__(self, docker_daemon_ip: str, image_name: str, experiment_folder: str, proc_cmd: str, exec_env: list):

        super(NRPDockerHandle, self).__init__()

        # Initialize members
        self._container = None
        self._exec_id = ""

        # Connect to docker daemon
        try:
            self._client = docker.client.DockerClient(base_url=docker_daemon_ip)
        except docker.errors.DockerException:
            raise ValueError(f'It was not possible to connect to docker daemon at IP: {docker_daemon_ip}. Please '
                             'ensure that the address is correct and your docker daemon is running and correctly '
                             'configured.')
        except socket.gaierror:
            raise ValueError('It was not possible to connect to docker daemon. '
                             f'Docker daemon ip: {docker_daemon_ip} is malformed.')

        # If experiment_folder == "", use current folder
        # Also handle "." since we'll need the folder name afterwards
        if experiment_folder in ["", "."]:
            experiment_folder = os.getcwd()

        if not os.path.isdir(experiment_folder):
            raise ValueError(f"The specified path to experiment folder: {experiment_folder}, "
                             "does not exist or is not a directory")

        self._experiment_folder = experiment_folder
        self._work_dir = os.path.join(self.DOCKER_HOME, os.path.basename(experiment_folder))

        # Create container and run proc_cmd inside
        self._run(image_name, proc_cmd, exec_env)

    def __del__(self):
        self.stop()
        self.remove()

    def _run(self, image_name: str, proc_cmd: str, exec_env: str) -> None:
        """ Creates the container and runs proc_cmd inside.
        :param image_name: name of the docker image from which the container will be created
        :param proc_cmd: command used to run in the container
        :param exec_env: list of strings containing environment variables to be used for executing the command """

        # Start a container from the specified image
        try:
            container = self._client.containers.run(
                image=image_name,
                tty=True,
                detach=True,
                network_mode="host"
            )
        except docker.errors.ImageNotFound:
            raise ValueError(f"The specified docker image {image_name} could not be found.")

        if not container:
            raise RuntimeError("Failed to create docker container due to an unknown cause")

        # Name container and put experiment folder in container
        container_name = 'nrp_' + container.id[:12]
        container.rename(container_name)
        ok, msg = container_put_archive(container, self._experiment_folder, self.DOCKER_HOME)
        if not ok:
            raise RuntimeError(msg)

        # Run proc_cmd in container
        resp = self._client.api.exec_create(
            container.id, proc_cmd,
            tty=True,
            environment=exec_env,
            workdir=self._work_dir,
        )

        self._exec_id = resp['Id']

        self._logs = self._client.api.exec_start(
            resp['Id'], tty=True, stream=True
        )

        # It is needed to fetch again the container object after exec_run, the former object seems to get
        # invalidated
        self._container = self._client.containers.get(container_name)

    def stop(self) -> bool:
        """ Stop container """

        if self._container:
            self._container.stop()
            self._container.wait()
            return True
        else:
            return False

    def remove(self) -> None:
        """ Remove container """

        if self._container:
            self._container.remove()
            self._container = None
            self._exec_id = ""

    def get_experiment_archive(self, archive_name: str) -> bool:
        """ Get an archive (file or folder) from the experiment folder in the container and place it in the experiment
            folder in the host

            :param archive_name: name of the archive to be fetched"""

        res = False
        if self._container:
            res, msg = container_get_archive(self._container, os.path.join(self._work_dir, archive_name),
                                             self._experiment_folder)
            if not res:
                print(f'experiment archive: {archive_name} could not be retrieved from container: {msg}')

        return res

    def get_status(self) -> Optional[dict]:
        """ Returns the status of the process running in the container """

        try:
            proc_status = self._client.api.exec_inspect(self._exec_id)
            return {'running': proc_status['Running'], 'exit_code': proc_status['ExitCode']}
        except docker.errors.NotFound:
            pass

        return None

    def get_logs(self) -> list:
        """ Return the container logs """

        logs = []
        status = self.get_status()
        if status and status['running']:
            print('The NRP process is still running. Logs can only be fetched after the process ends')
            return logs

        if self._logs:
            logs.extend(self._logs)

        return logs

    def get_container_id(self) -> str:
        """ Returns the container id """

        if not self._container:
            return ""
        else:
            return self._container.id
