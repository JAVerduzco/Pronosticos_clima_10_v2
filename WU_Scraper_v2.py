import streamlit as st
import requests
import pandas as pd
from datetime import datetime

# Título de la aplicación
st.title("🌤️ Pronóstico del tiempo - 10 días")

# Lista de URLs y ciudades
urls_ciudades = [
    'https://api.weather.com/v3/wx/forecast/daily/10day?apiKey=TU_API_KEY&geocode=30.496%2C-112.323&units=m&language=en-US&format=json',  # Caborca
    'https://api.weather.com/v3/wx/forecast/daily/10day?apiKey=TU_API_KEY&geocode=29.1%2C-110.951&units=m&language=en-US&format=json',    # Hermosillo
    'https://api.weather.com/v3/wx/forecast/daily/10day?apiKey=TU_API_KEY&geocode=27.471%2C-109.929&units=m&language=en-US&format=json',  # Obregón
    'https://api.weather.com/v3/wx/forecast/daily/10day?apiKey=TU_API_KEY&geocode=25.792%2C-108.992&units=m&language=en-US&format=json',  # Los Mochis
    'https://api.weather.com/v3/wx/forecast/daily/10day?apiKey=TU_API_KEY&geocode=24.782%2C-107.395&units=m&language=en-US&format=json'   # Culiacán
]
ciudades = ['CAB', 'HMO', 'OBR', 'LMO', 'CUL']

def obtener_datos(url):
    response = requests.get(url)
    data = response.json()
    return data

df = pd.DataFrame()

# Primer ciclo: temperaturas máximas
for i, url in enumerate(urls_ciudades):
    datos = obtener_datos(url)
    if datos:
        df[f'{ciudades[i]}_TempMax'] = datos['calendarDayTemperatureMax']

# Segundo ciclo: temperaturas mínimas
for i, url in enumerate(urls_ciudades):
    datos = obtener_datos(url)
    if datos:
        df[f'{ciudades[i]}_TempMin'] = datos['calendarDayTemperatureMin']

# Tercer ciclo: QPF (excepto para la primera ciudad)
for i, url in enumerate(urls_ciudades):
    datos = obtener_datos(url)
    if datos:
        if i == 0:
            continue
        else:
            df[f'{ciudades[i]}_QPF'] = datos['qpf']

# Fechas
fechas = obtener_datos(urls_ciudades[0])['sunriseTimeLocal']

# Formato de fecha
def formato_fecha(fechas):
    parsed_date = datetime.strptime(fechas, '%Y-%m-%dT%H:%M:%S%z')
    return parsed_date.strftime('%Y-%m-%d')

formatted_dates = [formato_fecha(date) for date in fechas]

# Índices
df.index = formatted_dates

# Eliminar último registro
df = df[:-1]

# Mostrar tabla
st.subheader("📋 Tabla de datos")
st.dataframe(df, use_container_width=True)

# Descargar CSV
csv = df.to_csv().encode('utf-8')
st.download_button(
    label="⬇️ Descargar CSV",
    data=csv,
    file_name='PronTemp10dias.csv',
    mime='text/csv'
)
