import streamlit as st
import os
from langchain_google_genai import ChatGoogleGenerativeAI

# Configuración de la página
st.set_page_config(page_title="Ventas La Vitela", page_icon="🌲", layout="centered")

st.title("🌲 Asesor Inmobiliario - La Vitela")
st.caption("Pátzcuaro, Michoacán — Información de fracciones rústicas y financiamiento")

if st.button("🗑️ Limpiar Pantalla", use_container_width=True):
    st.session_state.mensajes = []
    st.rerun()

# Cargar llave de Google
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY", "")
if not GOOGLE_API_KEY:
    try:
        GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]
    except Exception:
        pass

if not GOOGLE_API_KEY:
    st.warning("⚠️ Configura GOOGLE_API_KEY en los Secrets de Streamlit.")
    st.stop()

# Cargar el modelo
@st.cache_resource
def cargar_cerebro():
    return ChatGoogleGenerativeAI(
        google_api_key=GOOGLE_API_KEY,
        model="gemini-3.8-flash",
        temperature=0.3 # Un poco más creativo para ventas
    )

llm = cargar_cerebro()

if "mensajes" not in st.session_state:
    st.session_state.mensajes = [{"rol": "assistant", "contenido": "¡Hola! Soy el asesor virtual del proyecto La Vitela en Pátzcuaro. ¿Te interesa información sobre pagos de contado o nuestro plan de financiamiento con $5,000 de enganche?"}]

# Mostrar historial
for msg in st.session_state.mensajes:
    with st.chat_message(msg["rol"]):
        st.markdown(msg["contenido"])

# Input del usuario
consulta = st.chat_input("Escribe tu duda aquí (ej. ¿Dónde están ubicados? ¿Cómo es el contrato?)...")

if consulta:
    # Agregar mensaje del usuario
    st.session_state.mensajes.append({"rol": "user", "contenido": consulta})
    with st.chat_message("user"):
        st.markdown(consulta)

    with st.chat_message("assistant"):
        with st.spinner("Analizando opciones..."):
            try:
                # EL CEREBRO DEL VENDEDOR (PROMPT MAESTRO)
                prompt_ventas = f"""Actúa como un Asesor Inmobiliario Senior y Especialista en Derecho Agrario de Pátzcuaro.
Tu objetivo es perfilar, informar y cerrar ventas de las fracciones del proyecto "La Vitela", transmitiendo total confianza legal y cero presión.

REGLAS DE ORO (ESCUDO LEGAL - INQUEBRANTABLES):
1. JAMÁS uses la palabra "fraccionamiento" ni "lotes" a secas. Usa ÚNICAMENTE "fracciones", "fracciones rústicas" o "lotes campestres".
2. El esquema legal de venta es estrictamente mediante un "Contrato Privado de Compraventa con Reserva de Dominio".

FICHA TÉCNICA DEL PROYECTO "LA VITELA":
- Ubicación: La Vitela, Pátzcuaro, Michoacán (a un costado de la escuela primaria).
- Accesos: Colinda por un lado con carretera y por el otro con camino de terracería.
- Agua: El servicio de agua será mediante un tanque vecinal (actualmente en proceso de construcción).
- Medidas: 200 m² por fracción (Ad Corpus).
- Disponibilidad: Proyecto de 121 fracciones. 10 ya están vendidas (y financiadas). Quedan 111 fracciones rústicas disponibles.

ESQUEMA DE PRECIOS:
- Precio de Contado: $200,000 MXN.
- Plan de Financiamiento Directo: 
  * Enganche: $5,000 MXN.
  * Mensualidades: $2,500 MXN.
  (El sistema debe calcular automáticamente que faltan $195,000 por pagar, lo que equivale a 78 mensualidades de $2,500).

INSTRUCCIONES DE RESPUESTA:
- Sé amable, persuasivo, claro y directo.
- Si preguntan por la certeza legal, explica la seguridad del Contrato Privado con Reserva de Dominio.
- Si preguntan por servicios, sé honesto: es un proyecto rústico campestre, el tanque vecinal de agua está por construirse.
- Responde siempre a la consulta del cliente de forma natural, sin parecer un robot.

Historial de la conversación:
{st.session_state.mensajes[-3:]} # Solo recordamos los últimos 3 mensajes para mantener contexto

Consulta actual del cliente: {consulta}
Respuesta del Asesor:"""
                
                respuesta_cruda = llm.invoke(prompt_ventas).content
                if isinstance(respuesta_cruda, list):
                    respuesta = respuesta_cruda[0]["text"]
                else:
                    respuesta = respuesta_cruda
                    
                st.markdown(respuesta)
                st.session_state.mensajes.append({"rol": "assistant", "contenido": respuesta})

            except Exception as e:
                st.error(f"Error en el sistema: {e}")