import network
import time
from machine import Pin
from umqtt.simple import MQTTClient

# Configuración de la red Wi-Fi
wifi_ssid = "vivoQR"  # Cambia por tu SSID
wifi_password = "73hgj3jg"  # Cambia por tu contraseña

# Configuración del broker MQTT
mqtt_broker = "192.168.36.212"  # Nueva IP del broker
mqtt_port = 1883
mqtt_topic = "utng"  # Nuevo tema

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

# Configuración del sensor de choque
sensor = Pin(26, Pin.IN)

# Conexión MQTT
def connect_mqtt():
    try:
        client = MQTTClient("shock_sensor_client", mqtt_broker, mqtt_port)
        client.connect()
        print("Conectado al broker MQTT")
        return client
    except Exception as e:
        print("Error al conectar con MQTT:", e)
        return None

# Enviar datos solo si el valor del sensor cambia
def publish_data(client, last_value):
    if client is None:
        print("Cliente MQTT no disponible, reintentando conexión...")
        return last_value
    
    try:
        value = sensor.value()  # Leer el estado del sensor
        if value != last_value:  # Solo enviar si hay cambio
            payload = str(value)  # Convertir el valor a string
            client.publish(mqtt_topic, payload)
            print("Datos enviados:", payload)
            return value  # Guardar nuevo estado
        return last_value
    except Exception as e:
        print("Error al leer el sensor o enviar datos:", e)
        return last_value

# Main
connect_wifi()
client = connect_mqtt()

last_value = sensor.value()  # Obtener el estado inicial del sensor

while True:
    last_value = publish_data(client, last_value)
    time.sleep(0.1)  # Pequeño delay para evitar lecturas excesivas
