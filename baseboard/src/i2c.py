#
# Multi Air Sensor board Sample Program
#
# Copyright(C) 2023. fireflake,inc.
#

from machine import I2C, Pin
from micropython import const
import utime
from dht20 import Dht20

'''
1.このプログラムでDHT20を動かす際は、必ずベースボードのI2CコネクタにDHT20を接続してください。
2.このプログラムの動作には、dht20.pyが必要です。ff-pico-example/multiairsensors/src/dht20.py にあるので使ってください。
3.このプログラムからdht20.pyを読みこむ際は、dht20.pyの9行目の import conf をコメントアウトしてください。
'''

# ベースボードのI2Cチャンネルを設定
_SCL_PIN = const(5)
_SDA_PIN = const(4)
_I2C_FREQ = const(400_000)
_I2C_CHANNEL = const(0)
i2c = I2C(_I2C_CHANNEL, scl = Pin(_SCL_PIN), sda = Pin(_SDA_PIN), freq = _I2C_FREQ)

# DHT20のインスタンスを作成
dht20 = Dht20(i2c)

# 3秒ごとにDHT20の測定値をprint
while True:
    temp, humid = dht20.read_temp_humid()
    print('{:.2f}C'.format(temp), '{:.2f}%'.format(humid))
    utime.sleep(3)
