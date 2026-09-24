import os
import requests
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()


def obtener_clima(ciudad, api_key):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={ciudad}&appid={api_key}&lang=es&units=metric"

    try:
        respuesta = requests.get(url, timeout=10)

        if respuesta.status_code == 200:
            datos = respuesta.json()

            temperatura = datos["main"]["temp"]
            descripcion = datos["weather"][0]["description"]

            return temperatura, descripcion

        else:
            print(f"Error al obtener el clima. Código de estado: {respuesta.status_code}")
            return None

    except Exception as e:
        print(f"Error al realizar la solicitud: {e}")
        return None


def enviar_email(remitente, password, destinatario, asunto, contenido):

    mensaje = MIMEMultipart()

    mensaje["From"] = remitente
    mensaje["To"] = destinatario
    mensaje["Subject"] = asunto

    mensaje.attach(MIMEText(contenido, "plain", "utf-8"))

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.ehlo()
            server.starttls()
            server.login(remitente, password)

            server.sendmail(
                remitente,
                destinatario,
                mensaje.as_string()
            )

        print("✅ Correo enviado exitosamente.")

    except Exception as e:
        print(f"❌ Error al enviar el correo: {e}")


if __name__ == "__main__":

    API_KEY = os.getenv("API_KEY")
    CIUDAD = os.getenv("CIUDAD")
    CORREO_REMITENTE = os.getenv("CORREO_REMITENTE")
    CONTRASENA = os.getenv("CONTRASENA")
    CORREO_DESTINATARIO = os.getenv("CORREO_DESTINATARIO")

    missing = [
        n for n, v in [
            ("API_KEY", API_KEY),
            ("CIUDAD", CIUDAD),
            ("CORREO_REMITENTE", CORREO_REMITENTE),
            ("CONTRASENA", CONTRASENA),
            ("CORREO_DESTINATARIO", CORREO_DESTINATARIO)
        ] if not v
    ]

    if missing:
        print("Faltan variables de entorno:", ", ".join(missing))

    else:

        resultado_clima = obtener_clima(CIUDAD, API_KEY)

        if resultado_clima:

            temperatura, descripcion = resultado_clima

            contenido = f"""
Hola,

Este es un reporte automático del clima.

El clima actual en {CIUDAD.upper()} es:

Temperatura: {temperatura:.2f} °C
Descripción: {descripcion}

¡Que tengas un excelente día!

------------------------------
Correo generado automáticamente
Keiner Pedrozo
"""

            # Mostrar en terminal
            print("\n===================================")
            print(f"REPORTE DE CLIMA: {CIUDAD.upper()}")
            print("===================================")
            print(contenido)

            # Enviar correo
            enviar_email(
                CORREO_REMITENTE,
                CONTRASENA,
                CORREO_DESTINATARIO,
                f"Reporte de Clima: {CIUDAD.upper()}",
                contenido
            )

        else:
            print("No se pudo obtener la información del clima.")