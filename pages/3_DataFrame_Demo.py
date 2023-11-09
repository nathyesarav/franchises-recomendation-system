from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
import pandas as pd

import streamlit as st
from streamlit.hello.utils import show_code

from google.oauth2 import service_account
from google.cloud import bigquery

# Create API client.
credentials = service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"]
)
client = bigquery.Client(credentials=credentials)

def sr_usuario_franquicia(nombre_usuario):
    @st.cache_data
    def get_data():
        sql = """
        SELECT rgm.name user_name,
        ngm.name business_name,
        rgm.sentiment_analysis,
        rgm.rating,
        FROM proyectofinal.review_gm rgm
        INNER JOIN proyectofinal.negocios_gm ngm on rgm.gmap_id = ngm.gmap_id
        WHERE ngm.category LIKE '%Fast food%'
        ORDER BY rgm.name
        """
        df = client.query(sql).to_dataframe()
        return df

    grouped_data = get_data()
    # Paso 1: Crear un vectorizador TF-IDF para convertir el texto en vectores numéricos
    tfidf_vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf_vectorizer.fit_transform(grouped_data['user_name'])

    # Paso 2: Calcular la matriz de similitud de coseno
    cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)

    # Paso 3: Función para obtener recomendaciones
    def obtener_recomendaciones(nombre_usuario, cosine_sim=cosine_sim):
        # Obtener el índice del usuario que coincide con el nombre
        if nombre_usuario in grouped_data["user_name"].values:
            idx = grouped_data[grouped_data["user_name"] == nombre_usuario].index[0]
        else:
            return ['No se encuentra el usuario']

        # Obtener las puntuaciones de similitud de coseno para el usuario dado
        sim_scores = list(enumerate(cosine_sim[idx]))

        # Ordenar los usuarios según las puntuaciones de similitud
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

        # Obtener los índices de los 5 usuarios más similares (excluyendo el propio negocio)
        top_indices = [i[0] for i in sim_scores[1:6]]

        # Obtener los nombres de los usuarios más similares
        usuarios_similares = grouped_data["user_name"].iloc[top_indices]

        # Retornar restaurantes de los usuarios similares
        return grouped_data["business_name"].iloc[usuarios_similares]
    
    return obtener_recomendaciones(nombre_usuario)

st.set_page_config(page_title="Demo Sistema de Recomendacion", page_icon="📊")
st.markdown("# DataFrame Demo")
st.sidebar.header("DataFrame Demo")
st.write(
    """Test del sistema de recomendación de negocios para invertir en  Florida"""
)
form_sr = st.form('my_form')
nombre_negocio = form_sr.text_input('Nombre del negocio...')
submit = form_sr.form_submit_button('Recomendar')
recomendaciones = 'Ingrese el nombre de la franquicia'

if submit:
    resultados = sr_franquicia_franquicia(nombre_negocio)
    form_sr.subheader(resultados)
else:
    form_sr.subheader(recomendaciones)