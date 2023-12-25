#
# Multi Air Sensor board Sample Program
#
# Copyright(C) 2023. fireflake,inc.
#

from machine import Pin, I2C, UART, WDT
import utime
import conf
from oled import Oled
from lps25hb import Lps25hb
from mhz19c import Mhz19c
from dht20 import Dht20

# global変数を宣言
led_pico = None              # Pico W本体のLED
led1 = None                  # マルチエアーセンサーボード上のLED
led2 = None                  # マルチエアーセンサーボード上のLED
led3 = None                  # マルチエアーセンサーボード上のLED
sw = None                    # マルチエアーセンサーボード上のタクトスイッチ
i2c = None                   # I2Cのインスタンス
oled = None                  # OLEDのインスタンス
mhz19c = None                # MH-Z19Cのインスタンス
lps25hb = None               # LPS25HBのインスタンス
dht20 = None                 # DHT20のインスタンス
wdt = None                   # ウォッチドッグタイマのインスタンス
debug_mode = False           # デバッグモードフラグ
sw_release_flag = False      # タクトスイッチが押された後離された際に True になるフラグ
ref_sw_on_time = 0           # タクトスイッチが押された時刻
ref_sw_off_time = 0          # タクトスイッチが押され終わった時刻

# Wathcdog Timer対応 sleep関数
# sleep中でもfeedしてWDTを実行させない
def sleep_with_feed(sec):
    global debug_mode, wdt
    for i in range(sec):
        if debug_mode == False and wdt != None:
            wdt.feed()
        utime.sleep(1)

# 復旧不可能な致命的なエラー発生時のエラーハンドラ
def fatal_err(err_msg):
    global led1, sw
    global debug_mode

    # Error を Log に出力
    print('Fatal err occured:' +str(err_msg))

    # OLEDに出せたら OLED にもエラーを表示(ベストエフォート）
    oled.show_data('Fatal err occur', str(err_msg))
    utime.sleep(5)

    # エラーの時の対応
    # Debug Mode OFF
    #    再起動で復旧を試みます
    # Debug Mode ON
    #    無限ループでLED 点滅。タクトスイッチが押された場合にはハードウェアリセット
    if debug_mode:
        while True:
            led1.on()
            utime.sleep_ms(500)
            led1.off()
            utime.sleep_ms(500)
            if sw.value() is 0:
                machine.reset()
    else:
        machine.reset()  # 再起動する 

# OLED表示とprintを同時に行う
def show_text(line1='', line2='', line3='', line4=''):
    global oled
    print(line1, line2, line3, line4)
    oled.show_data(line1, line2, line3, line4)

# 稼働中にタクトスイッチが押された・離された時の処理
def sw_callback(arg):
    # 長押し対応処理
    global sw_release_flag, ref_sw_on_time, ref_sw_off_time

    # SWが押されたら時の処理
    if sw.value() is 0:
        print('Sw Pressed')
        ref_sw_on_time = utime.ticks_ms()   # SW が押された時刻を取得

    # SWが押されたら時の処理
    if sw.value() is 1:
        print('Sw Released')
        ref_sw_off_time = utime.ticks_ms()  # SW が離された時刻を取得
        sw_release_flag = True              # スイッチが離されたフラグを立てる

def get_and_show_sensor_data():
    global led3
    global dht20, lps25hb, mhz19c
    try:
        # センサーからデータ取得
        temp, humid = dht20.read_temp_humid()
        temp = '{:.1f}C'.format(temp)
        humid = '{:.1f}%'.format(humid)
        press = '{:.0f}hPa'.format(lps25hb.read_press())
        co2 = '{:.0f}ppm'.format(mhz19c.read_co2())

        # 取得したデータをOLEDに表示させる
        show_text('Temp:  ' + temp, 'Humid: ' + humid, 'Press: ' + press, 'CO2:   ' + co2)

        # 一瞬だけLEDを点滅させる
        led3.on()
        utime.sleep_ms(50)
        led3.off()
    except Exception as e:
        fatal_err(e)

def main():    
    global led_pico, led1, led2, led3
    global i2c
    global oled
    global mhz19c, lps25hb, dht20
    global sw
    global debug_mode
    global wdt
    global ref_sw_on_time, ref_sw_off_time
    global sw_release_flag

    #初期化フェーズは debug mode 相当で動作（致命傷があっても再起動せずにエラー表示して停止）
    debug_mode = True

    # Pico W本体およびマルチエアーセンサーボード上のLEDのGPIO初期化
    led_pico = Pin(conf.GPIO_LED, Pin.OUT, value=0)
    led1 = Pin(conf.GPIO_11, Pin.OUT, value=0)  # LED1
    led2 = Pin(conf.GPIO_12, Pin.OUT, value=0)  # LED2
    led3 = Pin(conf.GPIO_13, Pin.OUT, value=0)  # LED3
    
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

    # I2C 接続の OLEDのインスタンス生成
    # インスタンス生成時の動作チェックに失敗したらfatal errorとして処理
    try:
        oled = Oled(i2c)
        show_text('Welcome...')
        utime.sleep(1)
    except Exception as e:
        fatal_err(e)

    # センサーのインスタンス生成
    # インスタンス生成時の動作チェックに失敗したらfatal errorとして処理
    try:
        dht20 = Dht20(i2c)
        lps25hb = Lps25hb(i2c)
        # CO2 Sensero
        mhz19c = Mhz19c(uart)
        mhz19c.turn_off_auto_calibration()   # 自動キャリブレーションをOFF
    except Exception as e:
        fatal_err(e)


    # 初期化フェーズが終わったので Debug Modeは一旦ここで終了
    debug_mode = False

    # 起動時にタクトスイッチが押されているかチェック
    # 押されていたらデバッグモードとして動作する。
    # Debug Mode では watchdog タイマーが無効化されるため開発中に breakpoint で止まった際に
    # リセットがかからないといった問題を回避できます。
    if sw.value() is 0:
        debug_mode = True
        show_text('debug mode', 'Enabled', 'WDT Disabled')
        utime.sleep(5)
        while sw.value() == 0:
            pass

    # タクトスイッチが押された際に呼び出される割り込みハンドラの設定
    sw_release_flag = False
    sw.irq(sw_callback, trigger=Pin.IRQ_RISING|Pin.IRQ_FALLING)
    
    # デバッグモードでなければWDTをセット
    wdt = None if debug_mode else WDT(timeout=8000)

    counter = 0
    while True:
        counter = counter +1

        # LOOP_WAIT で設定された時間間隔でセンサーデータをサンプリング
        if counter  % conf.LOOP_WAIT == 0:
            get_and_show_sensor_data()

        # キーをチェック。押したキーが離されたときに sw_release_flag が True になるので
        # 押された時間を計算、５秒間以上押されて長押しになっている場合に長押しの処理を実施
        if sw_release_flag :
            print('checking sw intervals')
            # タクトスイッチが5秒以上長押しされたらMH-Z19Cの自動キャリブレーションをONにする
            if utime.ticks_diff(ref_sw_off_time, ref_sw_on_time) >= 5000:
                print('long press enabled')
                mhz19c.turn_on_auto_calibration()
                show_text('CO2 auto', 'calibration on')
                sleep_with_feed(1)
            # SW が離された処理が終わったのでフラグをクリア
            sw_release_flag = False

        # 次の周期まで sleep
        sleep_with_feed(1)

if __name__ == "__main__":
    main()
