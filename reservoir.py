import streamlit as st
import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
from PIL import Image

# Imagen Banner

# Abrir la imagen original
img = Image.open("An interactive tool for analyzing.png")

# Redimensionar la imagen al tamaño deseado (1128 x 191 píxeles)
img = img.resize((1128, 191))

# Guardar la imagen redimensionada
img.save("linkedin_banner.png")

# Mostrar la imagen redimensionada en Streamlit
st.image("linkedin_banner.png", use_column_width=True)

# Start Here
st.subheader("Production Wells Analysis")

#load data
df_production = pd.read_excel('Volve production data.xlsx', sheet_name='Daily Production Data')

# Procesamiento de datos

# Filtrar solo los pozos productores
df_production = df_production[df_production['WELL_TYPE'] == 'OP']

# Asegúrate de que el formato de fecha sea el correcto para la visualización
df_production['DATEPRD'] = df_production['DATEPRD'].dt.date

# Ordenar las fechas
dates = sorted(df_production['DATEPRD'].unique())

# Selector de fecha en la aplicación
selected_date = st.select_slider("Please Select a Date", options=dates, format_func=lambda x: x.strftime('%d/%m/%Y'))

# Filtrar el DataFrame para la fecha seleccionada
df_filtered = df_production[df_production['DATEPRD'] == pd.to_datetime(selected_date, format='%d/%m/%Y').date()]

# Cálculos de totales para la fecha seleccionada
total_oil = round(df_filtered['BORE_OIL_VOL'].sum(), 2)
total_gas = round(df_filtered['BORE_GAS_VOL'].sum(), 2)
total_water = round(df_filtered['BORE_WAT_VOL'].sum(), 2)

# Mostrar los totales calculados en la aplicación
c1, c2, c3 = st.columns(3)
c1.metric("Total Oil Production", total_oil)
c2.metric("Total Gas Production", total_gas)
c3.metric("Total Water Production", total_water)

# Crear pestañas para las vistas básica y de datos
t1, t2 = st.tabs(["Basic View", "Data View"])

# Mostrar el DataFrame filtrado en la pestaña de vista de datos
t2.dataframe(df_filtered)

# Filtrar el DataFrame para la fecha seleccionada antes de crear cada gráfico de línea
df_date_filtered = df_production[df_production['DATEPRD'] <= pd.to_datetime(selected_date, format='%d/%m/%Y').date()]

# Gráfico de línea para la producción de petróleo
fig1 = px.line(df_date_filtered, x="DATEPRD", y="BORE_OIL_VOL", color="NPD_WELL_BORE_NAME", title='Oil Production Over Time')
t1.plotly_chart(fig1, use_container_width=True)

# Gráfico de línea para la producción de gas
fig2 = px.line(df_date_filtered, x="DATEPRD", y="BORE_GAS_VOL", color="NPD_WELL_BORE_NAME", title='Gas Production Over Time')
t1.plotly_chart(fig2, use_container_width=True)

# Gráfico de línea para la producción de agua
fig3 = px.line(df_date_filtered, x="DATEPRD", y="BORE_WAT_VOL", color="NPD_WELL_BORE_NAME", title='Water Production Over Time')
t1.plotly_chart(fig3, use_container_width=True)

#Grafico de dispersion
df_filtered ["HI_OIL"] = 1 - (df_filtered .BORE_OIL_VOL / df_filtered .BORE_OIL_VOL.mean())
df_filtered ["HI_WATER"] = 1 - (df_filtered .BORE_WAT_VOL / df_filtered .BORE_WAT_VOL.mean())

df_filtered  = df_filtered .dropna(subset=["BORE_GAS_VOL"])
fig4 = px.scatter(df_filtered , x="HI_OIL", y="HI_WATER", color="NPD_WELL_BORE_NAME", size="BORE_GAS_VOL", 
                  title="Normalized Oil and Water Production Indices with Gas Volume", template="plotly")
st.plotly_chart(fig4, use_container_width=True)
