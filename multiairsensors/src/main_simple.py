#
# Multi Air Sensor board Sample Program
#
# Copyright(C) 2023. fireflake,inc.
#

from machine import Pin, I2C, UART
import utime
import conf
from oled import Oled
from lps25hb import Lps25hb
from mhz19c import Mhz19c
from dht20 import Dht20

def main():    

    # マルチエアーセンサーボード上のLEDのGPIO初期化
    led = Pin(conf.GPIO_13, Pin.OUT, value=0)  # LED3
    
    # タクトスイッチのピンを設定設定
    sw = Pin(conf.GPIO_10, Pin.IN, Pin.PULL_UP)

    # マルチエアーセンサーボード上のUARTチャンネルを設定
    uart = UART(conf.UART1_CHANNEL,
                baudrate=conf.UART1_BAUDRATE,
                tx = Pin(conf.UART1_TX_PIN),
                rx = Pin(conf.UART1_RX_PIN))
    
    # マルチエアーセンサーボード側のI2Cチャンネルを設定
    i2c = I2C(conf.I2C1_CHANNEL,
              scl = Pin(conf.I2C1_SCL_PIN),
              sda = Pin(conf.I2C1_SDA_PIN),
              freq = conf.I2C1_FREQ)

    oled = Oled(i2c)
    dht20 = Dht20(i2c)
    lps25hb = Lps25hb(i2c)
    mhz19c = Mhz19c(uart)

    while True:
        # センサーからデータ取得
        temp, humid = dht20.read_temp_humid()
        temp = '{:.1f}C'.format(temp)
        humid = '{:.1f}%'.format(humid)
        press = '{:.0f}hPa'.format(lps25hb.read_press())
        co2 = '{:.0f}ppm'.format(mhz19c.read_co2())

        # 取得したデータをOLEDに表示させる
        oled.show_data('Temp:  ' + temp, 'Humid: ' + humid, 'Press: ' + press, 'CO2:   ' + co2)
        print('Temp:  ' + temp, 'Humid: ' + humid, 'Press: ' + press, 'CO2:   ' + co2)

        # 一瞬だけLEDを点滅させる
        led.on()
        utime.sleep_ms(50)
        led.off()

        # 次の周期まで sleep
        utime.sleep(conf.LOOP_WAIT)

if __name__ == "__main__":
    main()
