#
# Multi Air Sensor board Sample Program
#
# Copyright(C) 2023. fireflake,inc.
#

from machine import Pin
import utime
from micropython import const

# ベースボードのフォトカプラの入力ピンには、GPIO20, GPIO21を指定出来ます
_GPIO_20 = const(20)
_GPIO_21 = const(21)
pin= Pin(_GPIO_20, Pin.IN, machine.Pin.PULL_UP)

while True:
    print(pin.value())  # 入力があれば0、なければ1になる
    utime.sleep(3)
