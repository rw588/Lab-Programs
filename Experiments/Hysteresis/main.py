import IDS

import time
import matplotlib.pyplot as plt
import numpy as np
import pyvisa
from pymeasure.instruments.keithley import Keithley2450



#connect ids
ids = IDS.Device('192.168.1.1')
ids.connect()

#connect Keithley
# resource_manager = pyvisa.ResourceManager()
# ins_kth2450 = resource_manager.open_resource("TCPIP::192.168.1.21::inst0::INSTR")
sourcemeter = Keithley2450("TCPIP::192.168.1.3::inst0::INSTR")

#align

#initialize
#ids.system.setInitMode(1)

#setup measurement
#ids.system.startMeasurement()

wait = 1
minVolt = -20
maxVolt = 110
voltstepsize = 10
voltage = np.arange(minVolt, maxVolt+voltstepsize, voltstepsize, dtype=np.int64)
lenVolt = len(voltage)

print(voltages)
# ins_kth2450.write("*RST")
# ins_kth2450.write("SENS:FUNC CURR")
# ins_kth2450.write("SENS:CURR:RANG:AUTO ON")
# ins_kth2450.write("SENS:CURR:UNIT AMP")
# ins_kth2450.write("SENS:CURR:OCOM ON")
# ins_kth2450.write("SOUR:FUNC VOLT")
# ins_kth2450.write("SOUR:VOLT 5")
# ins_kth2450.write("SOUR:VOLT:RANG 50")
# ins_kth2450.write("SOUR:VOLT:ILIM 1e-3")
# ins_kth2450.write(":INIT:CONT")
    #ins_kth2450.write("SENS:FUNC 'CURR'")
    #ins_kth2450.write("SENS:CURR:RANG 150e-6")

sourcemeter.reset()
sourcemeter.apply_voltage()
sourcemeter.source_voltage_range = 60
sourcemeter.current_range = 0.05
sourcemeter.compliance_current = 0.05 #do not exceed 20 mA when in 200V range or you will get limited?
sourcemeter.source_voltage = 0
sourcemeter.measure_current()
time.sleep(0.1)



zeit = np.arange(0, 60, 1, dtype=np.int64)
data = np.zeros_like(voltages)
stdev = np.zeros_like(data)
data2 = np.zeros_like(voltages)
stdev2 = np.zeros_like(data)
i = 0
i2 = 0

while ids.system.getCurrentMode() != 'measurement running':
    print('waiting for ids')
    time.sleep(2)



#start measurement
#ins_kth2450.write("OUTP ON")
print("Starting Keithley measurement")

# for voltage in voltages:
#     #ins_kth2450.write(f"SOUR:VOLT {voltage}")
#     ins_kth2450.write(":SOUR:VOLT:LEV {}".format(voltage))
#     for j in range(10):
#         data[i] = ids.displacement.getAbsolutePosition(0)[1]
#         i = i + 1
#         time.sleep(wait)

sourcemeter.enable_source()

for voltage in voltages:
    sourcemeter.ramp_to_voltage(voltage)
    print(voltage)
    time.sleep(2)
    temp = np.zeros(1000, dtype=np.int64)
    for j in range(1000):
        temp[j] = ids.displacement.getAbsolutePosition(0)[1]
        #time.sleep(0.001)
    data[i] = np.average(temp)
    stdev[i] = np.std(temp)
    i = i + 1

for voltage in reversed(voltages):
    sourcemeter.ramp_to_voltage(voltage)
    print(voltage)
    time.sleep(2)
    temp2 = np.zeros(1000, dtype=np.int64)
    for j in range(1000):
        temp2[j] = ids.displacement.getAbsolutePosition(0)[1]
        #time.sleep(0.001)
    data2[i2] = np.average(temp2)
    stdev2[i2] = np.std(temp2)
    i2 = i2 + 1

#stop devices
#ids.system.stopMeasurement()
#ins_kth2450.write("OUTP OFF")
#time.sleep(2)
#ids.close()
sourcemeter.ramp_to_voltage(0)
time.sleep(5)
sourcemeter.shutdown()
#ins_kth2450.close()


#plotting
# av = np.average(data)
# data = data - av
revvoltages = voltages[::-1]
# print(stdev)
# print(stdev2)
# plt.plot(voltages, data)
# plt.plot(revvoltages, data2)
offset = data[0]
data = data - offset
data2 = data2 - offset
np.savetxt('changealso.csv', (voltages,data,stdev,revvoltages,data2,stdev2), delimiter=',', header='voltages,datarampup,stdrampup,reversedvoltages,datarampdown,stdrampdown')
plt.errorbar(voltages, data, yerr=stdev, ls='--', marker='+', capsize=5, capthick=1, label='Ramp Up')
plt.errorbar(revvoltages, data2, yerr=stdev2, ls='--', marker='+', capsize=5, capthick=1, label='Ramp Down')
plt.title('Hysterisis of 3-Stack Thorlabs Piezo')
plt.xlabel('Applied Voltage [V]')
plt.ylabel('Change in Position of IDS [pm]')
plt.legend()
plt.savefig('changename.pdf', dpi=300)
plt.show()





#print(ids.displacement.getMeasurementEnabled())
# ids.pilotlaser.enable()
# time.sleep(5)
# ids.pilotlaser.disable()
#ids.system.startMeasurement()
# ids.system.startMeasurement()
# time.sleep(2)
#print(ids.system.getCurrentMode())
#print(ids.system_service.errorNumberToString(1, 0))

#print(ids.displacement.getAbsolutePosition(0)[1])
#print(ids.system_service.errorNumberToString(0, 2086))

#print(ids.system.getCurrentMode())




