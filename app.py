import streamlit as st


if "correos" not in st.session_state:
    st.session_state.correos = []

# Captura parámetros de la URL 
query_params = st.query_params
correo = query_params.get("correo", "")

# Si el enlace tiene un correo, lo guarda
if correo and correo not in st.session_state.correos:
    st.session_state.correos.append(correo)
    st.write(f"¡Gracias {correo}! Tu clic ha sido registrado.")
else:
    st.write("Bienvenido al registro de clics.")

# Visualización en tiempo real
st.write("### Correos que han hecho clic:")
for c in st.session_state.correos:
    st.write("- ", c)
