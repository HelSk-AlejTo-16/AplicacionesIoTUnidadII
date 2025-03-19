import network
import time
import machine
import onewire
import ds18x20
import ubinascii
from umqtt.simple import MQTTClient

# Configuración WiFi
SSID = "vivoQR"
PASSWORD = "73hgj3jg"

# Configuración MQTT
MQTT_BROKER = "192.168.36.212"
MQTT_PORT = 1883
MQTT_TOPIC = "utng"
MQTT_CLIENT_ID = ubinascii.hexlify(machine.unique_id()).decode()

# Conectar a WiFi
def conectar_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(SSID, PASSWORD)
    
    print("Conectando a WiFi...", end="")
    while not wlan.isconnected():
        time.sleep(1)
        print(".", end="")
    print("\nConectado a WiFi:", wlan.ifconfig())

# Conectar a MQTT
def conectar_mqtt():
    client = MQTTClient(MQTT_CLIENT_ID, MQTT_BROKER, MQTT_PORT)
    client.connect()
    print("Conectado al broker MQTT:", MQTT_BROKER)
    return client

# Configurar sensor DS18B20
pin = machine.Pin(4)
ow = onewire.OneWire(pin)
ds = ds18x20.DS18X20(ow)
roms = ds.scan()

# Inicializar conexión
conectar_wifi()
mqtt_client = conectar_mqtt()

while True:
    ds.convert_temp()
    time.sleep(1)
    
    for rom in roms:
        temp = ds.read_temp(rom)
        print("Temperatura:", temp, "°C")
        
        # Publicar en MQTT
        mqtt_client.publish(MQTT_TOPIC, str(temp))
        print(f"Publicado en {MQTT_TOPIC}: {temp} °C")
    
    time.sleep(5)  # Espera 5 segundos antes de la siguiente medición
