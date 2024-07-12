import streamlit as st
import pandas as pd
import psycopg2
import os
import plotly.express as px

# Configurar la página de Streamlit
st.set_page_config(layout="wide", page_title="'DISTRITO 7'")

# Conectar a la base de datos PostgreSQL
def get_postgresql_connection():
    conn = psycopg2.connect(
        host="c6sfjnr30ch74e.cluster-czrs8kj4isg7.us-east-1.rds.amazonaws.com",
        database="da8p7polirg7h2",
        user="u49172vrhqajni",
        password="pcb9b07ba2a78907a722c43201a6cb07868a940796b411f44157294af525a00ce",
        port="5432"
    )
    return conn

# Inicializar la base de datos
def initialize_database():
    conn = get_postgresql_connection()
    cur = conn.cursor()
    
    # Eliminar la tabla denuncias si ya existe
    cur.execute('DROP TABLE IF EXISTS denuncias')
    
    # Crear la nueva tabla denuncias
    cur.execute('''
        CREATE TABLE denuncias (
            id SERIAL PRIMARY KEY,
            texto TEXT,
            fecha DATE,
            "idUnidadEducativa" INT,
            "imageUrl" TEXT
        )
    ''')
    
    # Insertar datos de ejemplo si la tabla está vacía
    cur.execute('SELECT COUNT(*) FROM denuncias')
    count = cur.fetchone()[0]
    
    if count == 0:
        cur.execute('''
            INSERT INTO denuncias (texto, fecha, "idUnidadEducativa", "imageUrl")
            VALUES 
                ('Denuncia 1', '2024-07-01', 1, 'https://example.com/image1.jpg'),
                ('Denuncia 2', '2024-07-02', 2, 'https://example.com/image2.jpg'),
                ('Denuncia 3', '2024-07-03', 3, 'https://example.com/image3.jpg'),
                ('Denuncia 4', '2024-07-04', 4, 'https://example.com/image4.jpg'),
                ('Denuncia 5', '2024-07-05', 5, 'https://example.com/image5.jpg'),
                ('Denuncia 6', '2024-07-06', 1, 'https://example.com/image6.jpg'),
                ('Denuncia 7', '2024-07-07', 2, 'https://example.com/image7.jpg'),
                ('Denuncia 8', '2024-07-08', 3, 'https://example.com/image8.jpg'),
                ('Denuncia 9', '2024-07-09', 4, 'https://example.com/image9.jpg'),
                ('Denuncia 10', '2024-07-10', 5, 'https://example.com/image10.jpg')
                
        ''')
    
    conn.commit()
    cur.close()
    conn.close()

# Llamar a la función de inicialización de la base de datos
initialize_database()

# Obtener los datos de PostgreSQL
@st.cache_data
def load_data():
    conn = get_postgresql_connection()
    query = "SELECT * FROM denuncias"
    df = pd.read_sql(query, conn)
    conn.close()
    return df

df = load_data()

# Imprimir las columnas del DataFrame para depuración
st.write("Columnas del DataFrame:", df.columns)

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
    st.image(os.path.join("assets", "denuncia.jpg"), width=200)
with col2:
    st.markdown("<h1 style='text-align: center;'>DENUNCIAS EN EL DISTRITO 7</h1>", unsafe_allow_html=True)
with col3:
    st.image('https://media.dev.to/cdn-cgi/image/width=1000,height=420,fit=cover,gravity=auto,format=auto/https%3A%2F%2Fdev-to-uploads.s3.amazonaws.com%2Fi%2Fwsp14jmi17ti2s1fikgw.png', width=300)

# Mostrar tabla de datos
if not df.empty:
    col1, col2, col3 = st.columns([1, 6, 1])
    with col2:
        edited_df = st.experimental_data_editor(df, height=300, width=1500)
else:
    st.write("No se encontraron datos en la base de datos.")

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
