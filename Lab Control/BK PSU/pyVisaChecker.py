import pyvisa as visa

# Create a resource manager object
rm = visa.ResourceManager()

# List all connected devices
devices = rm.list_resources()

# Print the devices and their addresses
print("Connected devices:")
for i, device in devices:
    print(device, " : ", i)
