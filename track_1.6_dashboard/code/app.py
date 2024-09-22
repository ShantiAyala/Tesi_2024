import random
from dash import Dash, html, dcc, dash_table, Input, Output
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from services.data_analysis import fetch_data_for_dash,fetch_data_for_dash2, generate_energy_consumption, generate_water_consumption, generate_pesticide_use, calculate_from_rainfall
from services.queries import stock_query, stock_history_price, best_of_query, weather_query, quantities_sold, payment_methods_used, total_amounts_current_year, quantity_per_transaction_current_year, crop_details_query,  crop_names_query, temperature_query, humidity_query, precipitation_query, costs_query, salariescost_query, precipitationcost_query


# Initialize the Dash app
app = Dash(__name__, external_stylesheets=['/static/styles.css'])

# Section 1.a   Fetch the data for the table and bar graph ---------------
df_stock = fetch_data_for_dash(stock_query)

# Fetch the data for the line graph (price history)
df_price_history = fetch_data_for_dash(stock_history_price)
df_price_history['startdate'] = pd.to_datetime(df_price_history['startdate'])
years = df_price_history['startdate'].dt.year.unique()
product_names = df_price_history['productname'].unique()

#1.b  Fetch the data for the table and bar graph bestrating --------------------------

# Fetch the data from the query
df_best_of = fetch_data_for_dash(best_of_query)
df_best_of['year'] = df_best_of['year'].astype(int)
df_best_of['month'] = df_best_of['month'].astype(int)

# Get the list of unique years and months
available_years_sales_rating = sorted(df_best_of['year'].unique())
available_months_sales_rating = list(range(1, 13))  # Lista da 1 a 12 per i mesi

#2.a Fetch the data for line chart weather conditions -----------------------

df_weather = fetch_data_for_dash(weather_query)
df_weather['date'] = pd.to_datetime(df_weather['date'])
#4.a Fetch the data for section 4 -----------------------
crop_names = fetch_data_for_dash(crop_names_query)['cropname'].tolist()
# Dizionario per mappare le variabili con le loro unità di misura
variable_units = {
    'temperature': '°C',
    'humidity': '%',
    'precipitation': 'mm',
    'windspeed': 'm/s',
    'solarradiation': 'W/m²',
    'soilmoisture': '%'
}
mesi = [
    'Gennaio', 'Febbraio', 'Marzo', 'Aprile', 'Maggio', 'Giugno',
    'Luglio', 'Agosto', 'Settembre', 'Ottobre', 'Novembre', 'Dicembre'
]
#-----------------------------------------

# Create a simple bar chart using Plotly for stock data
fig_stock = px.bar(df_stock, x='productname', y='stockquantity', title='Stock per Product')

# Define the layout of the Dash app
app.layout = html.Div(className='container', children=[
    
    # Main title (spans across 2 columns)
    html.Div([
        html.Div([
            html.H1('ATTavola DASHBOARD', className='title_text')
        ], className="title_container")
    ], className="row flex-display"),


    # Row 1 - ANALISI PRODOTTI
    html.Div(className='sub-container', children=[
        html.H2('1) Analisi Prodotti'),
        
        
        
        html.H2("Scorte magazzino", style={'textAlign': 'center'}),

        # Add a bar chart for stock data
        html.Div(className="graph", children=[
            dcc.Graph(
                id='bar-chart',
                figure=fig_stock
            )
        ]),

        html.H1("Costo nel Tempo", style={'textAlign': 'center'}),

        # Add Slider for Year Selection
        html.Label("Select Year:"),
        dcc.Slider(
            id='year-slider',
            min=min(years),
            max=max(years),
            value=max(years),  # Imposta l'anno corrente come valore predefinito
            marks={str(year): str(year) for year in years},
            step=None
        ),

        # Add Dropdown for Product Selection
        html.Label("Select Product:"),
        dcc.Dropdown(
            id='product-dropdown',
            options=[{'label': 'All', 'value': 'All'}] + [{'label': name, 'value': name} for name in product_names],
            value='All',  # Imposta "All" come valore predefinito
            multi=False
        ),

        # Line Graph for Price History
        dcc.Graph(id='price-chart'),


        #best product----------------
        # Main title
        html.H2("Prodotti più venduti e valutati", style={'textAlign': 'center'}),


        # Month Slider
        html.Label("Select Month"),
        dcc.Slider(
            id='month-slider',
            min=1, max=12, step=1, value=1,
            marks={i: f'{i}' for i in range(1, 13)}
        ),

        # Output table
    
        dash_table.DataTable(
            id='best-table',
            columns=[
                {"name": "Prodotto più venduto", "id": "best_selling"},
                {"name": "Best Rating", "id": "best_rated"}
            ],
            data=[],
            style_table={'width': '50%', 'margin': 'auto'},
            style_cell={'padding': '10px', 'textAlign': 'center'},
            style_header={'fontWeight': 'bold', 'backgroundColor': 'rgb(230, 230, 230)'}
        )
    ]),    

    # Row 2 - MONITORAGGIO AMBIENTALE
    html.Div(className='sub-container', children=[html.H2('2) Monitoraggio Ambientale')]),
    # Titolo
    html.H2("Analisi Registrazioni Atmosferiche", style={'textAlign': 'center'}),
  
    
    # Slider per selezione dell'anno
    html.Label("Select Year"),
    dcc.Slider(
        id='year2-slider',
        min=2020, max=2023, step=1, value=2023,
        marks={i: f'{i}' for i in range(2020, 2024)}
    ),
    html.Label("Select Month"),
        dcc.Slider(
            id='month2-slider',
            min=1, max=12, step=1, value=1,
            marks={i: f'{i}' for i in range(1, 13)}
        ),
    # Dropdown per la variabile meteo da visualizzare
    html.Label("Select Weather Variable"),
    dcc.Dropdown(
        id='weather-variable-dropdown',
        options=[
            {'label': 'Temperature', 'value': 'temperature'},
            {'label': 'Humidity', 'value': 'humidity'},
            {'label': 'Precipitation', 'value': 'precipitation'},
            {'label': 'Wind Speed', 'value': 'windspeed'},
            {'label': 'Solar Radiation', 'value': 'solarradiation'},
            {'label': 'Soil Moisture', 'value': 'soilmoisture'}
        ],
        value='temperature',  
    ),
    
    # Grafico lineare weathercondistions
    dcc.Graph(id='weather-graph'),

    # Row 3 - ANALISI VENDITE--------------------------------------------------------------------------
    html.Div(className='sub-container', children=[html.H2('3) Analisi Vendite')]),
    
    dcc.Dropdown(
        id='month-dropdown',
        options=[{'label': mesi[i-1], 'value': i} for i in range(1, 13)], 
        value=1,  # Mese di default (Gennaio)
        clearable=False
    ),


    html.Div(className='sub-container', children=[
        html.Div(id='sales-pie-container'),  
        html.Div(id='payment-method-pie-container')  
    ]),

    dcc.Dropdown(
        id='month-dropdown2',
        options=[{'label': mesi[i - 1], 'value': i} for i in range(1, 13)],
        value=1,  # Default month (January)
        clearable=False
    ),
    html.Div(className='sub-container', children=[
        html.Div([
            html.Div(id='total-amount-line-chart-container')  # Container for the total amount line chart
        ]),
        html.Div([
            html.Div(id='quantity-line-chart-container')  # Container for the quantity line chart
        ])
    ]),


    # Row 4 Sezione 4 Crops - -----------------------------------------------
    html.H1("4) Analisi delle Colture"),

    # Selettore per il nome della coltura
    dcc.Dropdown(
        id='crop-dropdown',
        options=[{'label': crop_name, 'value': crop_name} for crop_name in crop_names],
        placeholder="Seleziona una coltura",
        style={'width': '50%'}
    ),

    # Selettore del mese
    dcc.Dropdown(
        id='month4-dropdown',
        options=[{'label': mesi[i], 'value': i + 1} for i in range(len(mesi))],
        placeholder="Seleziona un mese",
        style={'width': '50%'}
    ),

    # Contenitore per la tabella dei dettagli della coltura
    html.Div(id='crop-table-container', style={'margin-top': '20px'}),

    # Contenitore per i grafici a istogramma delle condizioni meteo
    html.Div(id='weather-comparison-bar-charts'),
    
    
    # Row 5 - sezione 5 -----------------------------------------
    html.Div(
    className='sub-container',
    children=[
        html.H2('5) Analisi Costi'),
            html.Div(
                children=[
                    dcc.Dropdown(
                        id='month5-dropdown',
                        options=[{'label': m, 'value': i + 1} for i, m in enumerate(mesi)],
                        value=1,
                        clearable=False,
                        style={'margin-bottom': '20px'}  # Spaziatura sotto il dropdown
                    ),
                    html.Div(id='monthly-cost-pie-chart-container')  # Contenitore per il grafico e il messaggio
                ],
                style={'padding': '20px', 'border': '1px solid #ddd', 'border-radius': '5px'}  # Stile per il contenitore
            )
        ]
    ),

])


# CALLBACKS -----------------------------------------------------------------
# Sezione 1.a Callback per aggiornare il grafico lineare in base alle selezioni di anno e prodotto
from dash import Dash, html, dcc, dash_table, Input, Output
import plotly.graph_objects as go
import pandas as pd

# Callback per aggiornare il grafico dei prezzi
@app.callback(
    Output('price-chart', 'figure'),
    [Input('year-slider', 'value'),        # Riferito al grafico dei prezzi
     Input('product-dropdown', 'value')]
)
def update_graph(selected_year, selected_product):
    # Filtra i dati per l'anno selezionato
    filtered_df = df_price_history[df_price_history['startdate'].dt.year == selected_year]
    
    # Filtra i dati per il prodotto selezionato, se non è "All"
    if selected_product != 'All':
        filtered_df = filtered_df[filtered_df['productname'] == selected_product]
    
    # Crea il grafico
    fig = go.Figure()

    # Se "All" è selezionato, mostra tutte le linee
    if selected_product == 'All':
        for product in filtered_df['productname'].unique():
            product_df = filtered_df[filtered_df['productname'] == product]
            fig.add_trace(go.Scatter(
                x=product_df['startdate'],
                y=product_df['price'],
                mode='lines',
                name=product
            ))
    else:
        # Se un prodotto specifico è selezionato, mostra solo la sua linea
        fig.add_trace(go.Scatter(
            x=filtered_df['startdate'],
            y=filtered_df['price'],
            mode='lines',
            name=selected_product
        ))

    # Aggiungi titolo e etichette al grafico
    fig.update_layout(
        title=f'Price History for {selected_product if selected_product != "All" else "All Products"} in {selected_year}',
        xaxis_title='Date',
        yaxis_title='Price',
        hovermode='closest',
        # Aggiungi il range manuale per mostrare l'intero anno
        xaxis_range=[f'{selected_year}-01-01', f'{selected_year}-12-31']
    )

    return fig

# Callback per aggiornare la tabella in base al mese selezionato
@app.callback(
    Output('best-table', 'data'),
    [Input('month-slider', 'value')]  # Solo selezione del mese
)
def update_table(selected_month):
    # Supponiamo che l'anno sia fisso, ad esempio 2024
    selected_year = 2024
    
    # Filtra i dati per l'anno e mese selezionati
    filtered_df = df_best_of[(df_best_of['year'] == selected_year) & (df_best_of['month'] == selected_month)]
    
    if filtered_df.empty:
        return []

    # Trova il prodotto più venduto
    best_selling_product = filtered_df.loc[filtered_df['total_sales'].idxmax()]['productname']

    # Trova il prodotto con il miglior rating
    best_rated_product = filtered_df.loc[filtered_df['total_ratings'].idxmax()]['productname']

    # Restituisci i dati alla tabella
    return [{
        'best_selling': best_selling_product,
        'best_rated': best_rated_product
    }]

# SEZIONE 2.a Callback  ----------------------------
# Callback per aggiornare il grafico in base alla selezione di mese, anno e variabile
@app.callback(
    Output('weather-graph', 'figure'),
    [Input('month2-slider', 'value'),
     Input('year2-slider', 'value'),
     Input('weather-variable-dropdown', 'value')]
)
def update_graph(selected_month, selected_year, selected_variable):
    # Filtra i dati per il mese e l'anno selezionato
    filtered_df = df_weather[(df_weather['date'].dt.month == selected_month) & 
                             (df_weather['date'].dt.year == selected_year)]
    
    # Ottieni il massimo e il minimo della variabile selezionata
    max_value = filtered_df[selected_variable].max()
    min_value = filtered_df[selected_variable].min()

    # Crea il grafico lineare
    fig = go.Figure()

    # Aggiungi la linea per la variabile selezionata
    fig.add_trace(go.Scatter(
        x=filtered_df['date'],
        y=filtered_df[selected_variable],
        mode='lines',
        name=selected_variable.capitalize()
    ))

    # Evidenzia il valore massimo
    max_date = filtered_df[filtered_df[selected_variable] == max_value]['date'].iloc[0]
    fig.add_trace(go.Scatter(
        x=[max_date],
        y=[max_value],
        mode='markers+text',
        name='Max',
        text=f'Max: {max_value}',
        textposition="bottom right",
        marker=dict(color='red', size=10)
    ))

    # Evidenzia il valore minimo
    min_date = filtered_df[filtered_df[selected_variable] == min_value]['date'].iloc[0]
    fig.add_trace(go.Scatter(
        x=[min_date],
        y=[min_value],
        mode='markers+text',
        name='Min',
        text=f'Min: {min_value}',
        textposition="top right",
        marker=dict(color='blue', size=10)
    ))

    # Aggiorna il layout del grafico
    fig.update_layout(
        title=f'{selected_variable.capitalize()} in {selected_month}/{selected_year}',
        xaxis_title='Date',
        yaxis_title=f'{selected_variable.capitalize()} ({variable_units[selected_variable]})',
        hovermode='x'
    )

    return fig


# SEZIONE 3a Callback ------------------------------------------------

#pie-chart vendite -----------------------
@app.callback(
    Output('sales-pie-container', 'children'),
    [Input('month-dropdown', 'value')]
)
def update_sales_pie_chart(selected_month):
    df = fetch_data_for_dash(quantities_sold)
    # Filtra i dati in base al mese selezionato
    filtered_df = df[df['month'] == selected_month]
    
    if filtered_df.empty:
        # Restituisce un messaggio se non ci sono dati disponibili
        return html.Div(
            children=[
                html.H4(f"Nessun dato disponibile per {mesi[selected_month - 1]}", style={'color': 'red'}),
                html.P("Prova a selezionare un altro mese o attendi che i dati siano aggiornati.")
            ],
            style={'textAlign': 'center', 'margin': '50px', 'border': '1px solid #ddd', 'padding': '20px'}
        )
    
    # Crea il grafico a torta
    fig = px.pie(
        filtered_df, 
        values='totalquantity', 
        names='productname',
        title=f"Product Sales Distribution for {mesi[selected_month - 1]}",
        color_discrete_sequence=px.colors.qualitative.Plotly
    )
    return dcc.Graph(figure=fig)

# Callback per aggiornare il grafico a torta dei metodi di pagamento o mostrare un messaggio
@app.callback(
    Output('payment-method-pie-container', 'children'),
    [Input('month-dropdown', 'value')]
)
def update_payment_method_pie_chart(selected_month):
    df = fetch_data_for_dash(payment_methods_used)
    # Filtra i dati in base al mese selezionato
    filtered_df = df[df['month'] == selected_month]
    
    if filtered_df.empty:
        # Restituisce un messaggio se non ci sono dati disponibili
        return html.Div(
            children=[
                html.H4(f"Nessun dato disponibile per {mesi[selected_month - 1]}", style={'color': 'red'}),
                html.P("Prova a selezionare un altro mese o attendi che i dati siano aggiornati.")
            ],
            style={'textAlign': 'center', 'margin': '50px', 'border': '1px solid #ddd', 'padding': '20px'}
            
        )
    
    # Crea il grafico a torta
    fig = px.pie(
        filtered_df, 
        values='totaltransactions', 
        names='paymentmethod',
        title=f"Payment Method Distribution for {mesi[selected_month - 1]}",
        color_discrete_sequence=px.colors.sequential.Greens
    )
    return dcc.Graph(figure=fig)

#sezione 3.a linear-chart vendite -----------------------
@app.callback(
    Output('total-amount-line-chart-container', 'children'),
    [Input('month-dropdown2', 'value')]
)
def update_total_amount_line_chart(selected_month):
    df = fetch_data_for_dash(total_amounts_current_year)
    
    # Filtra i dati per il mese selezionato
    df['month'] = pd.to_datetime(df['date']).dt.month
    filtered_df = df[df['month'] == selected_month]
    
    if filtered_df.empty:
        # Mostra un messaggio se i dati non sono disponibili
        return html.Div(
            children=[
                html.H4(f"Dati non ancora disponibili per {mesi[selected_month - 1]}", style={'color': 'red'}),
                html.P("Prova a selezionare un altro mese o attendi che i dati siano aggiornati.")
            ],
            style={'textAlign': 'center', 'margin': '50px', 'border': '1px solid #ddd', 'padding': '20px'}
        )
    
    # Crea il grafico a linee
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=filtered_df['date'],
        y=filtered_df['total_amount'],
        mode='lines+markers',
        name='Total Amount',
        line=dict(color='green')
    ))
    
    # Evidenzia valori minimi e massimi
    min_value = filtered_df['total_amount'].min()
    max_value = filtered_df['total_amount'].max()
    
    fig.add_trace(go.Scatter(
        x=filtered_df['date'][filtered_df['total_amount'] == min_value],
        y=[min_value],
        mode='markers+text',
        name='Min',
        marker=dict(color='darkgreen', size=10),
        text=['Min'],
        textposition='bottom center'
    ))
    fig.add_trace(go.Scatter(
        x=filtered_df['date'][filtered_df['total_amount'] == max_value],
        y=[max_value],
        mode='markers+text',
        name='Max',
        marker=dict(color='lightgreen', size=10),
        text=['Max'],
        textposition='bottom center'
    ))

    # Calcola il totale dell'importo per il mese selezionato
    total_month_amount = filtered_df['total_amount'].sum()

    fig.update_layout(
        title=f"Importi Totali Transazioni per {mesi[selected_month - 1]}",
        xaxis_title="Data",
        yaxis_title="Importo Totale (€)"
    )

    # Restituisce il grafico e il totale del mese sotto al grafico
    return html.Div(
        children=[
            dcc.Graph(figure=fig),  # Grafico
            html.Div(
                children=f"Totale Importo per {mesi[selected_month - 1]}: €{total_month_amount:,.2f}",
                style={
                    'border': '2px solid green',  # Bordo verde
                    'padding': '10px',  # Spaziatura interna
                    'margin-top': '20px',  # Margine superiore
                    'textAlign': 'center',  # Testo centrato
                    'fontSize': '16px',  # Dimensione del font
                    'backgroundColor': '#f0f0f0',  # Colore di sfondo
                    'fontWeight': 'bold'  # Testo in grassetto
                }
            )
        ]
    )




def update_total_amount_line_chart(selected_month):
    df = fetch_data_for_dash(total_amounts_current_year)
    
    # Filter the data for the selected month
    df['month'] = pd.to_datetime(df['date']).dt.month
    filtered_df = df[df['month'] == selected_month]
    
    if filtered_df.empty:
        # Display a message if no data is available
        return html.Div(
            children=[
                html.H4(f"Dati non ancora disponibili per {mesi[selected_month - 1]}", style={'color': 'red'}),
                html.P("Prova a selezionare un altro mese o attendi che i dati siano aggiornati.")
            ],
            style={'textAlign': 'center', 'margin': '50px', 'border': '1px solid #ddd', 'padding': '20px'}
        )
    
    # Create a line chart
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=filtered_df['date'],
        y=filtered_df['total_amount'],
        mode='lines+markers',
        name='Total Amount',
        line=dict(color='green')
    ))
    
    # Highlight min and max values
    min_value = filtered_df['total_amount'].min()
    max_value = filtered_df['total_amount'].max()
    
    fig.add_trace(go.Scatter(
        x=filtered_df['date'][filtered_df['total_amount'] == min_value],
        y=[min_value],
        mode='markers+text',
        name='Min',
        marker=dict(color='darkgreen', size=10),
        text=['Min'],
        textposition='bottom center'
    ))
    fig.add_trace(go.Scatter(
        x=filtered_df['date'][filtered_df['total_amount'] == max_value],
        y=[max_value],
        mode='markers+text',
        name='Max',
        marker=dict(color='lightgreen', size=10),
        text=['Max'],
        textposition='bottom center'
    ))

    # Calculate total amount for the selected month
    total_month_amount = filtered_df['total_amount'].sum()

    fig.update_layout(
        title=f"Importi Totali Transazioni per {mesi[selected_month - 1]}",
        xaxis_title="Data",
        yaxis_title="Importo Totale (€)",
        annotations=[  # QUI !!! Aggiungi l'annotazione con il totale del mese
            {
                'x': 1.05,  # Posizione X sul grafico (oltre 1 è fuori dal grafico, a destra)
                'y': 0.5,   # Posizione Y sul grafico (0 è in basso, 1 è in alto)
                'xref': 'paper',  # Riferimento relativo al grafico
                'yref': 'paper',  # Riferimento relativo al grafico
                'text': f"Totale Mese: €{total_month_amount:,.2f}",  # Testo dell'annotazione con il totale
                'showarrow': False,  # Nessuna freccia
                'font': {
                    'size': 14,  # Dimensione del font
                    'color': 'black'  # Colore del testo
                },
                'align': 'left'
            }
        ]
    )

    return dcc.Graph(figure=fig)


# Callback for updating the quantity per transaction line chart
@app.callback(
    Output('quantity-line-chart-container', 'children'),
    [Input('month-dropdown2', 'value')]
)
def update_quantity_line_chart(selected_month):
    df = fetch_data_for_dash(quantity_per_transaction_current_year)
    
    # Filter the data for the selected month
    df['month'] = pd.to_datetime(df['date']).dt.month
    filtered_df = df[df['month'] == selected_month]
    
    if filtered_df.empty:
        # Display a message if no data is available
        return html.Div(
            children=[
                html.H4(f"Dati non ancora disponibili per {mesi[selected_month - 1]}", style={'color': 'red'}),
                html.P("Prova a selezionare un altro mese o attendi che i dati siano aggiornati.")
            ],
            style={'textAlign': 'center', 'margin': '50px', 'border': '1px solid #ddd', 'padding': '20px'}
        )
    
    # Create a line chart
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=filtered_df['date'],
        y=filtered_df['total_quantity'],
        mode='lines+markers',
        name='Total Quantity',
        line=dict(color='green')
    ))
    
    # Highlight min and max values
    min_value = filtered_df['total_quantity'].min()
    max_value = filtered_df['total_quantity'].max()
    
    fig.add_trace(go.Scatter(
        x=filtered_df['date'][filtered_df['total_quantity'] == min_value],
        y=[min_value],
        mode='markers+text',
        name='Min',
        marker=dict(color='darkgreen', size=10),
        text=['Min'],
        textposition='bottom center'
    ))
    fig.add_trace(go.Scatter(
        x=filtered_df['date'][filtered_df['total_quantity'] == max_value],
        y=[max_value],
        mode='markers+text',
        name='Max',
        marker=dict(color='lightgreen', size=10),
        text=['Max'],
        textposition='bottom center'
    ))

    fig.update_layout(
        title=f"Quantità per Transazione per {mesi[selected_month - 1]}",
        xaxis_title="Data",
        yaxis_title="Quantità Totale"
    )
    return dcc.Graph(figure=fig)

#Sezione 4a culture e piantagioni --------------------------------------------
@app.callback(
    Output('crop-table-container', 'children'),
    [Input('crop-dropdown', 'value')]
)
def update_crop_table(selected_crop):
    if not selected_crop:
        return html.Div("Seleziona una coltura per visualizzare i dettagli.")

    # Usa la query per ottenere i dettagli della coltura selezionata
    crop_data = fetch_data_for_dash(crop_details_query % (f"'{selected_crop}'"))
    
    if crop_data.empty:
        return html.Div("Nessun dato disponibile per la coltura selezionata.")
    
    # Trasponi i dati della tabella
    crop_data_transposed = crop_data.T.reset_index()
    crop_data_transposed.columns = ['Variabile', 'Valore']
    
    # Crea una tabella trasposta con colori molto chiari
    return dash_table.DataTable(
        data=crop_data_transposed.to_dict('records'),
        columns=[{'name': i, 'id': i} for i in crop_data_transposed.columns],
        style_header={'backgroundColor': '#f0fff0', 'fontWeight': 'bold', 'color': 'black'},
        style_cell={
            'backgroundColor': '#f8fff8',
            'color': 'black',
            'textAlign': 'center'
        },
        style_table={'width': '70%', 'margin': 'auto', 'border': '1px solid #e0ffe0'}
    )

#-----------
@app.callback(
    Output('weather-comparison-bar-charts', 'children'),
    [Input('crop-dropdown', 'value'), Input('month-dropdown', 'value')]
)
def update_weather_comparison_charts(selected_crop, selected_month):
    # Modificare le query per includere i parametri `selected_crop` e `selected_month`
    temperature_query = f"""
        SELECT 
            (SELECT OptimalTemperatureMin 
             FROM Crops 
             WHERE CropName = '{selected_crop}') AS mintemp,
            (SELECT OptimalTemperatureMax 
             FROM Crops 
             WHERE CropName = '{selected_crop}') AS maxtemp,
            (SELECT AVG(Temperature) 
             FROM WeatherConditions 
             WHERE EXTRACT(YEAR FROM Date) = 2024 
             AND EXTRACT(MONTH FROM Date) = {selected_month}) AS avgtemperature
    """

    humidity_query = f"""
        SELECT 
            (SELECT OptimalHumidityMin 
             FROM Crops 
             WHERE CropName = '{selected_crop}') AS minhumidity,
            (SELECT OptimalHumidityMax 
             FROM Crops 
             WHERE CropName = '{selected_crop}') AS maxhumidity,
            (SELECT AVG(Humidity) 
             FROM WeatherConditions 
             WHERE EXTRACT(YEAR FROM Date) = 2024 
             AND EXTRACT(MONTH FROM Date) = {selected_month}) AS avghumidity
    """

    days_in_month = pd.Period(f"2024-{selected_month:02d}").days_in_month
    precipitation_query = f"""
        SELECT 
            (SELECT OptimalPrecipitationMin 
             FROM Crops 
             WHERE CropName = '{selected_crop}') AS minprecipitation,
            (SELECT OptimalPrecipitationMax 
             FROM Crops 
             WHERE CropName = '{selected_crop}') AS maxprecipitation,
            (SELECT AVG(Precipitation) * {days_in_month} 
             FROM WeatherConditions 
             WHERE EXTRACT(YEAR FROM Date) = 2024 
             AND EXTRACT(MONTH FROM Date) = {selected_month}) AS precipitation
    """

    # Ottenere i dati utilizzando la funzione fetch_data_for_dash()
    df_temp = fetch_data_for_dash(temperature_query)
    df_hum = fetch_data_for_dash(humidity_query)
    df_prec = fetch_data_for_dash(precipitation_query)

    # I dati sono già filtrati in base a `selected_crop` e `selected_month` tramite le query
    temp_data = df_temp.iloc[0]
    hum_data = df_hum.iloc[0]
    prec_data = df_prec.iloc[0]

    # Creare il grafico per la Temperatura
    temp_fig = go.Figure(data=[
        go.Bar(name='Min Temp', x=['Temperature'], y=[temp_data['mintemp']], marker_color='darkgreen'),
        go.Bar(name='Avg Temp', x=['Temperature'], y=[temp_data['avgtemperature']], marker_color='green'),
        go.Bar(name='Max Temp', x=['Temperature'], y=[temp_data['maxtemp']], marker_color='lightgreen')
    ])
    temp_fig.update_layout(title='Temperature Comparison', yaxis_title='Temperature (°C)', barmode='group')

    # Creare il grafico per l'Umidità
    hum_fig = go.Figure(data=[
        go.Bar(name='Min Humidity', x=['Humidity'], y=[hum_data['minhumidity']], marker_color='darkgreen'),
        go.Bar(name='Avg Humidity', x=['Humidity'], y=[hum_data['avghumidity']], marker_color='green'),
        go.Bar(name='Max Humidity', x=['Humidity'], y=[hum_data['maxhumidity']], marker_color='lightgreen')
    ])
    hum_fig.update_layout(title='Humidity Comparison', yaxis_title='Humidity (%)', barmode='group')

    # Creare il grafico per le Precipitazioni
    prec_fig = go.Figure(data=[
        go.Bar(name='Min Precipitation', x=['Precipitation'], y=[prec_data['minprecipitation']], marker_color='darkgreen'),
        go.Bar(name='Avg Precipitation', x=['Precipitation'], y=[prec_data['precipitation']], marker_color='green'),
        go.Bar(name='Max Precipitation', x=['Precipitation'], y=[prec_data['maxprecipitation']], marker_color='lightgreen')
    ])
    prec_fig.update_layout(title='Precipitation Comparison', yaxis_title='Precipitation (mm)', barmode='group')

    # Ritorna i tre grafici in un layout orizzontale
    return [
    html.Div([
        dcc.Graph(figure=temp_fig, style={'width': '30%'}),
        dcc.Graph(figure=hum_fig, style={'width': '30%'}),
        dcc.Graph(figure=prec_fig, style={'width': '30%'})
    ], style={'display': 'flex', 'justify-content': 'space-around', 'align-items': 'center'})
]


# Callback Sezione 5 costi-------------------------------------------------------------
def fetch_checked_month(query, params):
    """
    Fetch data from the database given a query and parameters.
    Tries to find the nearest available data if the specific month isn't available.
    """
    # Esegui la query per ottenere i dati del mese richiesto
    df = fetch_data_for_dash2(query, params=params)
    
    # Se i dati del mese richiesto sono presenti, restituisci il dataframe
    if not df.empty:
        return df
    
    # Se non ci sono dati per il mese richiesto, cerca il mese precedente disponibile
    year, requested_month = params
    months_with_data_query = """
        SELECT DISTINCT EXTRACT(MONTH FROM date) AS month
        FROM Costs
        WHERE EXTRACT(YEAR FROM date) = %s
        ORDER BY month;
    """
    available_months_df = fetch_data_for_dash2(months_with_data_query, params=(year,))
    available_months = available_months_df['month'].tolist()
    
    # Trova il mese disponibile più vicino
    nearest_month = max([month for month in available_months if month <= requested_month], default=None)
    
    # Se non c'è un mese precedente, usa il primo mese disponibile dopo quello richiesto
    if nearest_month is None:
        nearest_month = min(available_months, default=requested_month)
    
    # Esegui di nuovo la query con il mese più vicino disponibile
    return fetch_data_for_dash2(query, params=(year, nearest_month))

@app.callback(
    Output('monthly-cost-pie-chart-container', 'children'),  # Cambiato per il nuovo layout
    [Input('month5-dropdown', 'value')]
)
def update_cost_pie_chart(selected_month):
    year = 2024

    # Esegui le query
    df_costs = fetch_checked_month(costs_query, (year, selected_month))
    df_salaries = fetch_data_for_dash(salariescost_query)
    df_precipitation = fetch_data_for_dash2(precipitationcost_query, (year, selected_month))
    
    # Controlla se i dati non sono disponibili
    if df_costs.empty or df_salaries.empty or df_precipitation.empty:
        return html.Div(
            children=[
                html.H4(f"Dati non ancora disponibili per {mesi[selected_month - 1]}", style={'color': 'red'}),
                html.P("Prova a selezionare un altro mese o attendi che i dati siano aggiornati.")
            ],
            style={'textAlign': 'center', 'margin': '50px', 'border': '1px solid #ddd', 'padding': '20px'}
        )
    
    # Dati estratti dalle query
    water_cost = df_costs['totalwatercost'].iloc[0]
    energy_cost = df_costs['totalenergycost'].iloc[0]
    fertilizer_cost = df_costs['totalfertilizercost'].iloc[0]
    total_salaries = df_salaries['totalsalaries'].iloc[0]
    monthly_precipitation = df_precipitation['monthlyprecipitation'].iloc[0]

    

    # Consumi generati attraverso metodi statistici
    consumed_en = generate_energy_consumption()
    consumed_wa = generate_water_consumption()
    consumed_pe = generate_pesticide_use()
    rainfall = calculate_from_rainfall(monthly_precipitation)

    # Calcolare i costi mensili
    water_month_cost = water_cost * (consumed_wa - rainfall) * random.uniform(0.95, 1.05) / 12
    energy_month_cost = energy_cost * consumed_en * random.uniform(0.95, 1.05) / 8
    pesticide_month_cost = fertilizer_cost * consumed_pe * random.uniform(0.95, 1.05) / 10
    total_salaries = total_salaries / 14  # 14 mensilità pagate

    # Calcolare altre spese
    altre_spese = random.uniform(0, 1700)
    totalcosts = water_month_cost + energy_month_cost + pesticide_month_cost + altre_spese + total_salaries

    # Crea la sezione con il totale delle spese
    total_cost_section = html.Div(
        children=[
            html.H4(f"Totale spese per {mesi[selected_month - 1]}: €{totalcosts:,.2f}", style={'color': 'green'})
        ],
        style={'textAlign': 'center', 'margin': '20px', 'border': '1px solid #ddd', 'padding': '10px'}
    )
    
    # Creare il grafico a torta
    fig = px.pie(
        names=['Totale Stipendi', 'Costo Acqua', 'Costo Energia', 'Costo Pesticidi', 'Altre Spese'],
        values=[total_salaries, water_month_cost, energy_month_cost, pesticide_month_cost, altre_spese],
        title=f"Costi mensili per {mesi[selected_month - 1]}",
        color_discrete_sequence=px.colors.sequential.Greens
    )
    
    # Restituisce il grafico a torta e la sezione con il totale delle spese
    return html.Div(
        children=[
            dcc.Graph(figure=fig),
            total_cost_section
        ]
    )




# Run the app ----------------------------------------------------------------------
if __name__ == '__main__':
    app.run_server(debug=True)
