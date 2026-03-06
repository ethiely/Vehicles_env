import pandas as pd
import plotly.express as px
import streamlit as st
import numpy as np
        
market_data = pd.read_csv('global_market.csv') # lendo os dados

st.header('Exploratory Analysis - Global EV Market up to 2026') # título da aplicação

# Criando gráfico de barras para vendas por marca

st.subheader("Total EV Sales by Brand")
st.markdown("This chart allows us to compare and identify which brands are   leading the market in terms of sales, providing insights   into consumer preferences and market trends")  
    
sales_brand = (
    market_data
    .groupby("ev_brand")["ev_sales_units"]
    .sum()
    .reset_index()
)

fig = px.bar(
    sales_brand,
    x="ev_brand",
    y="ev_sales_units",
    title=" ",
    color="ev_brand")

st.plotly_chart(fig, use_container_width=True)

#criando gráfico de barras para vendas por região
st.subheader("Total EV Sales by Region")
hist_button = st.button('Click to generate a histogram for total sales') # criar um botão
        
if hist_button:
    st.write('Creating a histogram for the total sales of EVs by region')
sales_region = (
    market_data
    .groupby("region")["ev_sales_units"]
    .sum()
    .reset_index()
)

fig = px.bar(
    sales_region,
    x="region",
    y="ev_sales_units",
    color="region",
    title="We are able to compare the performance of different regions in the global EV market"
)

st.plotly_chart(fig, use_container_width=True)

#Criando gráfico de dispersão para comparar tempo de carregamento e alcance do veículo por marca
st.subheader("Charging Time vs Vehicle Range by EV Brand")
brands = market_data["ev_brand"].unique()
selected_brand = st.selectbox("Select EV Brand", brands)


filtered_data = market_data[market_data["ev_brand"] == selected_brand]


disp_button = st.button('Create Scatter Plot', key="scatter_button")

if disp_button:
    st.write(f'Creating a scatter plot for {selected_brand}')

    # criar bins de 100 km
    max_range = filtered_data["vehicle_range_km"].max()
    bins = np.arange(0, max_range + 100, 100)

    filtered_data["range_bin"] = pd.cut(
        filtered_data["vehicle_range_km"],
        bins=bins
    )

    fig = px.scatter(
        filtered_data,
        x="charging_time_hours",
        y="vehicle_range_km",
        color="range_bin",
        title=f"Comparison of Charging Time and Vehicle Range - {selected_brand}"
    )

    st.plotly_chart(fig, use_container_width=True)



#Criando gráfico de histograma para distribuição do alcance dos veículos elétricos
st.subheader("Distribution of EV Vehicle Range")

fig = px.histogram(
    market_data,
    x="vehicle_range_km",
    nbins=20,
    color="vehicle_type",
    title="This histogram shows the distribution of vehicle range (in km) for different types of EVs"
)

st.plotly_chart(fig, use_container_width=True) 






#Criando gráfico de dispersão para comparar estações de carregamento e vendas de EV por região
st.subheader("Charging Stations vs EV Sales by Region")

agg_data = (
    market_data
    .groupby("region")[["charging_stations", "ev_sales_units"]]
    .sum()
    .reset_index()
)

fig = px.scatter(
    agg_data,
    x="charging_stations",
    y="ev_sales_units",
    color="region",
    size="ev_sales_units",
    title="Is the infrastructure of charging stations driving EV sales?")
st.markdown("This scatter plot allows us to analyze the relationship between the availability of   charging stations and EV sales across different regions,   providing insights into how infrastructure may influence   consumer adoption of electric vehicles.")

st.plotly_chart(fig, use_container_width=True)

 # criando gráfico de heatmap para vendas por marca e tipo de veículo
st.subheader("EV Sales by Brand and Vehicle Type")

# agrupar vendas
sales_data = (
    market_data
    .groupby(["ev_brand", "vehicle_type"])["ev_sales_units"]
    .sum()
    .reset_index()
)

# criar pivot table
heatmap_data = sales_data.pivot(
    index="vehicle_type",
    columns="ev_brand",
    values="ev_sales_units"
)

# criar heatmap
fig = px.imshow(
    heatmap_data,
    labels=dict(x="EV Brand", y="Vehicle Type", color="Sales Units"),
    title="This heatmap allows us to identify which combinations are most popular",
    color_continuous_scale="Blues"
    )

st.plotly_chart(fig, use_container_width=True)
