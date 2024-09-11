import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import geopandas as gpd
from shapely.geometry import Point
from geopandas import GeoDataFrame
import streamlit as st
from pathlib import Path

def show_top_category(df):
    colors = ['grey' if value != max(df['product_id'].head(10)) else 'blue' for value in df['product_id'].head(10)]

    plt.figure(figsize=(10, 6))
    ax = sns.barplot(x='product_category_name_english', y='product_id', data=df.head(10), palette=colors, legend=False, hue='product_category_name_english')

    for container in ax.containers:
        ax.bar_label(container)

    plt.xlabel('Kategori Produk')
    plt.ylabel('Jumlah Produk')
    plt.xticks(rotation=45)

    st.pyplot(plt)

def show_bottom_category(df):
    colors = ['grey' if value != min(df['product_id'].tail(10)) else 'red' for value in df['product_id'].tail(10)]

    plt.figure(figsize=(10, 6))
    ax = sns.barplot(x='product_category_name_english', y='product_id', data=df.tail(10), palette=colors, legend=False, hue='product_category_name_english')

    for container in ax.containers:
        ax.bar_label(container)

    plt.xlabel('Kategori Produk')
    plt.ylabel('Jumlah Produk')
    plt.xticks(rotation=45)

    st.pyplot(plt)

def show_payments_pie_chart(df):
    colors = ['#ff9999','#66b3ff','#99ff99','#ffcc99','#c2c2f0']

    plt.figure(figsize=(10, 6))
    plt.pie(df['order_id'], colors=colors, autopct='%1.1f%%', startangle=140, pctdistance=0.85)

    centre_circle = plt.Circle((0,0),0.50,fc='white')
    fig = plt.gcf()
    fig.gca().add_artist(centre_circle)

    plt.legend(df['payment_type'], loc="best")
    plt.tight_layout()

    st.pyplot(plt)

def show_marker_map(df):
    geometry = [Point(xy) for xy in zip(df['geolocation_lng'], df['geolocation_lat'])]
    gdf = gpd.GeoDataFrame(df, geometry=geometry)

    gdf.set_crs(epsg=4326, inplace=True)

    world = gpd.read_file(parent_dir/'main_data\country_map\\ne_10m_admin_0_countries.shp')

    brazil = world[world.SOVEREIGNT == 'Brazil']

    ax = brazil.plot(figsize=(20, 20))

    gdf.plot(ax=ax, 
            column='customer_id', 
            cmap='magma', 
            markersize=gdf['customer_id'] / 4, 
            alpha=0.4, 
            legend=True,
    )

    for x, y, label, label_val in zip(gdf['geolocation_lng'], gdf['geolocation_lat'], gdf['state_name'], gdf['customer_id']):
        plt.annotate(f'{label} ({label_val})', xy=(x, y), xytext=(3, 3), textcoords="offset points")

    st.pyplot(plt)

def show_top_city(df):
    colors = ['grey' if value != max(df['order_id'].head(10)) else 'blue' for value in df['order_id'].head(10)]

    plt.figure(figsize=(10, 6))
    ax = sns.barplot(x='customer_city', y='order_id', data=df.head(10), palette=colors, legend=False, hue='customer_city')

    for container in ax.containers:
        ax.bar_label(container)

    plt.xlabel('Kota')
    plt.ylabel('Jumlah Pemesanan')
    plt.xticks(rotation=45)

    st.pyplot(plt)  

def show_top_category_in_state(df, state_name):
    # Filter berdasarkan state_name
    filtered_df = df[df['state_name'] == state_name]
    
    filtered_df = filtered_df.head(5) if len(filtered_df) >= 5 else filtered_df.head(3) if len(filtered_df) >= 3 else filtered_df.head(1)
    
    # Menentukan warna khusus untuk nilai y paling tinggi
    colors = ['grey' if value != max(filtered_df['product_id']) else 'blue' for value in filtered_df['product_id']]
    
    plt.figure(figsize=(10, 6))
    ax = sns.barplot(x='product_category_name_english', y='product_id', data=filtered_df, palette=colors, legend=False, hue='product_category_name_english')
    
    for container in ax.containers:
        ax.bar_label(container)
    
    plt.xlabel('Kategori Produk')
    plt.ylabel('Jumlah Produk')
    plt.xticks(rotation=45)
    
    st.pyplot(plt)

parent_dir = Path(__file__).parents[0]

items_orders_products_payments_df = pd.read_csv(parent_dir/'main_data/items_orders_products_data.csv')
state_mark_customer_count_df = pd.read_csv(parent_dir/'main_data\state_mark_customer_count_data.csv')
order_city_count_df = pd.read_csv(parent_dir/'main_data\order_city_count_data.csv')
product_in_state = pd.read_csv(parent_dir/'main_data\product_in_state_data.csv').sort_values(by='product_id', ascending=False)

products_count_df = items_orders_products_payments_df.groupby(by='product_category_name_english').product_id.nunique().sort_values(ascending=False).reset_index()
payments_type_count = items_orders_products_payments_df.groupby(by='payment_type').order_id.nunique().sort_values(ascending=False).reset_index()

state_names = {
    'AC': 'Acre', 'AL': 'Alagoas', 'AM': 'Amazonas', 'AP': 'Amapá', 'BA': 'Bahia', 'CE': 'Ceará', 'DF': 'Distrito Federal', 'ES': 'Espírito Santo', 'GO': 'Goiás', 'MA': 'Maranhão', 'MG': 'Minas Gerais', 'MS': 'Mato Grosso do Sul', 'MT': 'Mato Grosso', 'PA': 'Pará', 'PB': 'Paraíba', 'PE': 'Pernambuco', 'PI': 'Piauí', 'PR': 'Paraná', 'RJ': 'Rio de Janeiro', 'RN': 'Rio Grande do Norte', 'RO': 'Rondônia', 'RR': 'Roraima', 'RS': 'Rio Grande do Sul', 'SC': 'Santa Catarina', 'SE': 'Sergipe', 'SP': 'São Paulo', 'TO': 'Tocantins'
}

state_mark_customer_count_df['state_name'] = state_mark_customer_count_df['customer_state'].map(state_names)

st.header('Proyek Analisis Data: E-Commerce Public Dataset')

st.subheader('Performa Penjualan Berdasarkan Kategori Produk')
col1, col2 = st.columns(2)

with col1:
    st.markdown('#### Kategori Produk Penjualan Terbanyak')
    show_top_category(products_count_df)

with col2:
    st.markdown('#### Kategori Produk Penjualan Paling Sedikit')
    show_bottom_category(products_count_df)

st.subheader('Kategori Produk Terbanyak Berdasarkan State')

city_name = st.selectbox(
    label="Pilih State",
    options=(product_in_state['state_name'].unique().tolist()),
    index=0,
)
show_top_category_in_state(product_in_state, city_name)

st.subheader("Metode Pembayaran yang digunakan Pelanggan")
show_payments_pie_chart(payments_type_count)

st.subheader('Sebaran Jumlah Pelanggan berdasarkan State')
show_marker_map(state_mark_customer_count_df)

st.subheader('Kota Terbanyak yang melakukan pemesanan barang')
show_top_city(order_city_count_df)
