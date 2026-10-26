import streamlit as st

# Configuración inicial de la página
st.set_page_config(
    page_title="Gestor de Catálogo y Tienda Melo's Beauty",
    page_icon="🌸",
    layout="wide"
)

# Definición de la variable por defecto para la imagen de fondo
MELO2_DEFAULT = "melo2.jpeg"  # Modifica esta ruta o URL según la ubicación de tu imagen

# Estilos CSS con sintaxis corregida para f-strings en Python.
# Se utilizan dobles llaves {{ y }} para los bloques de CSS y llaves simples {MELO2_DEFAULT} únicamente para la variable.
STYLING_CSS = f"""
<style>
/* Fondo general con marca de agua melo2.jpeg */
.stApp {{
    background: linear-gradient(rgba(255, 245, 247, 0.92), rgba(255, 245, 247, 0.92)), url("{MELO2_DEFAULT}") repeat center center fixed;
    background-size: cover;
    color: #2C2C2C;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}}

#MainMenu {{visibility: hidden;}}
footer {{visibility: hidden;}}
</style>
"""

# Inyección del código CSS en Streamlit
st.markdown(STYLING_CSS, unsafe_allow_html=True)

# Encabezado principal de la aplicación
st.title("🌸 Gestor de Catálogo y Tienda Melo's Beauty")
st.subheader("Catálogo de productos y gestión de tienda")
st.write("La aplicación se ha iniciado correctamente con los estilos estilizados.")
