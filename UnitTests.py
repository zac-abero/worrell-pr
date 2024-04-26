import unittest
from unittest.mock import MagicMock
from example import MeerstetterTEC

class TestMeerstetterTEC(unittest.TestCase):

    def setUp(self):
        self.tec = MeerstetterTEC()

    def test_get_data(self):
        # Mock the session and set the return values for get_parameter
        self.tec.session().get_parameter = MagicMock(side_effect=[10, 20, 30, 40, 50])
        
        expected_data = {
            "loop status": (10, ""),
            "object temperature": (20, "degC"),
            "target object temperature": (30, "degC"),
            "output current": (40, "A"),
            "output voltage": (50, "V")
        }
        
        self.assertEqual(self.tec.get_data(), expected_data)

    def test_set_temp(self):
        # Mock the session and assert that set_parameter is called with the correct values
        self.tec.session().set_parameter = MagicMock()
        self.tec.set_temp(25.0)
        self.tec.session().set_parameter.assert_called_with(parameter_id=3000, value=25.0, address=self.tec.address, parameter_instance=self.tec.channel)

    def test_ramp_temp(self):
        # Mock the get_data method to return a specific value for "object temperature"
        self.tec.get_data = MagicMock(return_value={"object temperature": (20, "degC")})
        
        # Mock the set_temp method and assert that it is called with the correct values
        self.tec.set_temp = MagicMock()
        self.tec.ramp_temp(25, 1, 60)
        self.tec.set_temp.assert_called_with(25)

    def test_enable(self):
        # Mock the set_parameter method and assert that it is called with the correct values
        self.tec.session().set_parameter = MagicMock()
        self.tec.enable()
        self.tec.session().set_parameter.assert_called_with(value=1, parameter_name="Status", address=self.tec.address, parameter_instance=self.tec.channel)

    def test_disable(self):
        # Mock the set_parameter method and assert that it is called with the correct values
        self.tec.session().set_parameter = MagicMock()
        self.tec.disable()
        self.tec.session().set_parameter.assert_called_with(value=0, parameter_name="Status", address=self.tec.address, parameter_instance=self.tec.channel)

if __name__ == '__main__':
    unittest.main()

