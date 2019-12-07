# The MIT License (MIT)
#
# Copyright (c) 2019 Bryan Siepert for Adafruit Industries
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
"""
`adafruit_icm20649`
================================================================================

Library for the ST ICM20649 Wide-Range 6-DoF Accelerometer and Gyro

* Author(s): Bryan Siepert

Implementation Notes
--------------------

**Hardware:**

* Adafruit's ICM20649 Breakout: https://adafruit.com/product/4464

**Software and Dependencies:**

* Adafruit CircuitPython firmware for the supported boards:
  https://circuitpython.org/downloads


* Adafruit's Bus Device library: https://github.com/adafruit/Adafruit_CircuitPython_BusDevice
* Adafruit's Register library: https://github.com/adafruit/Adafruit_CircuitPython_Register
"""

__version__ = "0.0.0-auto.0"
__repo__ = "https://github.com/adafruit/Adafruit_CircuitPython_ICM20649.git"
# Common imports; remove if unused or pylint will complain
from time import sleep
import adafruit_bus_device.i2c_device as i2c_device

from adafruit_register.i2c_struct import UnaryStruct, ROUnaryStruct, Struct
from adafruit_register.i2c_bit import RWBit
from adafruit_register.i2c_bits import RWBits

#pylint: disable=bad-whitespace
_ICM20649_DEFAULT_ADDRESS = 0x68 #icm20649 default i2c address
_ICM20649_DEVICE_ID = 0xE1 # Correct context of WHO_AM_I register

# Bank 0
_ICM20649_WHO_AM_I = 0x00  # device_id register
_ICM20649_REG_BANK_SEL = 0x7F # register bank selection register
_ICM20649_PWR_MGMT_1  = 0x06 #primary power management register
_ICM20649_ACCEL_XOUT_H = 0x2D # first byte of accel data
_ICM20649_GYRO_XOUT_H = 0x33 # first byte of accel data

# Bank 2
_ICM20649_GYRO_SMPLRT_DIV = 0x00
_ICM20649_GYRO_CONFIG_1     = 0x01
_ICM20649_ACCEL_SMPLRT_DIV_1 = 0x10
_ICM20649_ACCEL_SMPLRT_DIV_2 = 0x11
_ICM20649_ACCEL_CONFIG_1     = 0x14


G_TO_ACCEL           = 9.80665
#pylint: enable=bad-whitespace
class CV:
    """struct helper"""

    @classmethod
    def add_values(cls, value_tuples):
        """Add CV values to the class"""
        cls.string = {}
        cls.lsb = {}

        for value_tuple in value_tuples:
            name, value, string, lsb = value_tuple
            setattr(cls, name, value)
            cls.string[value] = string
            cls.lsb[value] = lsb

    @classmethod
    def is_valid(cls, value):
        """Validate that a given value is a member"""
        return value in cls.string



class AccelRange(CV):
    """Options for ``accelerometer_range``"""
    pass #pylint: disable=unnecessary-pass

AccelRange.add_values((
    ('RANGE_4G', 0, 4, 8192),
    ('RANGE_8G', 1, 8, 4096.0),
    ('RANGE_16G', 2, 16, 2048),
    ('RANGE_30G', 3, 30, 1024),
))

class GyroRange(CV):
    """Options for ``gyro_data_range``"""
    pass #pylint: disable=unnecessary-pass

GyroRange.add_values((
    ('RANGE_500_DPS', 0, 500, 65.5),
    ('RANGE_1000_DPS', 1, 1000, 32.8),
    ('RANGE_2000_DPS', 2, 2000, 16.4),
    ('RANGE_4000_DPS', 3, 4000, 8.2)
))


class ICM20649: #pylint:disable=too-many-instance-attributes
    """Library for the ST ICM-20649 Wide-Range 6-DoF Accelerometer and Gyro.

        :param ~busio.I2C i2c_bus: The I2C bus the ICM20649 is connected to.
        :param address: The I2C slave address of the sensor

    """

    # Bank 0
    _device_id = ROUnaryStruct(_ICM20649_WHO_AM_I, "<B")
    _bank = RWBits(2, _ICM20649_REG_BANK_SEL, 4)
    _reset = RWBit(_ICM20649_PWR_MGMT_1, 7)
    _sleep = RWBit(_ICM20649_PWR_MGMT_1, 6)
    _clock_source = RWBits(3, _ICM20649_PWR_MGMT_1, 0)

    _raw_accel_data = Struct(_ICM20649_ACCEL_XOUT_H, ">hhh")
    _raw_gyro_data = Struct(_ICM20649_GYRO_XOUT_H, ">hhh")

    # Bank 2
    _gyro_range = RWBits(2, _ICM20649_GYRO_CONFIG_1, 1)
    _accel_dlpf_enable = RWBits(1, _ICM20649_ACCEL_CONFIG_1, 0)
    _accel_range = RWBits(2, _ICM20649_ACCEL_CONFIG_1, 1)
    _accel_dlpf_config = RWBits(3, _ICM20649_ACCEL_CONFIG_1, 3)

    # this value is a 12-bit register spread across two bytes, big-endian first
    _accel_rate_divisor = UnaryStruct(_ICM20649_ACCEL_SMPLRT_DIV_1, ">H")

    _gyro_rate_divisor = UnaryStruct(_ICM20649_GYRO_SMPLRT_DIV, ">B")

    def __init__(self, i2c_bus, address=_ICM20649_DEFAULT_ADDRESS):
        self.i2c_device = i2c_device.I2CDevice(i2c_bus, address)
        if self._device_id != _ICM20649_DEVICE_ID:
            raise RuntimeError("Failed to find ICM20649 - check your wiring!")
        self.reset()

        self._bank = 0
        self._sleep = False

        self._bank = 2
        self._accel_range = AccelRange.RANGE_8G #pylint: disable=no-member
        self._cached_accel_range = self._accel_range

        #TODO: CV-ify
        self._accel_dlpf_config = 3


        # 1.125 kHz/(1+ACCEL_SMPLRT_DIV[11:0]),
        # 1125Hz/(1+20) = 53.57Hz
        self._accel_rate_divisor = 20

        # writeByte(ICM20649_ADDR,GYRO_CONFIG_1, gyroConfig);
        self._gyro_range = GyroRange.RANGE_500_DPS #pylint: disable=no-member
        sleep(0.100)
        self._cached_gyro_range = self._gyro_range

        # //ORD = 1100Hz/(1+10) = 100Hz
        self._gyro_rate_divisor = 0x0A

        # //reset to register bank 0
        self._bank = 0

    def reset(self):
        """Resets the internal registers and restores the default settings"""
        self._reset = True
        while self._reset:
            sleep(0.001)

    @property
    def acceleration(self):
        """The x, y, z acceleration values returned in a 3-tuple and are in m / s ^ 2."""
        raw_accel_data = self._raw_accel_data

        x = self._scale_xl_data(raw_accel_data[0])
        y = self._scale_xl_data(raw_accel_data[1])
        z = self._scale_xl_data(raw_accel_data[2])

        return(x, y, z)

    @property
    def gyro(self):
        """The x, y, z angular velocity values returned in a 3-tuple and are in degrees / second"""
        raw_gyro_data = self._raw_gyro_data
        x = self._scale_gyro_data(raw_gyro_data[0])
        y = self._scale_gyro_data(raw_gyro_data[1])
        z = self._scale_gyro_data(raw_gyro_data[2])

        return (x, y, z)

    def _scale_xl_data(self, raw_measurement):
        return raw_measurement / AccelRange.lsb[self._cached_accel_range] * G_TO_ACCEL

    def _scale_gyro_data(self, raw_measurement):
        return raw_measurement / GyroRange.lsb[self._cached_gyro_range]

    @property
    def accelerometer_range(self):
        """Adjusts the range of values that the sensor can measure, from +/- 4G to +/-30G
        Note that larger ranges will be less accurate. Must be an `AccelRange`"""
        return self._cached_accel_range

    @accelerometer_range.setter
    def accelerometer_range(self, value): #pylint: disable=no-member
        if not AccelRange.is_valid(value):
            raise AttributeError("range must be an `AccelRange`")
        self._bank = 2
        self._accel_range = value
        self._cached_accel_range = value
        self._bank = 0

    @property
    def gyro_range(self):
        """Adjusts the range of values that the sensor can measure, from 500 Degrees/second to 4000
        degrees/s. Note that larger ranges will be less accurate. Must be a `GyroRange`"""
        return self._cached_gyro_range

    @gyro_range.setter
    def gyro_range(self, value):
        if not GyroRange.is_valid(value):
            raise AttributeError("range must be a `GyroRange`")

        self._bank = 2
        self._gyro_range = value
        self._cached_gyro_range = value
        self._bank = 0
        sleep(.100) # needed to let new range settle

    @property
    def accelerometer_data_rate_divisor(self):
        """The divisor for the rate at which accelerometer measurements are taken in Hz

        Note: The data rates are set indirectly by setting a rate divisor according to the
        following formula: ``accelerometer_data_rate = 1125/(1+divisor)``

        This function sets the raw rate divisor.
"""
        self._bank = 2
        raw_rate_divisor = self._accel_rate_divisor
        self._bank = 0
        #rate_hz = 1125/(1+raw_rate_divisor)
        return raw_rate_divisor

    @accelerometer_data_rate_divisor.setter
    def accelerometer_data_rate_divisor(self, value):
        # check that value <= 4095
        self._bank = 2
        self._accel_rate_divisor = value
        self._bank = 0

    @property
    def gyro_data_rate_divisor(self):
        """The divisor for the rate at which gyro measurements are taken in Hz

        Note: The data rates are set indirectly by setting a rate divisor according to the
        following formula: ``gyro_data_rate = 1100/(1+divisor)``

        This function sets the raw rate divisor.
        """

        self._bank = 2
        raw_rate_divisor = self._gyro_rate_divisor
        self._bank = 0
        # rate_hz = 1100/(1+raw_rate_divisor)
        return raw_rate_divisor

    @gyro_data_rate_divisor.setter
    def gyro_data_rate_divisor(self, value):
        # check that value <= 255
        self._bank = 2
        self._gyro_rate_divisor = value
        self._bank = 0

    def _accel_rate_calc(self, divisor):#pylint:disable=no-self-use
        return 1125/(1+divisor)

    def _gyro_rate_calc(self, divisor):#pylint:disable=no-self-use
        return 1100/(1+divisor)

    @property
    def accelerometer_data_rate(self):
        """The rate at which accelerometer measurements are taken in Hz

        Note: The data rates are set indirectly by setting a rate divisor according to the
        following formula: ``accelerometer_data_rate = 1125/(1+divisor)``

        This function does the math to find the divisor from a given rate but it will not be
        exactly as specified.
        """
        return self._accel_rate_calc(self.accelerometer_data_rate_divisor)

    @accelerometer_data_rate.setter
    def accelerometer_data_rate(self, value):
        if value < self._accel_rate_calc(4095) or value > self._accel_rate_calc(0):
            raise AttributeError("Accelerometer data rate must be between 0.27 and 1125.0")
        self.accelerometer_data_rate_divisor = value

    @property
    def gyro_data_rate(self):
        """The rate at which gyro measurements are taken in Hz

        Note: The data rates are set indirectly by setting a rate divisor according to the
        following formula: ``gyro_data_rate = 1100/(1+divisor)``

        This function does the math to find the divisor from a given rate but it will not
        be exactly as specified.
        """
        return self._gyro_rate_calc(self.gyro_data_rate_divisor)

    @gyro_data_rate.setter
    def gyro_data_rate(self, value):
        if value < self._gyro_rate_calc(4095) or value > self._gyro_rate_calc(0):
            raise AttributeError("Gyro data rate must be between 4.30 and 1100.0")

        divisor = round(((1125.0-value)/ value))
        self.gyro_data_rate_divisor = divisor
