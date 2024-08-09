import IDS
import time
import matplotlib.pyplot as plt
import numpy as np
import pyvisa
from pymeasure.instruments.keithley import Keithley2450

#connect ids
ids = IDS.Device('192.168.1.1')
ids.connect()
sourcemeter = Keithley2450("TCPIP::192.168.1.3::inst0::INSTR")

wait = 1

minVolt = -30
maxVolt = 120
voltstepsize = 10
voltage = np.arange(minVolt, maxVolt+voltstepsize, voltstepsize, dtype=np.int64)
#create a reversed array of voltage
voltageReverse = voltage[::-1]
#make an array that is 5x indentical copies of voltage and then voltage reversed appended after each other
voltageReverse2 = np.concatenate((voltage, voltageReverse), axis=None)
#do it 5x
voltages = np.tile(voltageReverse2, 10)

print(voltages)

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

while ids.system.getCurrentMode() != 'measurement running':
    print('waiting for ids')
    time.sleep(2)

#start measurement
print("Starting Keithley measurement")

sourcemeter.enable_source()

for voltage in voltages:
    sourcemeter.ramp_to_voltage(voltage)
    print(voltage)
    time.sleep(2)
    temp = np.zeros(1000, dtype=np.int64)
    for j in range(1000):
        temp[j] = ids.displacement.getAbsolutePosition(0)[1]
    data[i] = np.average(temp)
    stdev[i] = np.std(temp)
    i = i + 1

#stop devices
sourcemeter.ramp_to_voltage(0)
time.sleep(5)
sourcemeter.shutdown()


#plotting
offset = data[0]
data = data - offset
np.savetxt('changealso.csv', (voltages,data,stdev), delimiter=',', header='voltages,datarampup,stdrampup')
plt.errorbar(voltages, data, yerr=stdev, ls='--', marker='+', capsize=5, capthick=1, label='Ramp Up')
plt.title('Hysterisis of CLSZ1')
plt.xlabel('Applied Voltage [V]')
plt.ylabel('Change in Position of IDS [pm]')
plt.legend()
plt.savefig('changename.pdf', dpi=300)
plt.show()





