# app.py

import streamlit as st
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime
import pytz  # pip install pytz
import base64

sender_email = "notificacionesticsimonbolivar@gmail.com"
password = "tvva tbwn hpjn lvwz"
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
st.title("Campaña: Correo sospechoso, empresa segura")
if correo:
    # Guarda el clic y envía la notificación solo una vez por sesión
    if "clic_registrado" not in st.session_state:
        st.session_state.clics.append(f"{fecha_hora} - {correo}")
        enviar_notificacion_html(correo, fecha_hora)
        st.session_state.clic_registrado = True
else:
    st.write("Bienvenido, pero no detectamos tu correo en el enlace.")

# Mensaje de campaña 
st.write(f"Estamos haciendo una campaña de ciberseguridad. Acabas de hacer clic en el enlace de un correo que te enviamos, no hagas clic en enlaces sospechosos. esto pone en riesgo la seguridad de tu información y la de la empresa. Si tienes dudas, contacta al departamento de TI.")
st.write("Lee la siguiente informacion para mas detalles y realiza el cuestionario, recuerda que la seguridad de la empresa depende de todos nosotros.")

# Muestra pdf
st.write("### Información de Ciberseguridad")

with open("doc/Correo_Sospechoso_Empresa_Segura.pdf", "rb") as f:
    pdf_bytes = f.read()
    b64_pdf = base64.b64encode(pdf_bytes).decode()

href = f'<a href="data:application/pdf;base64,{b64_pdf}" download="Correo_Sospechoso_Empresa_Segura.pdf" target="_blank">Haz clic aquí para descargar el PDF</a>'
st.markdown(href, unsafe_allow_html=True)

