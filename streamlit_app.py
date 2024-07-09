import streamlit as st
import pandas as pd
import plotly.express as px
import psycopg2
import os

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

def initialize_database():
    conn = get_postgresql_connection()
    cur = conn.cursor()
    
    # Eliminar la tabla si ya existe
    cur.execute('DROP TABLE IF EXISTS denuncias')
    
    # Crear la tabla
    cur.execute('''
        CREATE TABLE denuncias (
            id SERIAL PRIMARY KEY,
            texto TEXT,
            fecha DATE,
            idUnidadEducativa INT,
            imageUrl TEXT
        )
    ''')
    
    # Insertar datos de ejemplo si la tabla está vacía
    cur.execute('SELECT COUNT(*) FROM denuncias')
    count = cur.fetchone()[0]
    
    if count == 0:
        cur.execute('''
            INSERT INTO denuncias (texto, fecha, idUnidadEducativa, imageUrl)
            VALUES 
                ('Denuncia por acoso escolar', '2024-06-01', 1, 'https://example.com/image1.jpg'),
                ('Denuncia por falta de infraestructura', '2024-06-02', 2, 'https://example.com/image2.jpg'),
                ('Denuncia por violencia física', '2024-06-03', 3, 'https://example.com/image3.jpg'),
                ('Denuncia por falta de maestros', '2024-06-04', 4, 'https://example.com/image4.jpg'),
                ('Denuncia por robo de materiales', '2024-06-05', 5, 'https://example.com/image5.jpg'),
                ('Denuncia por discriminación', '2024-06-06', 1, 'https://example.com/image6.jpg'),
                ('Denuncia por falta de agua potable', '2024-06-07', 2, 'https://example.com/image7.jpg'),
                ('Denuncia por maltrato verbal', '2024-06-08', 3, 'https://example.com/image8.jpg'),
                ('Denuncia por falta de electricidad', '2024-06-09', 4, 'https://example.com/image9.jpg'),
                ('Denuncia por falta de seguridad', '2024-06-10', 5, 'https://example.com/image10.jpg')
        ''')
    
    conn.commit()
    cur.close()
    conn.close()

def get_postgresql_data():
    conn = get_postgresql_connection()
    query = "SELECT * FROM denuncias"
    df = pd.read_sql(query, conn)
    conn.close()
    return df

# Inicializar la base de datos
initialize_database()

# Crear la aplicación Streamlit
st.set_page_config(layout="wide", page_title="'DISTRITO 7'")

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
        pie_fig = px.pie(df, names='idunidadeducativa', title='Distribución por Unidad Educativa')
        st.plotly_chart(pie_fig, use_container_width=True)
    
    col1, col2, col3 = st.columns([1, 6, 1])
    with col2:
        bar_fig = px.bar(df, x='id', y='idunidadeducativa', title='Denuncias por ID y Unidad Educativa')
        st.plotly_chart(bar_fig, use_container_width=True)
    
    col1, col2, col3 = st.columns([1, 6, 1])
    with col2:
        scatter_fig = px.scatter(df, x='fecha', y='id', title='Fecha vs ID de Denuncias')
        st.plotly_chart(scatter_fig, use_container_width=True)
