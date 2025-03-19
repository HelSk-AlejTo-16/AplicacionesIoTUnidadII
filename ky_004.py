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

def connect_mqtt():
    try:
        client = MQTTClient("ky004_button_client", mqtt_broker, mqtt_port)
        client.connect()
        print("Conectado al broker MQTT")
        return client
    except Exception as e:
        print("Error al conectar con MQTT:", e)
        return None

# Configuración del sensor KY-004 (Botón)
BUTTON_PIN = Pin(4, Pin.IN, Pin.PULL_UP)  # Botón con pull-up interno
LED_PIN = Pin(2, Pin.OUT)                 # LED indicador

# Función para enviar datos por MQTT solo si hay un cambio de estado
def publish_button_state(client, last_state):
    if client is None:
        print("Cliente MQTT no disponible, reintentando conexión...")
        return last_state

    try:
        button_state = 1 if BUTTON_PIN.value() == 0 else 0  # 1 si presionado, 0 si no
        if button_state != last_state:  # Solo enviar si cambia el estado
            client.publish(mqtt_topic, str(button_state))  # Enviar INT como string
            print(f"Botón {'PRESIONADO' if button_state else 'LIBERADO'} - Estado enviado: {button_state}")
            return button_state
        return last_state
    except Exception as e:
        print("Error al leer el botón o enviar datos:", e)
        return last_state

# Main
connect_wifi()
client = connect_mqtt()

last_button_state = None  # Estado inicial del botón

while True:
    last_button_state = publish_button_state(client, last_button_state)

    # Encender LED si el botón está presionado
    if BUTTON_PIN.value() == 0:
        LED_PIN.on()
    else:
        LED_PIN.off()

    time.sleep(0.1)  # Pequeño delay para evitar lecturas excesivas
