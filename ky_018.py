import network
import machine
import time
from umqtt.simple import MQTTClient

# 📌 Configuración WiFi
WIFI_SSID = "vivoQR"
WIFI_PASSWORD = "72hgj3jg"

# 📌 Configuración MQTT
MQTT_BROKER = "192.168.36.212"  # Puedes usar otro broker
MQTT_PORT = 1883  # Puerto estándar sin TLS
MQTT_CLIENT_ID = "esp32_photoresistor"
MQTT_TOPIC = "utng"

# 📌 Configuración del ADC (fotorresistencia)
PHOTORESISTOR_PIN = 33  # GPIO 36 (ADC1_CH0)
adc = machine.ADC(machine.Pin(PHOTORESISTOR_PIN))
adc.atten(machine.ADC.ATTN_11DB)  # Rango de 0-3.3V

# 📌 Conectar WiFi
def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(WIFI_SSID, WIFI_PASSWORD)
    
    print("Conectando a WiFi...", end="")
    while not wlan.isconnected():
        time.sleep(1)
        print(".", end="")
    
    print("\nConectado a:", WIFI_SSID)
    print("IP:", wlan.ifconfig()[0])

# 📌 Conectar MQTT con puerto
def connect_mqtt():
    client = MQTTClient(MQTT_CLIENT_ID, MQTT_BROKER, port=MQTT_PORT)
    client.connect()
    print(f"Conectado al broker MQTT en {MQTT_BROKER}:{MQTT_PORT}")
    return client

# 📌 Programa principal
connect_wifi()
mqtt_client = connect_mqtt()

while True:
    light_intensity = adc.read()  # Leer fotorresistencia
    print("Light Intensity:", light_intensity)
    
    # Enviar datos al broker MQTT
    mqtt_client.publish(MQTT_TOPIC, str(light_intensity))
    
    time.sleep(2)  # Esperar 2 segundos antes de la próxima lectura

