import streamlit as st
import pandas as pd
import plotly.express as px
import pymongo
from bson.objectid import ObjectId
import os

# Conectar a la base de datos
client = pymongo.MongoClient("mongodb://mongo:sfYOJDqFbGZlmmcifQxGGbXXeWLQeulo@monorail.proxy.rlwy.net:28058/springbootgraphql?authSource=admin")
db = client['springbootgraphql']
collection_accomodations = db['accomodations']

# Obtener la ruta de la imagen del logo
LOGO_PATH = os.path.join("assets", "agenciaViaje4.jpg")

# Crear la aplicación Streamlit
st.set_page_config(layout="wide", page_title="Agencia de Viajes 'URPI TOURS'")

# Estilos
st.markdown(
    """
    <style>
    .main {
        background-color: black;
        color: white;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Logo en la parte superior izquierda
col1, col2, col3 = st.columns([1, 6, 1])
with col1:
    st.image(LOGO_PATH, width=150)
with col2:
    st.markdown("<h1 style='text-align: center;'>AGENCIA DE VIAJES 'URPI TOURS'</h1>", unsafe_allow_html=True)
with col3:
    st.image('https://cdn.icon-icons.com/icons2/2415/PNG/512/mongodb_plain_wordmark_logo_icon_146423.png', width=100)

st.markdown("<h2 style='text-align: center;'>Base de datos MongoDB Grupo12</h2>", unsafe_allow_html=True)

# Función para obtener datos y convertirlos a DataFrame
@st.cache_data
def get_data():
    data = list(collection_accomodations.find())
    if data:
        df = pd.DataFrame(data)
        df['_id'] = df['_id'].astype(str)
        if 'typeRoom' in df.columns:
            df['typeRoom'] = df['typeRoom'].apply(lambda x: ', '.join(x) if isinstance(x, list) else str(x))
        return df
    return pd.DataFrame()

# Mostrar tabla de datos
df = get_data()
if not df.empty:
    edited_df = st.data_editor(df, height=300)
else:
    st.write("No data found in the database.")

# Graficos
if not df.empty:
    pie_fig = px.pie(df, names='stars', title='Distribución de Estrellas')
    bar_fig = px.bar(df, x='company', y='stars', title='Estrellas por Compañía')
    scatter_fig = px.scatter(df, x='coordinates', y='stars', title='Coordenadas vs Estrellas')

    st.plotly_chart(pie_fig)
    st.plotly_chart(bar_fig)
    st.plotly_chart(scatter_fig)

# Actualizar datos en MongoDB
if edited_df is not None and not edited_df.equals(df):
    for i in range(len(edited_df)):
        row_id = edited_df.at[i, '_id']
        for col in edited_df.columns:
            if edited_df.at[i, col] != df.at[i, col]:
                collection_accomodations.update_one({'_id': ObjectId(row_id)},
                                                    {"$set": {col: edited_df.at[i, col]}})
