class DataIncompatabilityError(Exception):
    pass
class Stopwatch:
    """
    Creates a stopwatch object
    """
    def __init__(self,starttime=0.000):
        """
        Creates a stopwatch whose starting value is the given time.
        """
        try:
            starttime = float(starttime)
        except:
            raise DataIncompatabilityError(f"Expected starttime to be possible to convert to float but recieved input '{starttime}', type '" + "".join(list(str(type('hello')))[8:-2])+"'")
        import time
        self.__timeModule = time
        self.__time = starttime
        self.playing = False
        self.__start = None
        self.__started = False
        self.__ontime = 0
    def set(self,value):
        """
        Sets the stopwatch's time to the given value.
        """
        try:
            value = float(value)
        except:
            msg = f"Expected input to be possible to convert to float but recieved input '{value}', type '" + "".join(list(str(type('hello')))[8:-2])+"'"
            raise DataIncompatabilityError(msg)
        if len(str(self.__time).split('.')[1]) == 3:
            return
        elif len(str(self.__time).split('.')[1]) > 3:
            self.__time = round(self.__time,3)
        else:
            self.__time = str(self.__time)
            while not len(str(self.__time).split('.')[1]) == 3:
                self.__time = self.__time + "0"
            self.__time = float(self.__time)
    def __backhandUpdateTime(self):
        self.__ontime += self.__timeModule.time() - self.__start
        self.__start = self.__timeModule.time()
        self.__time = self.__ontime
    def start(self):
        """
        Starts the stopwatch.
        """
        self.playing = True
        self.__started = True
        if self.__start == None:
            self.__start = self.__timeModule.time()
            
    def pause(self):
        """
        Pauses the stopwatch
        """
        self.playing = False
        self.__backhandUpdateTime()
    def gettime(self):
        """
        Returns the current time of the stopwatch.
        """
        self.__backhandUpdateTime()
        return self.__time

