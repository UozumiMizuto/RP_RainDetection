from machine import Pin
import machine
import time
import utime
import network
import slack_sdk

# require "Pico W"
SSID = 'SSID'
PW = 'Password'

# Require SlackAPI https://qiita.com/odm_knpr0122/items/04c342ec8d9fe85e0fe9
# xoxb-xxxxxxxxxxxxx-xxxxxxxxxxxxxx-xxxxxxxxxxxxxxxxxxxxxxxx
Token = 'Token'
Channel = '#general'

# wifi接続確認＆起動通知
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(SSID, PW)

while wlan.isconnected() == False:
    client = slack_sdk.WebClient(Token)
    client.chat_postMessage(Channel, text="RainDetectionが起動しました")

# 起動LED
led = machine.Pin(25, machine.Pin.OUT)
led.value(1)
time.sleep(5)
led.value(0)


while True:
# Dormant Modeでスリープする。雨に反応して起動する。
    
# Wifi起動して通知
    
# wifi解除
    
# lightsleepに入り、10分おきに疎通確認。
    
# 疎通が解除されたら

end