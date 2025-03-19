import network
import time
from machine import Pin, PWM
from umqtt.simple import MQTTClient

# Configuración de la red Wi-Fi
wifi_ssid = "vivoQR"  # Cambia por tu SSID
wifi_password = "73hgj7jg"  # Cambia por tu contraseña

# Configuración del broker MQTT
mqtt_broker = "192.168.36.212"  # Nueva IP del broker
mqtt_port = 1883
mqtt_topic = "utng"  # Nuevo tema
# Conexión Wi-Fi
def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print("Conectando a la red Wi-Fi...")
        wlan.connect(wifi_ssid, wifi_password)
        while not wlan.isconnected():
            time.sleep(1)
    print("Conexión Wi-Fi exitosa:", wlan.ifconfig())

# Conexión MQTT
def connect_mqtt():
    try:
        client = MQTTClient("ky016_actuator_client", mqtt_broker, mqtt_port)
        client.connect()
        print("Conectado al broker MQTT")
        return client
    except Exception as e:
        print("Error al conectar con MQTT:", e)
        return None

# Configuración del actuador KY-016 (RGB LED)
RED_PIN = PWM(Pin(25), freq=1000)
GREEN_PIN = PWM(Pin(26), freq=1000)
BLUE_PIN = PWM(Pin(27), freq=1000)

def set_color(r, g, b):
    RED_PIN.duty(r)
    GREEN_PIN.duty(g)
    BLUE_PIN.duty(b)

# Programa principal
connect_wifi()
mqtt_client = connect_mqtt()

while True:
    # Color Rojo
    set_color(1023, 0, 0)
    if mqtt_client:
        mqtt_client.publish(mqtt_topic, str(1))
    print("Color configurado: Rojo")
    time.sleep(1)
    
    # Color Verde
    set_color(0, 1023, 0)
    if mqtt_client:
        mqtt_client.publish(mqtt_topic, str(2))
    print("Color configurado: Verde")
    time.sleep(1)
    
    # Color Azul
    set_color(0, 0, 1023)
    if mqtt_client:
        mqtt_client.publish(mqtt_topic, str(3))
    print("Color configurado: Azul")
    time.sleep(1)
