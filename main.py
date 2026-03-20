from machine import Pin
import time

# 起動確認
led = machine.Pin(25, machine.Pin.OUT)
led.value(1)
time.sleep(5)
led.value(0)

# Dormant Modeでスリープする。雨に反応して起動する。

# Wifi起動して通知

# スリープモードに戻り、10分おきに疎通確認

# 疎通が解除されたら