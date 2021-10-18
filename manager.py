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

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

print(bcolors.WARNING + "Warning: No active frommets remain. Continue?" + bcolors.ENDC)
print(bcolors.HEADER + "Warning: No active frommets remain. Continue?" + bcolors.ENDC)
print(bcolors.OKBLUE + "Warning: No active frommets remain. Continue?" + bcolors.ENDC)
print(bcolors.OKCYAN + "Warning: No active frommets remain. Continue?" + bcolors.ENDC)
print(bcolors.OKGREEN + "Warning: No active frommets remain. Continue?" + bcolors.ENDC)
print(bcolors.FAIL + "Warning: No active frommets remain. Continue?" + bcolors.ENDC)

