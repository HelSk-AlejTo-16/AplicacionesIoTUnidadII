import network
import time
from machine import Pin
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
        print('Conectando a la red Wi-Fi...')
        wlan.connect(wifi_ssid, wifi_password)
        while not wlan.isconnected():
            time.sleep(1)
    print('Conexión Wi-Fi exitosa:', wlan.ifconfig())

# Configuración del sensor KY-010
SENSOR_PIN = Pin(15, Pin.IN, Pin.PULL_UP)  # Sensor de objeto
LED_PIN = Pin(2, Pin.OUT)  # LED indicador

# Conexión MQTT
def connect_mqtt():
    try:
        client = MQTTClient("ky010_sensor_client", mqtt_broker, mqtt_port)
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
        sensor_value = SENSOR_PIN.value()  # Leer estado del sensor (1 = objeto detectado)
        
        # Encender o apagar LED según la detección
        if sensor_value == 1:
            print("Objeto detectado")
            LED_PIN.on()
        else:
            LED_PIN.off()

        # Si el valor ha cambiado, publicamos el mensaje
        if sensor_value != last_value:  # Solo enviar si hay un cambio
            client.publish(mqtt_topic, str(sensor_value))  # Enviar como entero convertido a string
            print("Datos enviados:", sensor_value)
            return sensor_value  # Guardar nuevo estado
        
        return last_value
    except Exception as e:
        print("Error al leer el sensor o enviar datos:", e)
        return last_value

# Main
connect_wifi()
client = connect_mqtt()

last_value = None  # Inicializar como None (sin valor previo)

while True:
    last_value = publish_data(client, last_value)
    time.sleep(0.1)  # Pequeño delay para evitar lecturas excesivas
