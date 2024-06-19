"""

"""
import logging
import platform
from mecom import MeComSerial, ResponseException, WrongChecksum
from serial import SerialException
from serial.serialutil import PortNotOpenError
from navigateToThenTrigger import automate_GUI
import time
import threading

# default queries from command table below
DEFAULT_QUERIES = [
    "loop status",
    "object temperature",
    "target object temperature",
    "output current",
    "output voltage"
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
}

MAX_COM = 256

class MeerstetterTEC(object):
    """
    Controlling TEC devices via serial.
    """

    def _tearDown(self):
        self.session().stop()

    def __init__(self, port=None, scan_timeout=30, channel=1, queries=DEFAULT_QUERIES, *args, **kwars):
        assert channel in (1, 2)
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
                value = self.session().get_parameter(parameter_id=id, address=self.address, parameter_instance=self.channel)
                data.update({description: (value, unit)})
            except (ResponseException, WrongChecksum) as ex:
                self.session().stop()
                self._session = None
        return data

    def set_temp(self, value):
        """
        Set object temperature of channel to desired value.
        :param value: float
        :param channel: int
        :return:
        """
        # assertion to explicitly enter floats
        assert type(value) is float
        logging.info("set object temperature for channel {} to {} C".format(self.channel, value))
        return self.session().set_parameter(parameter_id=3000, value=value, address=self.address, parameter_instance=self.channel)


    def ramp_temp(self, starting_temp, target_temp, ramp_rate, numberOfWells):
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
        current_temp = self.get_data()["object temperature"][0]
        current_temp = float(current_temp)  #cast to a float
        target_temp = float(target_temp) 
        hold_rate= 10 + (numberOfWells*10) + 10
        autoGUI = automate_GUI()
        autoGUI.getButtonLocation(10)
        x, y = autoGUI.final_mouse_x, autoGUI.final_mouse_y
        self.enable()
        
        print(x, y)
        
        #ramp to the initial starting temperature 
        self.set_temp(starting_temp) 
        while abs(current_temp - starting_temp) > 0.01: #wait before proceeding
            time.sleep(1)
            current_temp = self.get_data()["object temperature"][0]
            current_temp = float(current_temp)  #cast to a float
            print("currentTemp is: " + str(current_temp))
            if abs(current_temp - starting_temp) < 0.01:
                    break
        
        #initial scan at starting temp
        print("allowing temp to stablize (holding temp for 1 min before scanning)")
        time.sleep(60)
        print(x,y)
        autoGUI.clickButton()
        print("holding " + str(current_temp))
        time.sleep(hold_rate) 
        print("starting temp is " + str(current_temp))
        
        rampTo = current_temp
        timeTotal = 0.0
        numberOfRamps = 0.0
        
        #loop to decrese the temp:
        if target_temp < current_temp:
            while abs(current_temp - target_temp) > 0.01:  # using a tolerance of 0.01
                rampTo = rampTo - ramp_rate if rampTo - ramp_rate >= target_temp else target_temp
                print("ramping to: " + str(rampTo))
                self.set_temp(rampTo)
                
                numberOfRamps += 1.0
                start_time = time.time()
                
                
                while True: 
                    time.sleep(1)
                    current_temp = self.get_data()["object temperature"][0]
                    current_temp = float(current_temp)  #cast to a float
                    print("currentTemp is: " + str(current_temp))
                    if abs(current_temp - rampTo) < 0.01:
                        end_time = time.time()
                        break
                
                timeTotal+= end_time-start_time
                
                print("allowing temp to stablize (holding temp for 1 min before scanning)")
                time.sleep(60)
                print(x,y)
                autoGUI.clickButton()
                print("holding " + str(current_temp))
                time.sleep(hold_rate)

            print("temp ramp is complete")

        else: #loop to increment the temp
            while abs(current_temp - target_temp) > 0.01:  # using a tolerance of 0.01
               
                rampTo = rampTo + ramp_rate if rampTo + ramp_rate <= target_temp else target_temp
                print("ramping to: " + str(rampTo))
                print(self.set_temp(rampTo))
                
                numberOfRamps += 1.0
                start_time = time.time()
                                
                while True: 
                    time.sleep(1)
                    current_temp = self.get_data()["object temperature"][0]
                    current_temp = float(current_temp)  #cast to a float
                    print("currenTemp is: " + str(current_temp))
                    if abs(current_temp - rampTo) < 0.01:
                        break
                
                end_time = time.time()
                timeTotal+= end_time-start_time
                
                print("allowing temp to stablize")
                time.sleep(60)
                print(x,y)
                autoGUI.clickButton()
                print("holding and scanning @ " + str(current_temp))
                time.sleep(hold_rate)
                     
        #last scan at target temperature
        print("allowing temp to stablize (holding temp for 1 min before scanning)")
        time.sleep(60)
        print(x,y)
        autoGUI.clickButton()
        print("holding " + str(current_temp))
        time.sleep(hold_rate) 
        
        #this is code to ramp temperature back down to 20 degrees, then switch static on back off
        print('begining ramp down')
        target_temp = 20
        while abs(current_temp - target_temp) > 0.01:  # using a tolerance of 0.01
               
            rampTo = rampTo + ramp_rate if rampTo + ramp_rate <= target_temp else target_temp
            print("ramping to: " + str(rampTo))
            print(self.set_temp(rampTo))
                                                
            while True: 
                time.sleep(1)
                current_temp = self.get_data()["object temperature"][0]
                current_temp = float(current_temp)  #cast to a float
                print("currentTemp is: " + str(current_temp))
                if abs(current_temp - rampTo) < 0.01:
                    time.sleep(15)
                    break
        time.sleep(15)
        self.disable() #so as to not ramp temp next time you turn the TEC on 
            

    def _set_enable(self, enable=True):
        """
        Enable or disable control loop
        :param enable: bool
        :param channel: int
        :return:
        """
        value, description = (1, "on") if enable else (0, "off")
        logging.info("set loop for channel {} to {}".format(self.channel, description))
        return self.session().set_parameter(value=value, parameter_name="Status", address=self.address, parameter_instance=self.channel)

    def enable(self):
        return self._set_enable(True)

    def disable(self):
        return self._set_enable(False)
    
    def start_ramp_temp(self, starting_temp, target_temp, ramp_rate, numberOfWells):
        # Run the ramp_temp method in a separate thread
        thread = threading.Thread(target=self.ramp_temp, args=(starting_temp, target_temp, ramp_rate, numberOfWells))
        thread.start()

""" 
if __name__ == '__main__':
    # start logging
    logging.basicConfig(level=logging.DEBUG, format="%(asctime)s:%(module)s:%(levelname)s:%(message)s")

    # initialize controller
    mc = MeerstetterTEC()

    mc.enable()
    # get the values from DEFAULT_QUERIES
    print(mc.get_data())
    

    # yeet the values
    mc.start_ramp_temp(20.0, -5.0, 2.0, 3) 
    
"""