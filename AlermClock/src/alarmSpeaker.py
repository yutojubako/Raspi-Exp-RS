"""
alarmspeaker.py

summary:Alarm speaker
"""
import wave
import pyaudio
import threading
from sensor import Sensor,ReceiveThread

threshold=1.4

class AlarmSpeaker:
    #alarmspeaker
    
    th = ReceiveThread()
    th.setDaemon(True)
    th.start()
    
    def __init__(self):
        #constructor
        self.__isRunnning=False
        self.__speakerThreadObj=None
        self.__CheckPressureThreadOBj=None
        
        
    def __del__(self):
        #Destructor
        self.stopThread()
    
    def goOff(self):
        self.stopThread()
        self.startThread()
    
    def startThread(self):
        """
        Start SpeakerThread and CheckPressureThread
        """
        self.__isRunning=True
        if self.__speakerThreadObj is None:
            self.__speakerThreadObj = threading.Thread(target=self.__speakerThread)
            self.__speakerThreadObj.start()
            
        if self.__checkPressureThreadObj is None:
            self.__checkPressureThreadObj = threading.Thread(target=self.__checkPressureThread)
            self.__checkPressureThreadObj.start()
    
    def stopThread(self):
        """
        Stop SpeakerThread and CheckPressureThread
        """
        
        self.__isRunning=False
        if self.__speakerThreadObj is not None:
            self.__speakerThreadObj.join()
            self.__speakerThreadObj = None
            
        if self.__checkPressureThreadObj is None:
            self.__checkPressureThreadObj.join()
            self.__checkPressureThreadObj = None


    def __checkPressureThreadObj(self):
        
        while self.__isRunning:
            sensor = Sensor()
            data1 = sensor.th.get_data()
            data2 = self.th.get_data()
            if data1[2]>1.4 or data2[2]>1.4:
                self.__isRunning = False
                del self
            
            
    def __speakerThread(self):
        """
        continue to sound music until stopped status
        """
        #sound path
        sound="/home/pi/exp66/AlermClock/sounds/alarmsound.wav"
    
        
        while self.__isRunning:
            wf = wave.open(sound,"r")
            audio = pyaudio.PyAudio()
            stream = audio.open(format=pyaudio.paInt16,
                                channels=wf.getnchannels(),
                                rate=wf.getframerate(),
                                output=True)
            
            data = wf.readframes(1024)
            
            while data != b'' and self.__isRunning:
                stream.write(data)
                data=wf.readframes(1024)
                
            stream.stop_stream()
            
            stream.close()
            audio.terminate()
            wf.close()