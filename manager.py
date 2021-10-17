import multiprocessing
import threading

class Manager:
    _instance = None
    _lock = threading.Lock()
    _isRunning = False
    _pipe = None

    @staticmethod
    def get_instance(serverRoom, portList):
        """
        Static access method.
        """
        if Manager._instance == None:
            Manager(serverRoom, portList)
        return Manager._instance

    def __init__(self, serverRoom, portList):
        """
        This class is a singleton.
        """
        if Manager._instance != None:
            raise Exception("This class is a singleton!")
        else:
            Manager._instance = self
            self.rooms = serverRoom
            self.portList = portList
