from textblob import TextBlob
import pages.Trending_topics as Trending_topics
import streamlit as st


st.set_page_config(page_title="Emotions Tweets", page_icon="assets/TwitterIcon.png")

st.markdown(
    '<link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">',
    unsafe_allow_html=True,
)


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


def homepage():
    st.title("Emotions Tweets:")
    st.write(
        """El objetivo general de este software es recopilar cierta cantidad de Tweets de las principales tendencias en Twitter según decida el usuario e identificar si una tendencia es positiva o negativa a través de un algoritmo que se basa en el análisis de datos o ciencia de datos."""
    )
    st.write(
        traducir_texto(
            "El objetivo general de este software es recopilar cierta cantidad de Tweets de las principales tendencias en Twitter según decida el usuario e identificar si una tendencia es positiva o negativa a través de un algoritmo que se basa en el análisis de datos o ciencia de datos.",
            "es",
            "en",
        )
    )

    st.write(
        f"""
        <br/>
        <a target="_self" href="http://localhost:8501/Trending_topics">
            <button class="btn btn-primary">
                Trending Topics
            </button>
        </a>
        """,
        unsafe_allow_html=True,
    )

    st.components.v1.html(
        '<br><img src="https://j.gifs.com/pgBzE6.gif" alt="GIF">', width=600, height=300
    )


homepage()
