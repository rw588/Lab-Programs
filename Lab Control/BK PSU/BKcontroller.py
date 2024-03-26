import pyvisa as visa
import time

# Define the power supply parameters
voltage_setpoint = 12  # Volts
current_setpoint = 1   # Amperes

# Connect to the power supply
rm = visa.ResourceManager()
device_address = 'GPIB0::1::INSTR'  # Replace this with the actual address of your power supply
psu = rm.open_resource(device_address)
psu.timeout = 10000  # Set the timeout to 10 seconds

# Reset the power supply
psu.write('*RST')

# Configure the power supply
psu.write('SOUR:VOLT {0}'.format(voltage_setpoint))
psu.write('SOUR:CURR {0}'.format(current_setpoint))

# Turn on the output
psu.write('OUTP:STAT ON')

# Wait for 10 seconds
time.sleep(10)

# Measure the output voltage and current
measured_voltage = float(psu.query('MEAS:VOLT?'))
measured_current = float(psu.query('MEAS:CURR?'))

print('Measured Voltage: {:.2f} V'.format(measured_voltage))
print('Measured Current: {:.2f} A'.format(measured_current))

# Turn off the output
psu.write('OUTP:STAT OFF')

# Close the connection to the power supply
psu.close()
