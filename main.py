from machine import Pin
import machine
import time
import utime
import network
import slack

import secrets

# wifi接続確認＆起動通知
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(secrets.SSID, secrets.PW)

while wlan.isconnected() == False:
    client = slack_sdk.WebClient(secrets.Token)
    client.chat_postMessage(secrets.Channel, text="RainDetectionが起動しました")

# 起動LED
led = machine.Pin(25, machine.Pin.OUT)
led.value(1)
time.sleep(5)
led.value(0)


while True:
# Dormant Modeでスリープする。雨に反応して起動する。
    led.value(1)
    time.sleep(5)
    led.value(0)
# Wifi起動して通知
    
# wifi解除
    
# lightsleepに入り、10分おきに疎通確認。
    
# 疎通が解除されたら

end