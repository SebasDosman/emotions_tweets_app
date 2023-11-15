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

st.markdown(
    '<link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">',
    unsafe_allow_html=True,
)

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


def traducir_texto(texto, idioma_origen, idioma_destino):
    blob = TextBlob(texto)

    texto_traducido = blob.translate(from_lang=idioma_origen, to=idioma_destino)

    return str(texto_traducido)


class ConexionTwitter:
    def __init__(self):
        self.auth = tweepy.OAuthHandler(API_KEY_TWITTER, API_SECRET_KEY)
        self.auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
        self.api = tweepy.API(self.auth)

    def getApi(self):
        return self.api

    def limpiar_texto_twits(self, lista_twits):
        twits_sin_emojis = [self.deEmojify(twit) for twit in lista_twits]
        return twits_sin_emojis

    def traducir_twits(self, lista_twits):
        twits_ingles = [
            TextBlob(twit).translate(from_lang="es", to="en") for twit in lista_twits
        ]
        return twits_ingles

        return []

    def deEmojify(self, text):
        regrex_pattern = re.compile(
            pattern="["
            "\U00002702-\U000027B0"
            "\U00002702-\U000027B0"
            "\U000024C2-\U0001F251"
            "\U0001f926-\U0001f937"
            "\U00010000-\U0010ffff"
            "\u2640-\u2642"
            "\u2600-\u2B55"
            "\u200d"
            "\u23cf"
            "\u23e9"
            "\u231a"
            "\u3030"
            "]+",
            flags=re.UNICODE,
        )
        return regrex_pattern.sub(r"", text)

    def buscarTwitsTendenciasIngles(self, tendencia, n_tweets):
        lista_twits = self.api.search_tweets(q=tendencia, lang="es", count=n_tweets)

        lista_twits_texto_sucia = [twit._json["text"].strip() for twit in lista_twits]

        twits_limpios = self.limpiar_texto_twits(lista_twits_texto_sucia)
        twits_ingles = self.traducir_twits(twits_limpios)

        for i in range(len(twits_ingles)):
            st.write(f"""{i+1}. { twits_ingles[i]}""")

        return twits_ingles

    def buscarTwitsTendenciasEspanol(self, tendencia, n_tweets):
        lista_twits = self.api.search_tweets(q=tendencia, lang="es", count=n_tweets)

        lista_twits_texto_sucia = [twit._json["text"].strip() for twit in lista_twits]

        twits_limpios = self.limpiar_texto_twits(lista_twits_texto_sucia)

        for i in range(len(twits_limpios)):
            st.write(f"""{i+1}. { twits_limpios[i]}""")

        return twits_limpios


class Obtener_porcentaje:
    def obtener_lista_porcentajes(self, lista_twits):
        return [self.obtener_porcentaje(twit) for twit in lista_twits]

    def obtener_porcentaje(self, text):
        return text.sentiment.polarity


def get_from_local_storage(k):
    v = st_javascript(f"JSON.parse(localStorage.getItem('{k}'));", key="unique")
    return v or {}


def redireccion():
    st.write(
        f"""
        <a target="_self" href="http://localhost:8501/Gráficas">
            <button class="btn btn-primary">
                Gráficas
            </button>
        </a>
        """,
        unsafe_allow_html=True,
    )


lista_twits_tendencia = []


def tweets():
    st.title("Tweets:")
    data = get_from_local_storage("tendencia")

    try:
        info = f"""La tendencia es {data[0]} y la cantidad de tweets es {data[1]}:"""
        info_english = traducir_texto(info, "es", "en")
        st.write(info)

    except KeyError as e:
        st.write(
            "Por favor ve a la sección de trending topics y selecciona la tendencia"
        )
        info_english_dos = traducir_texto(
            "Por favor ve a la sección de trending topics y selecciona la tendencia",
            "es",
            "en",
        )

        st.write(info_english_dos)
        st.components.v1.html(
            '<img src="https://media.tenor.com/uCMXQo80r0kAAAAC/guino-ozuna.gif" alt="GIF">',
            width=600,
            height=300,
        )

    conex = ConexionTwitter()
    porcentajes = Obtener_porcentaje()

    try:
        twits_espanol = conex.buscarTwitsTendenciasEspanol(data[0], data[1])

        st.components.v1.html("<br>")
        st.write(info_english)

        twits_ingles = conex.buscarTwitsTendenciasIngles(data[0], data[1])
    except Exception as e:
        print("Error al buscar los tweets, muchas peticiones")
        twits_espanol = []

    lista_porcentajes = porcentajes.obtener_lista_porcentajes(twits_ingles)

    js_code = f"""
    <script>
        localStorage.setItem("porcentajes", JSON.stringify( {lista_porcentajes} ));
    </script>
    """
    st.components.v1.html(js_code)


tweets()
