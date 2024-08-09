import zwo_efw
from gpiozero import LED
from time import sleep
from signal import pause

#initialize Filter Wheel
efw = zwo_efw.EFW()
efw.initialize()

#initialize GPIO pin
#when using shutter, make sure that it's in external control
#press the "enable"-button until the light glows 2 times
led = LED(26)

led.on()

sleep(2)

led.off() #close


#get position of next spot in filterwheel
pos = efw.get_position()
print(pos)

if pos +1 ==6:
    pos=1
else:
    pos=pos+1

# set position
efw.set_position(pos)

sleep(2)

led.on() #open

#use timer to let it open
#sleep(10)

#either using pause to keep the scipt open
# close via ctrl + c
pause() 


#close "uninitiate" pin
#led.close()

#to run scipt in environment still use conda activate exp first