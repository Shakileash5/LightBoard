import datetime
import utils

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
    DEBUG = True #False
    PADDING = 9
    _INSTANCE = None

    def __init__(self):
        pass

    def info(self,message,data=None,roomId=None):
        time = datetime.datetime.utcnow().strftime("%a %b %d %H:%M:%S %Z %Y")
        level = "info"#bcolors.OKBLUE+"info".ljust(Logger.PADDING)+bcolors.ENDC
        #print(level+"fea")
        if data == None:
            if roomId:
                print("Room - {}|{}|{}|{}".format(roomId,time,level,message))    
            else:
                print("{}|{}|{}".format(time,level,message))
        else:
            if roomId:
                print("Room - {}|{}|{}|{}|data: ".format(roomId,time,level,message,str(data)))
            else:
                print("{}|{}|{}|data: ".format(time,level,message,str(data)))

    def warning(self,message,data=None,roomId=None):
        time = datetime.datetime.utcnow().strftime("%a %b %d %H:%M:%S %Z %Y")
        level = "warning"#bcolors.WARNING+"warning".ljust(Logger.PADDING)+bcolors.ENDC
        if data == None:
            if roomId:
                print("Room - {}|{}|{}|{}".format(roomId,time,level,message))    
            else:
                print("{}|{}|{}".format(time,level,message))
        else:
            if roomId:
                print("Room - {}|{}|{}|{}|data: ".format(roomId,time,level,message,str(data)))
            else:
                print("{}|{}|{}|data: ".format(time,level,message,str(data)))
    
    def error(self,message,data=None,roomId=None):
        time = datetime.datetime.utcnow().strftime("%a %b %d %H:%M:%S %Z %Y")
        level = "error"#bcolors.FAIL+"error".ljust(Logger.PADDING)+bcolors.ENDC
        if data == None:
            if roomId:
                print("Room - {}|{}|{}|{}".format(roomId,time,level,message))    
            else:
                print("{}|{}|{}".format(time,level,message))
        else:
            if roomId:
                print("Room - {}|{}|{}|{}|data: ".format(roomId,time,level,message,str(data)))
            else:
                print("{}|{}|{}|data: ".format(time,level,message,str(data)))
    
    def debug(self,message,data=None,roomId=None):
        if Logger.DEBUG:
            time = datetime.datetime.utcnow().strftime("%a %b %d %H:%M:%S %Z %Y")
            level = "debug"#bcolors.OKCYAN+"debug".ljust(Logger.PADDING)+bcolors.ENDC
            if data == None:
                if roomId:
                    print("Room - {}|{}|{}|{}".format(roomId,time,level,message))    
                else:
                    print("{}|{}|{}".format(time,level,message))
            else:
                if roomId:
                    print("Room - {}|{}|{}|{}|data: ".format(roomId,time,level,message,str(data)))
                else:
                    print("{}|{}|{}|data: ".format(time,level,message,str(data)))
    
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

def a():
    Logger.getInstance().info("test")
    Logger.getInstance().warning("test")
    Logger.getInstance().error("test")
    Logger.getInstance().debug("test")

if __name__ == "__main__":
    logger = Logger.getInstance()
    logger.info("test")
    logger.warning("test")
    logger.error("test")
    logger.debug("test")
    a()