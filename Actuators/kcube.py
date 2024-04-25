import ctypes
import time

# Load the DLL
kinesis_path = "C:\\Program Files\\Thorlabs\\Kinesis\\"  # Adjust path if necessary
stepper_motor_dll = ctypes.cdll.LoadLibrary(kinesis_path + "Thorlabs.MotionControl.KCube.StepperMotor.dll")

# Device parameters
serial_no = "12345678"  # Replace with your motor's serial number
channel = 1  # Typically 1 for single-channel devices

# Initialize the device
stepper_motor_dll.TLI_BuildDeviceList()
stepper_motor_dll.CC_Open(serial_no.encode())
stepper_motor_dll.CC_StartPolling(serial_no.encode(), channel, 200)  # Polling at 200 ms
stepper_motor_dll.CC_ClearMessageQueue(serial_no.encode(), channel)

# Wait for the device to connect properly
time.sleep(1)

# Move the motor (example command)
new_position = 500000  # Example position
stepper_motor_dll.CC_MoveToPosition(serial_no.encode(), channel, new_position)
time.sleep(5)  # Wait for the motor to reach the position

# Check the current position
position = stepper_motor_dll.CC_GetPosition(serial_no.encode(), channel)
print("Current Position:", position)

# Stop the motor and close connection
stepper_motor_dll.CC_StopPolling(serial_no.encode(), channel)
stepper_motor_dll.CC_Close(serial_no.encode())

