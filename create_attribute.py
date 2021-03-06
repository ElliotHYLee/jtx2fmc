from __future__ import print_function

from dronekit import connect, Vehicle
from my_vehicle import MyVehicle #Our custom vehicle class
import time

def raw_imu_callback(self, attr_name, value):
    # attr_name == 'raw_imu'
    # value == vehicle.raw_imu
    print(value)

connection_string = '/dev/ttyACM0'#args.connect

# Connect to the Vehicle
print('Connecting to vehicle on: %s' % connection_string)
vehicle = connect(connection_string, wait_ready=True, vehicle_class=MyVehicle)

# Add observer for the custom attribute
#vehicle.add_attribute_listener('raw_imu', raw_imu_callback)

print('Display RAW_IMU messages for 1 seconds and then exit.')
#time.sleep(1)
for i in range (0, 10):
    print (vehicle.raw_imu)
    time.sleep(1)

#The message listener can be unset using ``vehicle.remove_message_listener``

#Close vehicle object before exiting script
print("Close vehicle object")
vehicle.close()
