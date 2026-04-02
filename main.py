from machine import Pin
import machine
import time
import utime
import network
import urequests
import json

import secrets

# slack
def send_slack(text):
    data = {"text": text}
    payload = json.dumps(data).encode('utf-8')
    headers = {"Content-Type": "application/json"}
    print (secrets.WEBHOOK_URL)
    try:
        response = urequests.post(secrets.WEBHOOK_URL, data=payload, headers=headers)
        print("Response:", response.status_code)
        print("Response Body:",response.text)
        response.close()
    except Exception as e:
        print("Error:", e)
        
        
# wifi接続確認＆起動通知
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(secrets.SSID, secrets.PW)

while not wlan.isconnected():
    time.sleep(1)
    
send_slack("RainDetectionが起動しました")
status = wlan.ifconfig()
print(status[0])

# 起動LED
led = machine.Pin("LED", machine.Pin.OUT)
led.value(1)
time.sleep(5)
led.value(0)


while True:
    wlan.active(False)
    wlan.deinit()
    
    print("aaaa")
# 1. 起こしてくれるピンを指定（例：GP15）
    wake_up_pin = machine.Pin(15, machine.Pin.IN, machine.Pin.PULL_DOWN)
    wake_up_pin.irq(trigger=machine.Pin.IRQ_RISING, handler=None)

    print("おやすみなさい...")
# 3. 休止！
    machine.lightsleep()

# --- 15番ピンに電気が流れると、ここから再開 ---
    print("おはよう！")
    
    wlan.active(True)
    while not wlan.isconnected():
        time.sleep(1)
        
    send_slack("雨が降ってきました")

# Dormant Modeでスリープする。雨に反応して起動する。

# Wifi起動して通知
    
# wifi解除
    
# lightsleepに入り、10分おきに疎通確認。
    
# 疎通が解除されたら

end