# -*- coding: utf-8 -*-
"""
Created on Sat Jun 11 17:12:56 2022

@author: pazud
"""

""" alarmSetting.py
    Summay:
        Alarm setting.
"""

from datetime import datetime, time

class AlarmSetting:
    """ AlarmSetting. """

    # Define properties.
    __PROP_TIME = "time"
    __PROP_DAYS = "days"
    __PROPERTIES = [__PROP_TIME, __PROP_DAYS]

    # Reset time of alarm setting.
    __RESET_TIME = datetime.strptime("00:00", '%H:%M').time()

    def __init__(self, time: datetime, days: list):
        """ Init constructor.
        """
        # self.time = time
        # self.days = days
        self.__dict__[self.__PROP_TIME] = time
        self.__dict__[self.__PROP_DAYS] = days

        self.__isEnabled = True
        self.__isAlreadyReset = False

    @property
    def time(self) -> time:
        """ time property.
        Returns:
            (time): datetime.time
        """
        return self.__dict__[self.__PROP_TIME]

    @property
    def days(self) -> list:
        """ days property.
        Returns:
            (list): days of week.
        """
        return self.__dict__[self.__PROP_DAYS]

    def isSetTime(self, now: datetime) -> bool:
        """ Check the setting time.
        Args:
            now (datetime): Current time.
        Returns:
            (bool): Judgment value of check the alarm setting.
        """
        self.__resetEnabledSetting(now.time())
        return self.__isSettingTime(now.time()) \
                and self.__isSettingDay(now.strftime('%a')) \
                and self.__isEnabled

    def setEnabled(self, enabled: bool):
        """ Set the enabled value.
        Args:
            enabled (bool): Setting value.
        """
        self.__isEnabled = enabled

    def serialize(self) -> dict:
        """ Serialize the AlarmSetting object.
            Return the dict type of the defined property.
        Returns:
            retVal (dict): Serialized value.
        """
        retVal = {}
        for key, value in self.__dict__.items():
            # Only defined properties.
            if self.__PROPERTIES in key:
                # The time type does not support json.
                # Convert time to str.
                if isinstance(value, time):
                    retVal[key] = value.strftime('%H:%M')
                else:
                    retVal[key] = value
        return retVal

    @classmethod
    def deserialize(cls, dict: dict):
        """ Deserialize the AlarmSetting object.
            Create the myself class from the dict data.
        Args:
            dict (dict): Setting data.
        Returns:
            (AlarmSetting): myself object.
        """
        # Return None if there is no defined property in the dict data.
        for prop in cls.__PROPERTIES:
            if prop not in dict:
                return None

        return cls(datetime.strptime(dict[cls.__PROP_TIME], '%H:%M').time(), dict[cls.__PROP_DAYS])


    def __isSettingTime(self, time: time) -> bool:
        """ Check the setting time.
        Args:
            time (time): Current time.
        Returns:
            (bool): Judgment value of check the setting time.
        """        
        return time.replace(second=0, microsecond=0) == self.time

    def __isSettingDay(self, day: str) -> bool:
        """ Check the setting day of the week.
        Args:
            day (str): Current day of the week.
        Returns:
            (bool): Judgment value of check the setting day of the week.
        """
        return day in self.days

    def __resetEnabledSetting(self, time: time):
        """ Reset the enabled value.
        Args:
            time (time): Current time.
        """
        time = time.replace(second=0, microsecond=0)

        # Matche the reset time and not yet reset.
        # Execute the reset process only during the reset time.
        if time == self.__RESET_TIME \
            and self.__isAlreadyReset == False:
            # Reset process.
            # Set enabled.
            self.setEnabled(True)
            self.__isAlreadyReset = True
        elif time != self.__RESET_TIME \
                and self.__isAlreadyReset == True:
            # Set false isAlreadyReset flg.
            self.__isAlreadyReset = False