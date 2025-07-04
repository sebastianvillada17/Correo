# app.py

import streamlit as st
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime
import pytz  # pip install pytz

sender_email = "notificacionesticsimonbolivar@gmail.com"
mensaje_error = "tvva tbwn hpjn lvwz"
receiver_email = "tic3@repuestossimonbolivar.com"

#Función para enviar correo de notificación con formato HTML
def enviar_notificacion_html(correo_persona, fecha_hora):
    subject = "🔔 Nuevo clic registrado"

    # Cuerpo del mensaje en HTML
    body = f"""
    <html>
    <body>
        <h3>Nuevo clic detectado</h3>
        <p><strong>Correo:</strong> {correo_persona}</p>
        <p><strong>Fecha:</strong> {fecha_hora}</p>
    </body>
    </html>
    """

    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject
    message.attach(MIMEText(body, "html"))

    try:
        server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message.as_string())
        server.quit()
        st.success(f"Correo de notificación enviado por {correo_persona}")
    except Exception as e:
        st.error(f"Error al enviar correo: {e}")

# Captura el parámetro 'correo' de la URL
query_params = st.query_params
correo = query_params.get("correo", "")


zona_colombia = pytz.timezone('America/Bogota')
fecha_hora = datetime.now(zona_colombia).strftime("%Y-%m-%d %H:%M:%S")

# Guarda los clics en memoria
if "clics" not in st.session_state:
    st.session_state.clics = []

# Lógica principal
if correo:
    # Guarda el clic
    st.session_state.clics.append(f"{fecha_hora} - {correo}")
    st.write(f"¡Gracias {correo}! Tu clic ha sido registrado el {fecha_hora}.")
    # Enviar notificación
    enviar_notificacion_html(correo, fecha_hora)
else:
    st.write("Bienvenido, pero no detectamos tu correo en el enlace.")

# Mostrar historial
st.write("### Historial de clics registrados:")
for registro in st.session_state.clics:
    st.write("- ", registro)
