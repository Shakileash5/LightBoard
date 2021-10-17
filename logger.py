import datetime

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


class Logger:
    DEBUG = False
    PADDING = 9
    _INSTANCE = None

    def __init__(self):
        pass

    def info(self,message):
        time = datetime.datetime.utcnow().strftime("%a %b %d %H:%M:%S %Z %Y")
        level = bcolors.OKBLUE+"info".ljust(Logger.PADDING)+bcolors.ENDC
        print(level+"fea")
        print("{}|{}|{}".format(time,level,message))

    def warning(self,message):
        time = datetime.datetime.utcnow().strftime("%a %b %d %H:%M:%S %Z %Y")
        level = bcolors.WARNING+"warning".ljust(Logger.PADDING)+bcolors.ENDC
        print("{}|{}|{}".format(time,level,message))
    
    def error(self,message):
        time = datetime.datetime.utcnow().strftime("%a %b %d %H:%M:%S %Z %Y")
        level = bcolors.FAIL+"error".ljust(Logger.PADDING)+bcolors.ENDC
        print("{}|{}|{}".format(time,level,message))
    
    def debug(self,message):
        if Logger.DEBUG:
            time = datetime.datetime.utcnow().strftime("%a %b %d %H:%M:%S %Z %Y")
            level = bcolors.OKCYAN+"debug".ljust(Logger.PADDING)+bcolors.ENDC
            print("{}|{}|{}".format(time,level,message))
    
    @staticmethod
    def getInstance():
        if Logger._INSTANCE is None:
            Logger._INSTANCE = Logger()
        return Logger._INSTANCE
    
    @staticmethod
    def setDebug(debug):
        Logger.DEBUG = debug
    
    @staticmethod
    def getDebug():
        return Logger.DEBUG
    
    @staticmethod
    def setPadding(padding):
        Logger.PADDING = padding
    
if __name__ == "__main__":
    logger = Logger.getInstance()
    logger.info("test")
    logger.warning("test")
    logger.error("test")
    logger.debug("test")