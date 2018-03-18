import time
from dronekit import connect, VehicleMode
connection_string = '/dev/ttyACM1'

#Connect to the Vehicle.
print("Connecting to vehicle on: %s" % (connection_string))
vehicle = connect(connection_string, wait_ready=True)

# Get some vehicle attributes (state)
print (" Is Armable?: %s" % ( vehicle.is_armable))
print (" System status: %s" % ( vehicle.system_status.state))
print (" GPS: %s" % ( vehicle.gps_0))
print (" Battery: %s" % ( vehicle.battery))
print (" Is Armable?: %s" % ( vehicle.is_armable))
print (" Mode: %s" % ( vehicle.mode.name))    # settable

for i in range(0,10):
    print ("att: %s" % ( vehicle.attitude  ))  # settable
    print ("pitchspeed: %s" % ( vehicle._pitchspeed  ))  # settable
    print ("roll speed: %s" % ( vehicle._rollspeed  ))  # settable
    print ("yawspeed: %s" % ( vehicle._yawspeed  ))  # settable
    time.sleep(1/30)

# Close vehicle object before exiting script
vehicle.close()

# Shut down simulator
print("Completed")
