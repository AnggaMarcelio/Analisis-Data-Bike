import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load data
df = pd.read_csv("day.csv")

# Konversi kolom 'dteday' menjadi format datetime
df['dteday'] = pd.to_datetime(df['dteday'])

# Sidebar untuk navigasi menu
st.sidebar.title("Menu")
menu = st.sidebar.selectbox("Pilih Visualisasi", [
    "Tren Penggunaan Sepeda Bulanan", 
    "Perbandingan Weekday vs Weekend", 
    "Distribusi Kategori Penggunaan per Musim",
    "Visualisasi Faktor Cuaca"
])

# Filter berdasarkan rentang tanggal
st.sidebar.subheader("Filter Data")
start_date = st.sidebar.date_input("Tanggal mulai", df['dteday'].min())
end_date = st.sidebar.date_input("Tanggal akhir", df['dteday'].max())
filtered_df = df[(df['dteday'] >= pd.to_datetime(start_date)) & (df['dteday'] <= pd.to_datetime(end_date))]

# Filter berdasarkan musim
season_filter = st.sidebar.multiselect("Pilih Musim", options=df['season'].unique(), default=df['season'].unique())
filtered_df = filtered_df[filtered_df['season'].isin(season_filter)]

# Visualisasi 1: Tren Penggunaan Sepeda Bulanan
if menu == "Tren Penggunaan Sepeda Bulanan":
    st.subheader("Tren Penggunaan Sepeda Bulanan")
    plt.figure(figsize=(12, 6))
    sns.lineplot(x='mnth', y='cnt', data=filtered_df, marker='o')
    plt.title('Tren Penggunaan Sepeda Bulanan')
    plt.xlabel('Bulan')
    plt.ylabel('Rata-rata Penyewaan')
    st.pyplot(plt)

# Visualisasi 2: Perbandingan Weekday vs Weekend
elif menu == "Perbandingan Weekday vs Weekend":
    st.subheader("Perbandingan Penggunaan Weekday vs Weekend")
    plt.figure(figsize=(6, 6))
    sns.boxplot(x='workingday', y='cnt', data=filtered_df)
    plt.title('Perbandingan Penggunaan Weekday vs Weekend')
    st.pyplot(plt)

# Visualisasi 3: Distribusi Kategori Penggunaan per Musim
elif menu == "Distribusi Kategori Penggunaan per Musim":
    st.subheader("Distribusi Kategori Penggunaan per Musim")
    filtered_df['usage_category'] = pd.qcut(filtered_df['cnt'], q=3, labels=['Rendah', 'Sedang', 'Tinggi'])
    plt.figure(figsize=(10, 5))
    sns.countplot(x='season', hue='usage_category', data=filtered_df, palette='viridis')
    plt.title('Distribusi Kategori Penggunaan per Musim')
    st.pyplot(plt)

# Visualisasi 4: Visualisasi Faktor Cuaca
elif menu == "Visualisasi Faktor Cuaca":
    st.subheader("Visualisasi Faktor Cuaca")
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))

    sns.scatterplot(x='temp', y='cnt', data=filtered_df, ax=axes[0])
    axes[0].set_title("Hubungan Suhu dengan Jumlah Penyewaan")

    sns.scatterplot(x='hum', y='cnt', data=filtered_df, ax=axes[1])
    axes[1].set_title("Hubungan Kelembapan dengan Jumlah Penyewaan")

    sns.boxplot(x='weathersit', y='cnt', data=filtered_df, ax=axes[2])
    axes[2].set_title("Distribusi Penyewaan Berdasarkan Kondisi Cuaca")

    plt.tight_layout()
    st.pyplot(fig)
