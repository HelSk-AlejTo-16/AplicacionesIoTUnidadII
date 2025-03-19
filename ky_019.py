import network
import time
import machine
import ubinascii
from umqtt.simple import MQTTClient

# Configuración WiFi
SSID = "vivoQR"
PASSWORD = "73hgj3jg"

# Configuración MQTT
MQTT_BROKER = "192.168.36.212"
MQTT_PORT = 1883
MQTT_TOPIC = "utng/relay"
MQTT_CLIENT_ID = ubinascii.hexlify(machine.unique_id()).decode()

# Configurar el relé
RELAY_PIN = machine.Pin(5, machine.Pin.OUT)
RELAY_PIN.value(0)  # Apagar relé al inicio

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

# Callback cuando se recibe un mensaje MQTT
def callback_mqtt(topic, msg):
    mensaje = msg.decode()
    print(f"Mensaje recibido: {mensaje}")

    if mensaje == "ON":
        RELAY_PIN.value(1)  # Encender relé
        print("✅ Relay encendido")
    elif mensaje == "OFF":
        RELAY_PIN.value(0)  # Apagar relé
        print("❌ Relay apagado")

# Conectar a MQTT
def conectar_mqtt():
    client = MQTTClient(MQTT_CLIENT_ID, MQTT_BROKER, MQTT_PORT)
    client.set_callback(callback_mqtt)
    client.connect()
    client.subscribe(MQTT_TOPIC)
    print("Conectado a MQTT y suscrito a:", MQTT_TOPIC)
    return client

# Inicializar conexión
conectar_wifi()
mqtt_client = conectar_mqtt()

while True:
    mqtt_client.check_msg()  # Escuchar mensajes MQTT
    time.sleep(0.5)
