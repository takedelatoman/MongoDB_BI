# dash_app.py
import dash
from dash import dcc, html, dash_table
from dash.dependencies import Input, Output, State
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

# Crear la aplicación Dash
app = dash.Dash(__name__, suppress_callback_exceptions=True, external_stylesheets=['styles.css'])

# Define Layout of App
app.layout = html.Div(style={'backgroundColor': 'black', 'color': 'white'}, children=[
    # Logo en la parte superior izquierda
    html.Div([
        html.Img(src=LOGO_PATH, style={'height': '150px', 'width': '150px', 'float': 'left', 'margin-right': '10px'}),
        html.H1('AGENCIA DE VIAJES "URPI TOURS"', style={'textAlign': 'center'}),
        html.Img(src='https://cdn.icon-icons.com/icons2/2415/PNG/512/mongodb_plain_wordmark_logo_icon_146423.png', style={'height': '100px', 'width': '100px', 'float': 'right'}),
    ]),
    html.H2('Base de datos MongoDB Grupo12', style={'textAlign': 'center'}),
    dcc.Interval(id='interval_db', interval=86400000 * 7, n_intervals=0),
    html.Div(id='mongo-datatable', children=[]),

    html.Div([
        html.Div(id='stars-pie-graph', className='five columns'),
        html.Div(id='company-stars-bar-graph', className='six columns'),
        html.Div(id='coordinates-stars-scatter-graph', className='six columns'),
    ], className='row'),
    dcc.Store(id='changed-cell')
])

# Display Datatable with data from Mongo database
@app.callback(Output('mongo-datatable', component_property='children'),
              Input('interval_db', component_property='n_intervals'))
def populate_datatable(n_intervals):
    # Convert the Collection (table) data to a pandas DataFrame
    data = list(collection_accomodations.find())
    if not data:
        return html.Div("No data found in the database.")

    df = pd.DataFrame(data)
    if '_id' in df.columns:
        df['_id'] = df['_id'].astype(str)
    else:
        return html.Div("El campo '_id' no se encontró en los datos.")

    # Convertir el campo 'typeRoom' a una cadena de texto
    if 'typeRoom' in df.columns:
        df['typeRoom'] = df['typeRoom'].apply(lambda x: ', '.join(x) if isinstance(x, list) else str(x))

    return [
        dash_table.DataTable(
            id='our-table',
            data=df.to_dict('records'),
            columns=[{'id': p, 'name': p, 'editable': False} if p == '_id'
                     else {'id': p, 'name': p, 'editable': True}
                     for p in df.columns],
            style_cell={'color': 'white', 'backgroundColor': 'black'},  # Estilo de las celdas
            style_header={'backgroundColor': 'rgb(30, 30, 30)', 'color': 'white'},
            page_size=10,  # Muestra 10 registros por página
            style_table={'overflowX': 'auto'},
        ),
    ]

# store the row id and column id of the cell that was updated
@app.callback(
    Output('changed-cell', 'data'),
    Input('our-table', 'data'),
    State('our-table', 'data_previous')
)
def store_changed_cell(input, old_input):
    if old_input is not None:
        if input != old_input:
            for i in range(len(input)):
                new_values = list(input[i].values())
                old_values = list(old_input[i].values())
                if new_values != old_values:
                    return [i, list(input[i].keys())[list(input[i].values()).index(new_values)]]

# Update MongoDB and create the graphs
@app.callback(
    Output("stars-pie-graph", "children"),
    Output("company-stars-bar-graph", "children"),
    Output("coordinates-stars-scatter-graph", "children"),
    Input("changed-cell", "data"),
    Input("our-table", "data"),
)
def update_d(cc, tabledata):
    if not tabledata:
        return html.Div("No data found in the database."), html.Div("No data found in the database."), html.Div("No data found in the database.")

    df = pd.DataFrame(tabledata)

    if cc is None:
        pie_fig = px.pie(df, names='stars', title='Distribución de Estrellas')
        bar_fig = px.bar(df, x='company', y='stars', title='Estrellas por Compañía')
        scatter_fig = px.scatter(df, x='coordinates', y='stars', title='Coordenadas vs Estrellas')
    else:
        x = int(cc[0])
        row_id = tabledata[x]['_id']
        col_id = cc[1]
        new_cell_data = tabledata[x][col_id]
        collection_accomodations.update_one({'_id': ObjectId(row_id)},
                              {"$set": {col_id: new_cell_data}})

        pie_fig = px.pie(df, names='stars', title='Distribución de Estrellas')
        bar_fig = px.bar(df, x='company', y='stars', title='Estrellas por Compañía')
        scatter_fig = px.scatter(df, x='coordinates', y='stars', title='Coordenadas vs Estrellas')

    return dcc.Graph(figure=pie_fig), dcc.Graph(figure=bar_fig), dcc.Graph(figure=scatter_fig)

if __name__ == '__main__':
    app.run_server(debug=True)
