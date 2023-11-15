from dotenv import load_dotenv
from streamlit_javascript import st_javascript
from textblob import TextBlob
import os
import re
import streamlit as st
import tweepy


st.set_page_config(page_title="Emotions Tweets", page_icon="assets/TwitterIcon.png")

load_dotenv()

API_KEY_TWITTER = os.getenv("API_KEY_TWITTER")
API_SECRET_KEY = os.getenv("API_SECRET_KEY")
BEARER_TOKEN = os.getenv("BEARER_TOKEN")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
ACCESS_TOKEN_SECRET = os.getenv("ACCESS_TOKEN_SECRET")


def traducir_texto(texto, idioma_origen, idioma_destino):
    blob = TextBlob(texto)

    texto_traducido = blob.translate(from_lang=idioma_origen, to=idioma_destino)

    return str(texto_traducido)


st.markdown(
    """
<style>
h1, h2, h3, h4, h5, h6 {
    font-size: 30px;
    font-weight: bold;
}
</style>
""",
    unsafe_allow_html=True,
)


class ConexionTwitter:
    def __init__(self):
        self.auth = tweepy.OAuthHandler(API_KEY_TWITTER, API_SECRET_KEY)
        self.auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
        self.api = tweepy.API(self.auth)

    def getApi(self):
        return self.api


class ObtenerTendencias:
    def __init__(self):
        self.conexion = ConexionTwitter()
        self.api = self.conexion.getApi()

    def obtenerTendenciasCol(self):
        woeid = 368149
        trends = self.api.get_place_trends(woeid)

        nombresTrends = []
        for trend in trends[0]["trends"]:
            nombresTrends.append(trend["name"])

        return nombresTrends


tendencias = ObtenerTendencias()
lista = tendencias.obtenerTendenciasCol()


def guardar_seleccion(palabra, num):
    js_code = f"""<script>localStorage.setItem("tendencia", JSON.stringify( {[ palabra, num]} ));</script>"""
    st.components.v1.html(js_code)


def generar_nombre_aleatorio(nombre):
    adjetivos = [
        "Increíble",
        "Furioso",
        "Épico",
        "Loco",
        "Divertido",
        "Brillante",
        "Inesperado",
        "Misterioso",
    ]
    sustantivos = [
        "Aventura",
        "Caos",
        "Magia",
        "Risas",
        "Desafío",
        "Innovación",
        "Sorpresa",
        "Enigma",
    ]

    adjetivo_aleatorio = random.choice(adjetivos)
    sustantivo_aleatorio = random.choice(sustantivos)

    nombre_aleatorio = adjetivo_aleatorio + " " + nombre + " " + sustantivo_aleatorio

    return nombre_aleatorio


def trending_topics():
    st.title("Trending Topics:")
    st.write("Seleccione el número de tweets:")
    st.write(traducir_texto("Seleccione el número de tweets:", "es", "en"))

    int_val = st.slider("", 20, 80, 20)
    html_code = """
    <div>
        <h4>Trending Topics in Colombia: </h4>
    </div>"""

    st.markdown(html_code, unsafe_allow_html=True)
    st.write("Seleccione una tendencia:")
    st.write(traducir_texto("Seleccione una tendencia:", "es", "en"))

    for i in range(len(lista)):
        col1, col2 = st.columns([0.1, 3])
        with col1:
            st.write(f"{i+1}.")
        with col2:
            if st.button(generar_nombre_aleatorio(lista[i]), key=f"{i}"):
                st.write("Por favor diríjase al apartado de tweets para visualizarlos")
                st.write(
                    traducir_texto(
                        "Por favor diríjase al apartado de tweets para visualizarlos",
                        "es",
                        "en",
                    )
                )
                guardar_seleccion(lista[i], int_val)


trending_topics()
