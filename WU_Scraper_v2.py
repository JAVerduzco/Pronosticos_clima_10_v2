import streamlit as st
import pandas as pd
import requests
from datetime import datetime

st.set_page_config(layout='wide')
st.header("Pronósticos a 10 días")

urls_ciudades = [
    'https://api.weather.com/v3/wx/forecast/daily/10day?apiKey=e1f10a1e78da46f5b10a1e78da96f525&geocode=30.496%2C-112.323&units=m&language=en-US&format=json',  # Caborca
    'https://api.weather.com/v3/wx/forecast/daily/10day?apiKey=e1f10a1e78da46f5b10a1e78da96f525&geocode=29.1%2C-110.951&units=m&language=en-US&format=json',    # Hermosillo
    'https://api.weather.com/v3/wx/forecast/daily/10day?apiKey=e1f10a1e78da46f5b10a1e78da96f525&geocode=27.471%2C-109.929&units=m&language=en-US&format=json',  # Obregon
    'https://api.weather.com/v3/wx/forecast/daily/10day?apiKey=e1f10a1e78da46f5b10a1e78da96f525&geocode=25.792%2C-108.992&units=m&language=en-US&format=json',  # Los Mochis
    'https://api.weather.com/v3/wx/forecast/daily/10day?apiKey=e1f10a1e78da46f5b10a1e78da96f525&geocode=24.782%2C-107.395&units=m&language=en-US&format=json'   # Culiacan
]
ciudades = ['CAB', 'HMO', 'OBR', 'LMO', 'CUL']

def obtener_datos(url):
    response = requests.get(url)
    data = response.json()
    return data

df = pd.DataFrame()

for i, url in enumerate(urls_ciudades):
    datos = obtener_datos(url)
    if datos:  # Solo procesar si se obtuvieron datos
        df[f'{ciudades[i]}_TempMax'] = datos['calendarDayTemperatureMax']  # Valores correspondientes a la key 'calendarDayTemperatureMax'

for i, url in enumerate(urls_ciudades):
    datos = obtener_datos(url)
    if datos:  # Solo procesar si se obtuvieron datos
        df[f'{ciudades[i]}_TempMin'] = datos['calendarDayTemperatureMin']  # Valores correspondientes a la key 'calendarDayTemperatureMin'

for i, url in enumerate(urls_ciudades):
    datos = obtener_datos(url)
    if datos:  # Solo procesar si se obtuvieron datos
        if i == 0:
            continue
        else:
            df[f'{ciudades[i]}_QPF'] = datos['qpf']  # Valores correspondientes a la key 'qpf'

fechas = obtener_datos(urls_ciudades[0])['sunriseTimeLocal']

# Function para formatear fechas
def formato_fecha(fechas):
    parsed_date = datetime.strptime(fechas, '%Y-%m-%dT%H:%M:%S%z')
    return parsed_date.strftime('%Y-%m-%d')

# Aplicar la function a la lista
formatted_dates = [formato_fecha(date) for date in fechas]

# Asignar las fechas como índices
df.index = formatted_dates

df = df[:-1]

# Impresión de tabla en pantalla
st.dataframe(df, use_container_width=True)
