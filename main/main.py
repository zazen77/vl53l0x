from machine import Pin, I2C
from vl53l0x import setup_tofl_device, TBOOT
import utime

device_1_xshut = Pin(18, Pin.OUT)
device_2_xshut = Pin(19, Pin.OUT)
device_3_xshut = Pin(20, Pin.OUT)

device_1_xshut.value(0)
device_2_xshut.value(0)
device_3_xshut.value(0)

i2c_1 = I2C(id=1, sda=Pin(14), scl=Pin(15))

# Set up device 1
print("Setting up device 1")
device_1_xshut.value(1)
utime.sleep_us(TBOOT)

tof_1 = setup_tofl_device(i2c_1, 40000, 18, 14)
tof_1.set_address(0x2a)

# Set up device 2
print("Setting up device 2")
device_2_xshut.value(1)
utime.sleep_us(TBOOT)

tof_2 = setup_tofl_device(i2c_1, 40000, 12, 8)
tof_2.set_address(0x2b)

try:
    # Set up device 3
    print("Setting up device 3")
    device_3_xshut.value(1)
    utime.sleep_us(TBOOT)

    tof_3 = setup_tofl_device(i2c_1, 40000, 12, 8)
        
    while True:
        dev1, dev2, dev3 = tof_1.ping(), tof_2.ping(), tof_3.ping()
        print(dev1, 'mm, ', dev2, 'mm', dev3, 'mm')
        utime.sleep_ms(1000)
finally:
    # Restore default address
    print("Restoring")
    tof_1.set_address(0x29)
    tof_2.set_address(0x29)
