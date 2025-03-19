import network
import time
from machine import Pin, PWM
from umqtt.simple import MQTTClient

# Configuración de la red Wi-Fi
wifi_ssid = "vivoQR"  # Cambia por tu SSID
wifi_password = "73hgj3jg"  # Cambia por tu contraseña

# Configuración del broker MQTT
mqtt_broker = "192.168.36.212"  # Nueva IP del broker
mqtt_port = 1883
mqtt_topic = "utng"  # Nuevo tema

# Conexión Wi-Fi
def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print("Conectando a la red Wi-Fi...")
        wlan.connect(wifi_ssid, wifi_password)
        retries = 0
        while not wlan.isconnected() and retries < 10:
            time.sleep(1)
            retries += 1
            print(f"Reintentando conexión Wi-Fi... {retries}/10")
        if retries == 10:
            print("No se pudo conectar a Wi-Fi después de varios intentos")
        else:
            print("Conexión Wi-Fi exitosa:", wlan.ifconfig())

def connect_mqtt():
    try:
        client = MQTTClient("ky006_buzzer_client", mqtt_broker, mqtt_port)
        client.connect()
        print("Conectado al broker MQTT")
        return client
    except Exception as e:
        print("Error al conectar con MQTT:", e)
        return None

# Configuración del sensor KY-006 (Buzzer pasivo)
BUZZER_PIN = Pin(18, Pin.OUT)
PWM_BUZZER = PWM(BUZZER_PIN)
PWM_BUZZER.freq(1000)  # Frecuencia inicial

# Función para enviar mensajes al broker MQTT
def send_mqtt_message(client, message):
    try:
        client.publish(mqtt_topic, message)
        print(f"Mensaje enviado al broker: {message}")
    except Exception as e:
        print(f"Error al enviar mensaje MQTT: {e}")

# Función para encender y apagar el buzzer con ciclo
def buzzer_cycle(client):
    while True:
        # Encender el buzzer
        PWM_BUZZER.duty(512)  # Encender buzzer (a la mitad de su capacidad)
        print("Buzzer ENCENDIDO")
        send_mqtt_message(client, "1")  # Enviar mensaje "1" al broker
        time.sleep(5)  # Mantener encendido por 5 segundos

        # Apagar el buzzer
        PWM_BUZZER.duty(0)  # Apagar buzzer
        print("Buzzer APAGADO")
        send_mqtt_message(client, "0")  # Enviar mensaje "0" al broker
        time.sleep(5)  # Mantener apagado por 5 segundos

# Main
connect_wifi()
client = connect_mqtt()
if client:
    buzzer_cycle(client)  # Llamamos a la función que maneja el ciclo de buzzer
