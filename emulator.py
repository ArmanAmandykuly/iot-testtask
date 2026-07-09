import paho.mqtt.client as mqtt
import json
import time
import random

# Настройки
TOKEN = "bfdLtMaUOJN9PpyjCNRC"
BROKER = "localhost"

# Состояние установки
state = {
    "temp_outside": 15.0,
    "temp_supply": 20.0,
    "setpoint": 22.0,
    "filter_clog": 0.0,
    "fan_speed": 50,
    "status": "RUN"
}

client = mqtt.Client()
client.username_pw_set(TOKEN)
client.connect(BROKER, 1883, 60)


print("Эмулятор запущен. Отправка данных...")

try:
    while True:
        # 1. Наружная температура "гуляет" вокруг 15 градусов
        state["temp_outside"] += random.uniform(-0.2, 0.2)
        
        # 2. Температура притока плавно стремится к уставке + добавляем шум датчика
        diff = state["setpoint"] - state["temp_supply"]
        state["temp_supply"] += (diff * 0.1) + random.uniform(-0.1, 0.1)
        
        # 3. Фильтр засоряется
        state["filter_clog"] = min(state["filter_clog"] + 0.05, 100.0)

        if random.random() < 0.01:
            jump = random.randint(30, 60)
            state["filter_clog"] = min(state["filter_clog"] + jump, 100.0)
            print(f"!!! ALERT: Sudden filter clog increase by {jump}% !!!")
            state["total_alarms"] += 1
        
        # 4. Скорость вентилятора с небольшим "дрожанием"
        state["fan_speed"] = 50 + random.randint(-2, 2)
        
        client.publish('v1/devices/me/telemetry', json.dumps(state))
        print(f"Отправлено: {state}")
        time.sleep(2)
except KeyboardInterrupt:
    print("Эмулятор остановлен.")
    client.disconnect()