#
# Multi Air Sensor board Sample Program
#
# Copyright(C) 2023. fireflake,inc.
#

from machine import Pin
import utime
from micropython import const

# ベースボードのフォトカプラの入力ピンには、GPIO6, GPIO7を指定出来ます
_GPIO_6 = const(6)
_GPIO_7 = const(7)
pin= Pin(_GPIO_6, Pin.OUT)
 
while True:
    pin.on()
    print('on')
    utime.sleep(3)
    pin.off()
    print('off')
    utime.sleep(3)
