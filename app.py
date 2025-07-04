import streamlit as st
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime

# Configuración del correo de notificación
sender_email = "notificacionesticsimonbolivar@gmail.com"
password = "tvva tbwn hpjn lvwz"
receiver_email = "tic3@repuestossimonbolivar.com"

# 📤 Función para enviar correo HTML de notificación
def enviar_notificacion_html(correo_persona, fecha_hora):
    subject = "🔔 Nuevo clic registrado"

    # Contenido en HTML
    body = f"""
    <html>
    <body>
        <h3>🔔 Nuevo clic detectado</h3>
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

# 📥 Captura el parámetro 'correo' de la URL
query_params = st.query_params
correo = query_params.get("correo", "")

# 📝 Guarda los clics en memoria
if "clics" not in st.session_state:
    st.session_state.clics = []

# 🛡️ Lógica principal
if correo:
    fecha_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # Guarda el clic
    st.session_state.clics.append(f"{fecha_hora} - {correo}")
    st.write(f"¡Gracias {correo}! Tu clic ha sido registrado el {fecha_hora}.")
    # Envía el correo de notificación
    enviar_notificacion_html(correo, fecha_hora)
else:
    st.write("Bienvenido, pero no detectamos tu correo en el enlace.")

# 📃 Mostrar historial de clics
st.write("### Historial de clics registrados:")
for registro in st.session_state.clics:
    st.write("- ", registro)
