"""
This module provides a class for controlling Meerstetter TEC devices via serial.
It is based on the MeCom protocol. It controls the temperature ramping of the TEC. 
"""

import logging
import platform
from mecom import MeComSerial, ResponseException, WrongChecksum
from serial import SerialException
from serial.serialutil import PortNotOpenError
from automateGUI import automateGUI
import time
import datetime
#import matplotlib.pyplot as plt
#import matplotlib.animation as animation


# default queries from command table below
DEFAULT_QUERIES = [
    "loop status",
    "object temperature",
    "target object temperature",
    "output current",
    "output voltage"
    "device status"
    
]

# syntax
# { display_name: [parameter_id, unit], }
COMMAND_TABLE = {
    "loop status": [1200, ""],
    "object temperature": [1000, "degC"],
    "target object temperature": [1010, "degC"],
    "output current": [1020, "A"],
    "output voltage": [1021, "V"],
    "sink temperature": [1001, "degC"],
    "ramp temperature": [1011, "degC"],
    "device status": [1201, "1 or 0"]
}

CSV_QUERIES = [
    "object temperature", 
    "output current", 
    "output voltage"
    ]

CSV_COMMAND_TABLE = {
    "object temperature": 1000,
    "output current": 1020,
    "output voltage": 1021
}

MAX_COM = 256

class MeerstetterTEC(object):
    """
    Controlling TEC devices via serial.
    """

    def _tearDown(self):
        self.session().stop()

    def __init__(self, port=None, scan_timeout=30, channel=[1,2], queries=DEFAULT_QUERIES, *args, **kwars):
        self.channel = channel
        self.port = port
        self.scan_timeout = scan_timeout
        self.queries = queries
        self._session = None
        self._connect()

    def _connect(self):
        # open session
        if self.port is not None:
            self._session = MeComSerial(serialport=self.port)
        else:
            if platform.system() != "Windows":
                start_index = 0
                base_name = "/dev/ttyUSB"
            else:
                start_index = 1
                base_name = "COM"

            scan_start_time = time.time()
            while True:
                for i in range(start_index, MAX_COM + 1):
                    try:
                        self._session = MeComSerial(serialport=base_name + str(i))
                        break
                    except SerialException:
                        pass
                if self._session is not None or (time.time() - scan_start_time) >= self.scan_timeout:
                    break
                time.sleep(0.1) # 100 ms wait time between each scan attempt

            if self._session is None:
                 raise PortNotOpenError
        # get device address
        self.address = self._session.identify()
        logging.info("connected to {}".format(self.address))

    def session(self):
        if self._session is None:
            self._connect()
        return self._session

    def get_data(self):
        data = {}
        
        for description in self.queries:
            id, unit = COMMAND_TABLE[description]
            try:
                value = self.session().get_parameter(parameter_id=id, address=self.address, parameter_instance=self.channel[0])
                data.update({description: (value, unit)})
            except (ResponseException, WrongChecksum) as ex:
                self.session().stop()
                self._session = None
        return data
    
    def get_param(self, param_id):
        try:
            value = self.session().get_parameter(parameter_id=param_id, address=self.address, parameter_instance=self.channel[0])
        except (ResponseException, WrongChecksum) as ex:
            self.session().stop()
            self._session = None
        return value
    
    def get_data_csv(self):
        data = []
        
        #get current time and append it first
        current_time = datetime.datetime.now()  # Get the current time
        formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S")  # Format the time as a string
        data.append(formatted_time)
        
        for query in CSV_QUERIES:
            id = COMMAND_TABLE[query][0]
            try:
                value = self.session().get_parameter(parameter_id=id, address=self.address, parameter_instance=self.channel[0])
                data.append(value)
            except (ResponseException, WrongChecksum) as ex:
                self.session().stop()
                self._session = None
        return data
    
    def get_temp(self) -> float:
        id = COMMAND_TABLE["object temperature"][0]
        try:
            value = self.session().get_parameter(parameter_id=id, address=self.address, parameter_instance=self.channel[0])
        except (ResponseException, WrongChecksum) as ex:
                self.session().stop()
                self._session = None
        return value 
                  
    def set_temp(self, value):
        """
        Set object temperature of channel to desired value.
        :param value: float
        :param channel: int
        :return:
        """
        # assertion to explicitly enter floats
        assert type(value) is float
        logging.info("set object temperature for channel {} to {} C".format(self.channel[0], value))
        logging.info("set object temperature for channel {} to {} C".format(self.channel[1], value))

        self.session().set_parameter(parameter_id=3000, value=value, address=self.address, parameter_instance=self.channel[0])
        return self.session().set_parameter(parameter_id=3000, value=value, address=self.address, parameter_instance=self.channel[1])

    def ramp_to(self, target_temp, ramp_rate, hold_rate, autoGUI, end_ramp_event, rampUp = True):

        current_temp = self.get_temp() #get the current temperature
        rampTo = current_temp
        times = []
                       
        while abs(current_temp - target_temp) > 0.1 and not end_ramp_event.is_set():  # using a tolerance of 0.01
            if rampUp:
                #increment the rampTo value by the ramp_rate if the rampTo value plus the ramp_rate is less than the target_temp
                rampTo = rampTo + ramp_rate if rampTo + ramp_rate <= target_temp else target_temp 
            else:
                #decrement the rampTo value by the ramp_rate if the rampTo value minus the ramp_rate is greater than the target_temp
                rampTo = rampTo - ramp_rate if rampTo - ramp_rate >= target_temp else target_temp
            
            print("ramping to: " + str(rampTo))
            self.set_temp(rampTo)
            first_time = time.time()                
            
            while abs(current_temp-rampTo)>0.1 and not end_ramp_event.is_set():  #loop until the current temperature is within 0.1 of the rampTo value
                time.sleep(1)                                                   
                current_temp = self.get_temp()
                current_temp = float(current_temp)  #cast to a float
                print("currenTemp is: " + str(current_temp))

            second_time = time.time()
            time_to_increment_temp = second_time - first_time
            times.append(time_to_increment_temp)
            print("time to increment temp: " + str(second_time - first_time))
            
            if autoGUI != None: #if scan is true, scan at the current temperature
                autoGUI.scan(current_temp, hold_rate, end_ramp_event)  
            else: #otherwise, sleep, allowing temp to stabilize
                time.sleep(10)
        """     
        print(f'average time to increment temp is: {sum(times)/len(times)}')
        print(f"times array: {times}")
        """
    
    #TODO: clean ramp_temp and ramp_to methods !!!
    def ramp_temp(self, starting_temp, target_temp, ramp_rate, numberOfWells, end_ramp_event):
        """
        Ramp the temperature to the target temperature with a specified ramp rate and hold rate.

        Parameters:
        - starting_temp (float): the temperature you want to start your ramp at
        - target_temp (float): The desired target temperature.
        - ramp_rate (float): The interval (in degrees C) that the temperature will ramp at, i.e. it will pause
          every x degrees to initiate a scan.  
        - holdRate (float): The duration to hold the temperature after reaching the target temperature.

        Returns:
        None
        """
        hold_rate= (numberOfWells*10) + 10 #calculate the hold rate based on the number of wells
        autoGUI = automateGUI()  #create an automateGUI object
        autoGUI.getButtonLocation() #get the start button location
        current_temp = self.get_temp() #get the current temperature
        self.enable() #enable the TEC
        
        start_time_of_ramp = time.time()

        #ramp to the initial starting temperature
        if starting_temp < current_temp: #if the starting temp is less than the current temp, ramp down to the starting temp
            self.ramp_to(starting_temp, 3, hold_rate, None, end_ramp_event, rampUp = False)
        else: #otherwise, ramp up to the starting temp
            self.ramp_to(starting_temp, 5, hold_rate, None, end_ramp_event, rampUp = True)
    
        #initial scan at starting temp
        current_temp = self.get_temp()
        autoGUI.scan(current_temp, hold_rate, end_ramp_event) 
        print("starting temp is " + str(current_temp))  
    
        #preform the actual ramping
        if self.get_temp() < target_temp:
            self.ramp_to(target_temp, ramp_rate, hold_rate, autoGUI, end_ramp_event, rampUp = True)
        else:
            self.ramp_to(target_temp, ramp_rate, hold_rate, autoGUI, end_ramp_event, rampUp = False)
        
        end_time_of_ramp = time.time()
        print(f'total time to ramp: {end_time_of_ramp - start_time_of_ramp}')          
        end_ramp_event.set() #signal that the program is over

    def _set_enable(self, enable=True):
        """
        Enable or disable control loop
        :param enable: bool
        :param channel: int
        :return:
        """
        value, description = (1, "on") if enable else (0, "off")
        logging.info("set loop for channel {} to {}".format(self.channel, description))
        self.session().set_parameter(value=value, parameter_name="Status", address=self.address, parameter_instance=self.channel[0])
        return self.session().set_parameter(value=value, parameter_name="Status", address=self.address, parameter_instance=self.channel[1])

    def enable(self):
        return self._set_enable(True)

    def disable(self):
        return self._set_enable(False)
