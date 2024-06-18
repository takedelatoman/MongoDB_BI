import streamlit as st
import pandas as pd
import plotly.express as px
import random
import pymongo
from bson.objectid import ObjectId
import os

# Conectar a la base de datos
client = pymongo.MongoClient("mongodb://mongo:sfYOJDqFbGZlmmcifQxGGbXXeWLQeulo@monorail.proxy.rlwy.net:28058/springbootgraphql?authSource=admin")
db = client['springbootgraphql']

#collection_users = db['users']
collection_users = db.users
collection_accomodations = db["accomodations"]
collection_offers = db["offers"]


# Obtener la ruta de la imagen del logo
LOGO_PATH = os.path.join("assets", "agenciaViaje4.jpg")

# Crear la aplicación Streamlit
st.set_page_config(layout="wide", page_title="'URPI TOURS'")

#borrar todo menos la 1ra
# Obtener el primer documento de la colección
#first_document = collection_accomodations.find_one()

# Eliminar todos los documentos excepto el primero
#collection_accomodations.delete_many({"_id": {"$ne": first_document["_id"]}})




# Limpiar la colección 'users', excepto los dos primeros documentos

#all_users = list(collection_users.find().limit(2))
#collection_users.delete_many({})

# Reinsertar los dos primeros documentos

#if all_users:
 #  collection_users.insert_many(all_users)


#OFFERS
# Obtener el primer documento de la colección 'offers'
#first_offer = collection_offers.find_one()

# Eliminar todos los documentos excepto el primero
#collection_offers.delete_many({"_id": {"$ne": first_offer["_id"]}})

#print("Se han eliminado todos los documentos de la colección 'offers' excepto el primero.")








# Lista de nombres y correos electrónicos


#nombres = [
#    "Pedro", "Juan", "Carlos", "Miguel", "Luis", "José", "David", "Jorge",
#    "Francisco", "Andrés", "Sergio", "Fernando", "Manuel", "Raúl", "Ricardo",
#    "Antonio", "Pablo", "Martín", "Alejandro", "Enrique", "Alberto", "Gabriel",
#    "Santiago", "Gonzalo", "Adrián", "Cristian", "Mario", "Diego", "Ramón", "Eduardo"
#]

# Insertar 30 usuarios únicos
#for nombre in nombres:
 #   user_data = {
  #      "name": nombre,
   #     "email": f"{nombre.lower()}@gmail.com",
    #    "password": "$2a$10$vYEE7iek8h/VoCfWvXrm4enWT6u9onO8dh.J7xMmcNtUu.flwRiZ2",
     #   "role": "Encargado Alojamiento"
    #}
    #user_data["_class"] = "com.graphl.flight.models.User"
    #collection_users.update_one(
     #   {"name": nombre, "email": f"{nombre.lower()}@gmail.com"},
      #  {"$setOnInsert": user_data},
       # upsert=True
    #)

#print("30 usuarios insertados exitosamente.")










st.write("Usuarios insertados exitosamente")
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
    edited_df = st.experimental_data_editor(df, height=300)
else:
    st.write("No data found in the database.")

# Graficos
if not df.empty:
    st.markdown("<h3 style='text-align: center;'>Gráficos</h3>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 6, 1])
    with col2:
        pie_fig = px.pie(df, names='stars', title='Distribución de Estrellas')
        st.plotly_chart(pie_fig, use_container_width=True)
    
    col1, col2, col3 = st.columns([1, 6, 1])
    with col2:
        bar_fig = px.bar(df, x='company', y='stars', title='Estrellas por Compañía')
        st.plotly_chart(bar_fig, use_container_width=True)
    
    col1, col2, col3 = st.columns([1, 6, 1])
    with col2:
        scatter_fig = px.scatter(df, x='coordinates', y='stars', title='Coordenadas vs Estrellas')
        st.plotly_chart(scatter_fig, use_container_width=True)

# Actualizar datos en MongoDB
if edited_df is not None and not edited_df.equals(df):
    for i in range(len(edited_df)):
        row_id = edited_df.at[i, '_id']
        for col in edited_df.columns:
            if edited_df.at[i, col] != df.at[i, col]:
                collection_accomodations.update_one({'_id': ObjectId(row_id)},
                                                    {"$set": {col: edited_df.at[i, col]}})












# Función para obtener datos de la colección 'offers' y convertirlos a DataFrame
@st.cache_data
def get_offers_data():
    data = list(collection_offers.find())
    if data:
        df = pd.DataFrame(data)
        df['_id'] = df['_id'].astype(str)
        return df
    return pd.DataFrame()

# Mostrar tabla de datos para 'offers'
offers_df = get_offers_data()
if not offers_df.empty:
    edited_offers_df = st.experimental_data_editor(offers_df, height=300)
else:
    st.write("No data found in the 'offers' collection.")

# Graficos para 'offers'
if not offers_df.empty:
    st.markdown("<h3 style='text-align: center;'>Gráficos para 'offers'</h3>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 6, 1])
    with col2:
        offers_bar_fig = px.bar(offers_df, x='title', y='price', color='beds', title='Precio por Camas y Título')
        st.plotly_chart(offers_bar_fig, use_container_width=True)
    
    col1, col2, col3 = st.columns([1, 6, 1])
    with col2:
        offers_scatter_fig = px.scatter(offers_df, x='state', y='title', color='price', title='Estado por Título y Precio')
        st.plotly_chart(offers_scatter_fig, use_container_width=True)