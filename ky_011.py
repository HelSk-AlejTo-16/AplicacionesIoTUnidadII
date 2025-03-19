import network
import time
from machine import Pin
from umqtt.simple import MQTTClient

# Wi-Fi Configuration
wifi_ssid = "vivoQR"  # Change to your SSID
wifi_password = "73hgj3jg"  # Change to your password

# MQTT Broker Configuration
mqtt_broker = "192.168.36.212"  # Broker IP
mqtt_port = 1883
mqtt_topic = "utng"  # Topic for LED status

# KY-011 LED Pins
RED_PIN = Pin(21, Pin.OUT)
GREEN_PIN = Pin(19, Pin.OUT)

# Wi-Fi Connection
def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('Connecting to Wi-Fi...')
        wlan.connect(wifi_ssid, wifi_password)
        while not wlan.isconnected():
            time.sleep(1)
    print('Wi-Fi Connected:', wlan.ifconfig())

# MQTT Connection
def connect_mqtt():
    try:
        client = MQTTClient("ky011_led_client", mqtt_broker, mqtt_port)
        client.connect()
        print("Connected to MQTT Broker")
        return client
    except Exception as e:
        print("MQTT Connection Error:", e)
        return None

# Publish LED status to MQTT
def publish_status(client, status):
    if client:
        try:
            client.publish(mqtt_topic, status)
            print("MQTT Sent:", status)
        except Exception as e:
            print("Error sending MQTT message:", e)

# Main Program
connect_wifi()
client = connect_mqtt()

while True:
    RED_PIN.value(1)
    GREEN_PIN.value(0)
    publish_status(client, "1")
    time.sleep(3)

    RED_PIN.value(0)
    GREEN_PIN.value(1)
    publish_status(client, "2")
    time.sleep(3)
