import streamlit as st
import pandas as pd
import geopandas as gpd
import folium
from streamlit_folium import st_folium
import matplotlib.pyplot as plt
import seaborn as sns

# =============================
# Pengaturan awal aplikasi
# =============================
st.set_page_config(
    page_title="Dashboard Potensi Desa Indonesia",
    layout="wide",
    page_icon="🌾"
)

st.title("🌾 Dashboard Potensi Desa di Indonesia")
st.markdown("Analisis dan visualisasi data potensi desa berdasarkan **lembaga pelatihan** di setiap provinsi.")

# =============================
# 1. Data Provinsi Langsung di Kode
# =============================
data = {
    "Provinsi": [
        "Aceh", "Sumatera Utara", "Sumatera Barat", "Riau", "Jambi", "Sumatera Selatan",
        "Bengkulu", "Lampung", "Bangka Belitung", "Kepulauan Riau", "DKI Jakarta",
        "Jawa Barat", "Jawa Tengah", "DI Yogyakarta", "Jawa Timur", "Banten",
        "Bali", "Nusa Tenggara Barat", "Nusa Tenggara Timur", "Kalimantan Barat",
        "Kalimantan Tengah", "Kalimantan Selatan", "Kalimantan Timur", "Kalimantan Utara",
        "Sulawesi Utara", "Sulawesi Tengah", "Sulawesi Selatan", "Sulawesi Tenggara",
        "Gorontalo", "Maluku", "Maluku Utara", "Papua Barat", "Papua"
    ],
    "Bahasa_Asing": [
        120, 95, 88, 105, 64, 82, 51, 70, 43, 38, 65, 142, 130, 75, 160, 78,
        54, 58, 60, 52, 48, 66, 55, 40, 50, 45, 71, 49, 37, 30, 28, 24, 26
    ],
    "Komputer": [
        200, 180, 160, 175, 140, 150, 130, 160, 95, 90, 120, 250, 230, 200, 270, 210,
        190, 170, 150, 145, 138, 120, 115, 110, 100, 98, 130, 125, 90, 70, 65, 60, 55
    ],
    "Menjahit": [
        180, 150, 140, 155, 120, 130, 100, 110, 88, 80, 100, 210, 195, 160, 220, 170,
        130, 120, 115, 105, 95, 100, 98, 92, 84, 75, 108, 100, 78, 65, 60, 58, 50
    ],
    "Total_Lembaga": [
        500, 425, 388, 435, 324, 362, 281, 340, 226, 208, 285, 602, 555, 435, 650, 458,
        374, 348, 325, 302, 281, 286, 268, 242, 234, 218, 309, 274, 205, 165, 153, 142, 131
    ],
    "Persentase_Desa_Dengan_Lembaga": [
        48.5, 42.0, 38.7, 40.2, 35.5, 37.1, 30.2, 33.5, 28.3, 26.9, 32.0, 60.2, 55.4, 43.7, 63.1, 44.2,
        38.9, 36.0, 33.1, 31.5, 30.4, 29.8, 28.2, 25.0, 24.8, 23.7, 27.9, 26.4, 21.2, 18.5, 17.0, 16.1, 15.4
    ],
    "Latitude": [
        4.6951, 2.1154, -0.7399, 0.2933, -1.4852, -3.3194, -3.5778, -5.4500, -2.7411, 3.9457,
        -6.2088, -6.9147, -7.1509, -7.7956, -7.5361, -6.4058, -8.4095, -8.6529, -8.6574,
        -0.2788, -1.6815, -3.0926, 0.8033, 3.0150, 1.4931, -0.8995, -5.1197, -4.1450,
        0.5435, -3.2385, 1.5700, -1.3361, -4.2699
    ],
    "Longitude": [
        96.7494, 99.5451, 100.8000, 101.7068, 102.4381, 104.9200, 102.3464, 105.2663, 106.4406, 108.1429,
        106.8456, 107.6098, 110.1403, 110.3695, 112.2384, 106.0640, 115.1889, 117.3616, 121.0794,
        109.3366, 113.3824, 115.2838, 116.8496, 117.1195, 124.8409, 120.8200, 119.4238, 122.1746,
        123.0395, 130.1453, 127.8085, 133.4749, 138.0800
    ]
}

df = pd.DataFrame(data)

# =============================
# Sidebar interaktif
# =============================
st.sidebar.header("🔍 Filter Data")
jenis_lembaga = ["Bahasa_Asing", "Komputer", "Menjahit"]
pilihan_jenis = st.sidebar.selectbox("Pilih Jenis Lembaga Pelatihan:", jenis_lembaga)

wilayah_opsi = st.sidebar.multiselect(
    "Pilih Provinsi (opsional):",
    df['Provinsi'].tolist(),
    default=[]
)

if wilayah_opsi:
    df_filtered = df[df['Provinsi'].isin(wilayah_opsi)]
else:
    df_filtered = df

# =============================
# Ringkasan Nasional
# =============================
st.subheader("📊 Ringkasan Data Nasional")
col1, col2, col3 = st.columns(3)
col1.metric("Total Provinsi", df['Provinsi'].nunique())
col2.metric("Total Lembaga Pelatihan", int(df['Total_Lembaga'].sum()))
col3.metric("Rata-rata Persentase Desa dengan Lembaga", f"{df['Persentase_Desa_Dengan_Lembaga'].mean():.2f}%")

st.divider()

# =============================
# Visualisasi Bar Chart
# =============================
st.subheader(f"🏫 5 Provinsi dengan {pilihan_jenis.replace('_', ' ')} Terbanyak")
top5 = df.sort_values(pilihan_jenis, ascending=False).head(5)

plt.figure(figsize=(8, 4))
sns.barplot(x='Provinsi', y=pilihan_jenis, data=top5, palette='viridis')
plt.title(f'5 Provinsi dengan {pilihan_jenis.replace('_', ' ')} Terbanyak')
plt.xticks(rotation=45)
st.pyplot(plt.gcf())
plt.close()

# =============================
# Peta Sebaran Lembaga
# =============================
st.subheader("🗺️ Peta Sebaran Lembaga Pelatihan per Provinsi")
gdf = gpd.GeoDataFrame(
    df,
    geometry=gpd.points_from_xy(df['Longitude'], df['Latitude']),
    crs="EPSG:4326"
)

m = folium.Map(location=[-2.5, 117], zoom_start=5)
for _, row in gdf.iterrows():
    tooltip = (
        f"<b>{row['Provinsi']}</b><br>"
        f"{pilihan_jenis.replace('_', ' ')}: {int(row[pilihan_jenis])}<br>"
        f"Total Lembaga: {int(row['Total_Lembaga'])}<br>"
        f"Persentase Desa: {row['Persentase_Desa_Dengan_Lembaga']:.1f}%"
    )
    folium.CircleMarker(
        location=[row['Latitude'], row['Longitude']],
        radius=7 + (row[pilihan_jenis] / df[pilihan_jenis].max()) * 8,
        color='blue',
        fill=True,
        fill_opacity=0.6,
        popup=tooltip,
        tooltip=tooltip
    ).add_to(m)

st_folium(m, width=1200, height=600)

# =============================
# Korelasi antar lembaga
# =============================
st.subheader("🔗 Korelasi antar Jenis Lembaga")
corr = df[["Bahasa_Asing", "Komputer", "Menjahit"]].corr()
plt.figure(figsize=(6, 4))
sns.heatmap(corr, annot=True, cmap='coolwarm')
plt.title("Korelasi antar Jenis Lembaga")
st.pyplot(plt.gcf())
plt.close()

# =============================
# Data tabel
# =============================
st.subheader("📋 Data Provinsi Lengkap")
st.dataframe(df_filtered)

st.markdown("---")
st.markdown("© 2025 Dashboard Potensi Desa Indonesia | Dibuat oleh Fridha Megantara Putra")
