#
# Multi Air Sensor board Sample Program
#
# Copyright(C) 2023. fireflake,inc.
#

# GPIO
GPIO_0 = const(0)
GPIO_1 = const(1)
GPIO_2 = const(2)
GPIO_3 = const(3)
GPIO_4 = const(4)
GPIO_5 = const(5)
GPIO_6 = const(6)
GPIO_7 = const(7)
GPIO_8 = const(8)
GPIO_9 = const(9)
GPIO_10 = const(10)
GPIO_11 = const(11)
GPIO_12 = const(12)
GPIO_13 = const(13)
GPIO_14 = const(14)
GPIO_15 = const(15)
GPIO_16 = const(16)
GPIO_17 = const(17)
GPIO_18 = const(18)
GPIO_19 = const(19)
GPIO_20 = const(20)
GPIO_21 = const(21)
GPIO_22 = const(22)
GPIO_26 = const(26)
GPIO_27 = const(27)
GPIO_28 = const(28)
GPIO_LED = const('LED')

# マルチエアーセンサーボード側のI2Cチャンネル
I2C1_CHANNEL = const(1)
I2C1_SCL_PIN = const(GPIO_3)
I2C1_SDA_PIN = const(GPIO_2)
I2C1_FREQ = const(400_000)

# マルチエアーセンサーボード側のUARTチャンネル
UART1_CHANNEL = const(1)
UART1_TX_PIN = const(GPIO_8)
UART1_RX_PIN = const(GPIO_9)
UART1_BAUDRATE = const(9_600)
UART1_BITS = const(8)
UART1_PARITYBIT = const(None)
UART1_STOPBIT = const(1)
UART1_TIMEOUT = const(10)

# メインループ関連
LOOP_WAIT = const(5)
