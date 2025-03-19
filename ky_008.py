import network
import time
from machine import Pin
from umqtt.simple import MQTTClient

# Configuración de la red Wi-Fi
wifi_ssid = "vivoQR"  # Cambia por tu SSID
wifi_password = "73hgj3jg"  # Cambia por tu contraseña

# Configuración del broker MQTT
mqtt_broker = "192.168.36.212"  # Dirección del broker MQTT
mqtt_port = 1883
mqtt_topic_laser = "utng"  # Tema para el láser

# Configuración del pin del Láser KY-08
LASER_PIN = Pin(17, Pin.OUT)

# Conexión Wi-Fi
def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('Conectando a la red Wi-Fi...')
        wlan.connect(wifi_ssid, wifi_password)
        while not wlan.isconnected():
            time.sleep(1)
    print('Conexión Wi-Fi exitosa:', wlan.ifconfig())

# Conexión MQTT
def connect_mqtt():
    try:
        client = MQTTClient("esp32_ky08", mqtt_broker, mqtt_port)
        client.connect()
        print("Conectado al broker MQTT")
        return client
    except Exception as e:
        print("Error al conectar con MQTT:", e)
        return None

# Publicar estado en MQTT
def publish_status(client, topic, status):
    if client:
        try:
            client.publish(topic, status)
            print(f"MQTT Enviado [{topic}]: {status}")
        except Exception as e:
            print("Error al enviar mensaje MQTT:", e)

# Conectar Wi-Fi y MQTT
connect_wifi()
client = connect_mqtt()

while True:
    # Alternar Láser KY-08
    LASER_PIN.value(1)
    publish_status(client, mqtt_topic_laser, "1")
    time.sleep(1)

    LASER_PIN.value(0)
    publish_status(client, mqtt_topic_laser, "0")
    time.sleep(1)
