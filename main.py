from machine import Pin, lightsleep
import machine
import time
import network
import urequests
import json
import secrets

wake_up_pin = machine.Pin(15, machine.Pin.IN, machine.Pin.PULL_UP)
wake_up_pin.irq(trigger=machine.Pin.IRQ_FALLING, handler=None)
sensor_power = machine.Pin(16, machine.Pin.OUT)

#####################################
# wifi
wlan = network.WLAN(network.STA_IF)

def connect_wifi():
    for attempt in range(5):
        print(f"WiFi接続試行 {attempt + 1}/5")
        wlan.active(False)
        time.sleep_ms(300)  # チップのリセット待ち
        wlan.active(True)
        time.sleep_ms(300)  # スキャン開始を待つ
        wlan.connect(secrets.SSID, secrets.PW)
        
        for i in range(30):
            if wlan.isconnected():
                print(wlan.ifconfig()[0])
                return True
            time.sleep(1)
        
        print(f"タイムアウト (status: {wlan.status()})")
    
    print("WiFi接続失敗")
    return False

def send_slack(text):
    print("slack送信開始:" + text)
    if not connect_wifi():
        return
    data = {"text": text}
    payload = json.dumps(data).encode('utf-8')
    headers = {"Content-Type": "application/json"}
    try:
        response = urequests.post(secrets.WEBHOOK_URL, data=payload, headers=headers)
        print("Response:", response.status_code)
        print("Response Body:", response.text)
        response.close()
    except Exception as e:
        print("Error:", e)
    finally:
        wlan.active(False)
        wlan.deinit()
        print("送信完了")

def detectrain(want):
    while True:
        sensor_power.value(1)
        time.sleep_ms(100)
        
        value1 = wake_up_pin.value()
        if value1 != want:
            sensor_power.value(0)
            return value1
            
        machine.lightsleep(500)
        value2 = wake_up_pin.value()
        machine.lightsleep(500)
        value3 = wake_up_pin.value()
        
        sensor_power.value(0)
        if value1 == value2 == value3:
            return value1
        time.sleep(60)
        # 1=雨なし、0=雨あり（センサー出力は逆）

#####################################
#起動時はここから実行
send_slack("RainDetectionが起動しました！")

while True:
    print("*待機中* 雨が降るのを待っています")
    while detectrain(0) == 1:
        machine.lightsleep(60000)

    send_slack("☔☔☔雨が降ってきました！☔☔☔")
    print("*待機中* 雨が止むのを待っています")

    while detectrain(1) == 0:
        machine.lightsleep(60000)

    send_slack("⛅️雨がやみました……")