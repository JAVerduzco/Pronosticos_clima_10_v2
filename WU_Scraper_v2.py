import streamlit as st
import requests
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Pronóstico 10 días", layout="wide")

# Título
st.title("🌤️ Pronóstico del tiempo - 10 días")

# Coordenadas y nombres de ciudades
urls_ciudades = [
    'https://api.weather.com/v3/wx/forecast/daily/10day?apiKey=TU_API_KEY&geocode=30.496%2C-112.323&units=m&language=en-US&format=json',  # Caborca
    'https://api.weather.com/v3/wx/forecast/daily/10day?apiKey=TU_API_KEY&geocode=29.1%2C-110.951&units=m&language=en-US&format=json',    # Hermosillo
    'https://api.weather.com/v3/wx/forecast/daily/10day?apiKey=TU_API_KEY&geocode=27.471%2C-109.929&units=m&language=en-US&format=json',  # Obregón
    'https://api.weather.com/v3/wx/forecast/daily/10day?apiKey=TU_API_KEY&geocode=25.792%2C-108.992&units=m&language=en-US&format=json',  # Los Mochis
    'https://api.weather.com/v3/wx/forecast/daily/10day?apiKey=TU_API_KEY&geocode=24.782%2C-107.395&units=m&language=en-US&format=json'   # Culiacán
]
ciudades = ['CAB', 'HMO', 'OBR', 'LMO', 'CUL']

# Obtener datos desde la API
@st.cache_data(show_spinner=True, ttl=3600)  # Cachea por 1 hora
def obtener_datos_actualizados():
    datos_ciudades = []
    for url in urls_ciudades:
        try:
            response = requests.get(url)
            datos = response.json()
            datos_ciudades.append(datos)
        except Exception as e:
            st.error(f"Error al obtener datos de la API: {e}")
            return None
    return datos_ciudades

# Formateo de fecha
def formato_fecha(fechas):
    parsed_date = datetime.strptime(fechas, '%Y-%m-%dT%H:%M:%S%z')
    return parsed_date.strftime('%Y-%m-%d')

# Procesar datos
datos_ciudades = obtener_datos_actualizados()
if datos_ciudades:
    df = pd.DataFrame()

    for i, datos in enumerate(datos_ciudades):
        ciudad = ciudades[i]
        df[f'{ciudad}_TempMax'] = datos['calendarDayTemperatureMax']
        df[f'{ciudad}_TempMin'] = datos['calendarDayTemperatureMin']
        if i != 0:
            df[f'{ciudad}_QPF'] = datos['qpf']

    # Fechas desde primera ciudad
    fechas = datos_ciudades[0]['validTimeLocal']
    formatted_dates = [formato_fecha(date) for date in fechas]
    df.index = formatted_dates

    # Mostrar tabla
    st.subheader("📋 Tabla de Pronóstico")
    st.dataframe(df[:-1], use_container_width=True)

    # Descargar CSV
    csv = df.to_csv(index=True).encode('utf-8')
    st.download_button(
        label="⬇️ Descargar CSV",
        data=csv,
        file_name='PronTemp10dias.csv',
        mime='text/csv'
    )
else:
    st.warning("No se pudieron obtener los datos.")
