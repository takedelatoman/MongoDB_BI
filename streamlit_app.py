import streamlit as st
import pandas as pd
import plotly.express as px
import psycopg2
import os

# Conectar a la base de datos PostgreSQL
def get_postgresql_data():
    conn = psycopg2.connect(
        host="c6sfjnr30ch74e.cluster-czrs8kj4isg7.us-east-1.rds.amazonaws.com",
        database="da8p7polirg7h2",
        user="u49172vrhqajni",
        password="pcb9b07ba2a78907a722c43201a6cb07868a940796b411f44157294af525a00ce",
        port="5432"
    )
    query = "SELECT * FROM denuncias"
    df = pd.read_sql(query, conn)
    conn.close()
    return df

# Crear la aplicación Streamlit
st.set_page_config(layout="wide", page_title="'URPI TOURS'")

# Obtener la ruta de la imagen del logo
LOGO_PATH = os.path.join("assets", "denuncia.jpg")

# Obtener los datos de PostgreSQL
@st.cache_data
def load_data():
    return get_postgresql_data()

df = load_data()

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
col1, col2, col3 = st.columns([1, 6, 2])  # Ajusta los anchos de las columnas según sea necesario
with col1:
    st.image(LOGO_PATH, width=200)
with col2:
    st.markdown("<h1 style='text-align: center;'>DENUNCIAS EN EL DISTRITO 7 </h1>", unsafe_allow_html=True)
with col3:
    st.image('https://media.dev.to/cdn-cgi/image/width=1000,height=420,fit=cover,gravity=auto,format=auto/https%3A%2F%2Fdev-to-uploads.s3.amazonaws.com%2Fi%2Fwsp14jmi17ti2s1fikgw.png', width=300)

# Mostrar tabla de datos
if not df.empty:
    col1, col2, col3 = st.columns([1, 6, 1])
    with col2:
        edited_df = st.experimental_data_editor(df, height=300, width=1500)
else:
    st.write("No data found in the database.")

# Gráficos
if not df.empty:
    st.markdown("<h3 style='text-align: center;'>Gráficos</h3>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 6, 1])
    with col2:
        pie_fig = px.pie(df, names='idUnidadEducativa', title='Distribución por Unidad Educativa')
        st.plotly_chart(pie_fig, use_container_width=True)
    
    col1, col2, col3 = st.columns([1, 6, 1])
    with col2:
        bar_fig = px.bar(df, x='id', y='idUnidadEducativa', title='Denuncias por ID y Unidad Educativa')
        st.plotly_chart(bar_fig, use_container_width=True)
    
    col1, col2, col3 = st.columns([1, 6, 1])
    with col2:
        scatter_fig = px.scatter(df, x='fecha', y='id', title='Fecha vs ID de Denuncias')
        st.plotly_chart(scatter_fig, use_container_width=True)