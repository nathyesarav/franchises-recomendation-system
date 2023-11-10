from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
import pandas as pd

import streamlit as st
from streamlit.hello.utils import show_code
from google.oauth2 import service_account
from google.cloud import bigquery

def sr_franquicia_franquicia(nombre_negocio):
    # Create API client.
    credentials = service_account.Credentials.from_service_account_info(
        st.secrets["gcp_service_account"]
    )
    client = bigquery.Client(credentials=credentials)

    @st.cache_data
    def get_data():
        sql = """
        SELECT ngm.name name, 
        SUM(rgm.sentiment_analysis) sentiment_analysis,
        AVG(rgm.rating) rating,
        AVG(ngm.avg_rating) avg_rating
        FROM `proyectofinal.review_gm` rgm
        INNER JOIN proyectofinal.negocios_gm ngm ON rgm.gmap_id = ngm.gmap_id
        WHERE ngm.category LIKE '%Fast food%'
        GROUP BY ngm.name
        ORDER BY ngm.name
        """
        #df = pd.read_csv("pages/data/gmaps_results.csv")
        df = client.query(sql).to_dataframe()
        return df

    grouped_data = get_data()
    # Paso 1: Crear un vectorizador TF-IDF para convertir el texto en vectores numéricos
    tfidf_vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf_vectorizer.fit_transform(grouped_data['name'])

    # Paso 2: Calcular la matriz de similitud de coseno
    cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)

    # Paso 3: Función para obtener recomendaciones
    def obtener_recomendaciones(nombre_negocio, cosine_sim=cosine_sim):
        # Obtener el índice del negocio que coincide con el nombre
        if nombre_negocio in grouped_data["name"].values:
            idx = grouped_data[grouped_data["name"] == nombre_negocio].index[0]
        else:
            return ['No se encuentra el negocio']

        # Obtener las puntuaciones de similitud de coseno para el negocio dado
        sim_scores = list(enumerate(cosine_sim[idx]))

        # Ordenar los negocios según las puntuaciones de similitud
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

        # Obtener los índices de los 5 negocios más similares (excluyendo el propio negocio)
        top_indices = [i[0] for i in sim_scores[1:6]]

        # Devolver los nombres de los negocios más similares
        return grouped_data["name"].iloc[top_indices]
    
    lista_negocios = grouped_data["name"]
    return obtener_recomendaciones(nombre_negocio)

st.set_page_config(page_title="Sistema de Recomendacion Franquicias", page_icon="📊")
st.markdown("# Sistema de Recomendacion Franquicias")
st.sidebar.header("Sistema de Recomendacion Franquicias")
st.write(
    """Sistema de recomendación de franquicias de Fast-Food para invertir en Florida"""
)

lista_negocios = []

form_sr = st.form('my_form')
nombre_usuario = form_sr.text_input('Nombre de franquicia...')
option = form_sr.selectbox(
    'Seleccione el nombre de la Franquicia',
    (lista_negocios)
submit = form_sr.form_submit_button('Recomendar')
recomendaciones = 'Ingrese el nombre del usuario'

if submit:
    resultados = sr_franquicia_franquicia(nombre_usuario)
    form_sr.subheader(resultados)
else:
    form_sr.subheader(recomendaciones)

