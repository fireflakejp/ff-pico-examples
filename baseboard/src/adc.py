#
# Multi Air Sensor board Sample Program
#
# Copyright(C) 2023. fireflake,inc.
#

from machine import ADC, Pin
from micropython import const
import utime

# ベースボードのADCには、ADC0, ADC1を指定出来ます
_ADC_CH0 = const(0)
_ADC_CH1 = const(0)
adc0 = machine.ADC(_ADC_CH0)

# ADCから読みこんだ生の読み取り値を電圧変換するためのスケールを作っておく
_MAX_READ_VOLT = const(3.3) # Pico WのADCで読みこめる最大電圧
_RAW_SCALE = const(65535)  # Pico WのADCの分解能は12bitだが、ADC.read_u16()で読んだ生の値は0-65535にスケーリングされるので
volt_scale = _MAX_READ_VOLT / _RAW_SCALE

while True:
    raw = adc0.read_u16()  # 0.0v-3.3v範囲を0-65535の値で読込み
    volt = raw * volt_scale  # 生の読み取り値を電圧変換
    print('{:.6f}V'.format(volt))
    utime.sleep(3)
