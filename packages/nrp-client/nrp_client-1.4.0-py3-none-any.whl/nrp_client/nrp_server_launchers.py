import os
import signal
import psutil


from abc import ABC, abstractmethod

class NRPCoreServerLauncher(ABC):

    @abstractmethod
    def is_alive_nrp_process(self) -> bool:
        raise NotImplementedError

    @abstractmethod
    def kill_nrp_process(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def get_exit_report(self) -> dict:
        raise NotImplementedError


class NRPCoreForkLauncher(NRPCoreServerLauncher):

    def __init__(self, args, experiment_folder):
        self.child_pid = os.fork()
        is_child = (self.child_pid == 0)

        # Server side
        if is_child:
            launch_command = ["NRPCoreSim", *args, "--slave"]
            if experiment_folder:
                launch_command += ["-d", experiment_folder]
            os.execvp("NRPCoreSim", launch_command)

    def is_alive_nrp_process(self) -> bool:
        try:
            p = psutil.Process(self.child_pid)
            if p.status() == "zombie":
                return False
        except psutil.NoSuchProcess:
            return False

        return True

    def kill_nrp_process(self) -> None:
        """Sends SIGTERM signal to the NRP Core subprocess"""
        try:
            os.kill(self.child_pid, signal.SIGTERM)
        except ProcessLookupError:
            pass

        # Server is closed now
        try:
            os.waitpid(self.child_pid, 0)
        except ChildProcessError:
            pass

    def get_exit_report(self) -> dict:
        # TODO: implement
        return {'exit_code': None, 'logs': []}
