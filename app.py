import streamlit as st
import pandas as pd
import geopandas as gpd
import folium
from streamlit_folium import st_folium
import seaborn as sns
import matplotlib.pyplot as plt

# =============================
# Pengaturan dasar aplikasi
# =============================
st.set_page_config(
    page_title="Dashboard Potensi Desa Indonesia",
    page_icon="🌾",
    layout="wide"
)

st.title("🌾 Dashboard Potensi Desa di Indonesia")
st.markdown("Analisis dan visualisasi data potensi desa berdasarkan **lembaga pelatihan** di setiap provinsi.")

# =============================
# Data utama (langsung di sini)
# =============================
data = {
    'Provinsi': [
        'Aceh', 'Sumatera Utara', 'Sumatera Barat', 'Riau', 'Jambi',
        'Sumatera Selatan', 'Bengkulu', 'Lampung', 'Kepulauan Bangka Belitung',
        'Kepulauan Riau', 'DKI Jakarta', 'Jawa Barat', 'Jawa Tengah',
        'DI Yogyakarta', 'Jawa Timur', 'Banten', 'Bali', 'Nusa Tenggara Barat',
        'Nusa Tenggara Timur', 'Kalimantan Barat', 'Kalimantan Tengah',
        'Kalimantan Selatan', 'Kalimantan Timur', 'Kalimantan Utara',
        'Sulawesi Utara', 'Sulawesi Tengah', 'Sulawesi Selatan',
        'Sulawesi Tenggara', 'Gorontalo', 'Sulawesi Barat', 'Maluku',
        'Maluku Utara', 'Papua Barat', 'Papua Barat Daya', 'Papua',
        'Papua Selatan', 'Papua Tengah', 'Papua Pegunungan'
    ],
    'Bahasa_Asing': [99, 322, 104, 84, 66, 160, 48, 129, 38, 61, 104, 547, 632, 66, 641, 129, 150, 147, 55, 64, 19, 37, 45, 8, 43, 31, 126, 30, 5, 20, 39, 24, 9, 11, 23, 3, 15, 5],
    'Komputer': [288, 372, 74, 138, 73, 227, 44, 188, 39, 30, 74, 448, 425, 39, 519, 132, 51, 91, 49, 85, 79, 154, 81, 18, 54, 82, 99, 28, 15, 13, 51, 59, 12, 2, 29, 1, 67, 5],
    'Menjahit_Tata_Busana': [698, 503, 112, 223, 171, 154, 62, 257, 13, 47, 58, 709, 609, 60, 832, 103, 48, 140, 95, 104, 70, 204, 112, 30, 68, 108, 318, 54, 34, 31, 21, 27, 0, 0, 23, 5, 4, 2],
    'Kecantikan': [110, 322, 39, 71, 49, 78, 26, 104, 11, 19, 51, 354, 237, 35, 443, 91, 53, 94, 31, 46, 17, 47, 36, 16, 53, 52, 145, 15, 9, 11, 12, 15, 0, 0, 9, 1, 3, 0],
    'Montir_Mobil_Motor': [255, 227, 37, 96, 22, 120, 40, 128, 6, 19, 45, 268, 240, 26, 448, 70, 23, 62, 51, 81, 34, 56, 49, 9, 62, 74, 110, 10, 2, 11, 26, 44, 8, 7, 20, 4, 45, 3],
    'Elektronika': [82, 77, 18, 38, 14, 48, 12, 45, 2, 7, 33, 141, 82, 15, 255, 48, 12, 29, 10, 28, 14, 24, 16, 4, 13, 23, 46, 14, 3, 1, 5, 16, 0, 1, 7, 2, 5, 3],
    'Lainnya': [76, 82, 47, 64, 43, 39, 20, 29, 8, 20, 50, 208, 277, 46, 236, 43, 75, 48, 34, 27, 25, 107, 51, 26, 21, 19, 73, 5, 7, 6, 20, 11, 0, 0, 14, 3, 2, 1],
    'Tidak_Ada_Lembaga': [5416, 5036, 1011, 1448, 1311, 2759, 1346, 2124, 308, 326, 120, 4412, 6995, 291, 6572, 1210, 474, 838, 3306, 1897, 1414, 1625, 825, 419, 1655, 1792, 2519, 2180, 681, 587, 1150, 1078, 944, 1038, 944, 678, 1121, 2617]
}

# Koordinat setiap provinsi
koordinat_provinsi = {
    'Aceh': [4.695135, 96.749397], 'Sumatera Utara': [2.192862, 99.381332], 'Sumatera Barat': [-0.739566, 100.800005],
    'Riau': [0.293347, 101.706825], 'Jambi': [-1.610350, 103.613251], 'Sumatera Selatan': [-3.319908, 103.914399],
    'Bengkulu': [-3.792860, 102.260924], 'Lampung': [-4.855501, 105.045055], 'Kepulauan Bangka Belitung': [-2.741600, 106.440727],
    'Kepulauan Riau': [3.945651, 108.142929], 'DKI Jakarta': [-6.200000, 106.816666], 'Jawa Barat': [-6.914744, 107.609810],
    'Jawa Tengah': [-7.150975, 110.140259], 'DI Yogyakarta': [-7.795580, 110.369492], 'Jawa Timur': [-7.536064, 112.238403],
    'Banten': [-6.120000, 106.150276], 'Bali': [-8.409518, 115.188919], 'Nusa Tenggara Barat': [-8.652932, 117.361648],
    'Nusa Tenggara Timur': [-8.657382, 121.079369], 'Kalimantan Barat': [0.278992, 111.475266],
    'Kalimantan Tengah': [-1.681488, 113.382355], 'Kalimantan Selatan': [-3.092642, 115.283760],
    'Kalimantan Timur': [0.538659, 116.419388], 'Kalimantan Utara': [3.073565, 116.041145],
    'Sulawesi Utara': [0.624763, 123.972974], 'Sulawesi Tengah': [-1.430025, 121.445618],
    'Sulawesi Selatan': [-3.644670, 119.946932], 'Sulawesi Tenggara': [-4.144910, 122.174620],
    'Gorontalo': [0.556174, 123.058548], 'Sulawesi Barat': [-2.844138, 119.232376],
    'Maluku': [-3.238462, 130.145242], 'Maluku Utara': [1.570999, 127.808769],
    'Papua Barat': [-1.038700, 131.317840], 'Papua Barat Daya': [-1.846220, 132.902780],
    'Papua': [-4.269928, 138.080353], 'Papua Selatan': [-7.015350, 139.634720],
    'Papua Tengah': [-3.704790, 138.676690], 'Papua Pegunungan': [-4.168100, 138.795780]
}

# Buat DataFrame utama
df = pd.DataFrame(data)
df['Latitude'] = df['Provinsi'].map(lambda x: koordinat_provinsi[x][0])
df['Longitude'] = df['Provinsi'].map(lambda x: koordinat_provinsi[x][1])

# Hitung kolom tambahan
df['Total_Lembaga'] = df.iloc[:, 1:-1].sum(axis=1)
df['Persentase_Desa_Dengan_Lembaga'] = df['Total_Lembaga'] / (df['Total_Lembaga'] + df['Tidak_Ada_Lembaga']) * 100

# =============================
# Sidebar filter
# =============================
st.sidebar.header("🔍 Filter Data")
jenis_lembaga = df.columns[1:-4].tolist()
pilihan_jenis = st.sidebar.selectbox("Pilih Jenis Lembaga:", jenis_lembaga)

# =============================
# Ringkasan data nasional
# =============================
st.subheader("📊 Ringkasan Nasional")
col1, col2, col3 = st.columns(3)
col1.metric("Total Provinsi", df['Provinsi'].nunique())
col2.metric("Total Lembaga Pelatihan", int(df['Total_Lembaga'].sum()))
col3.metric("Rata-rata Persentase Desa dengan Lembaga", f"{df['Persentase_Desa_Dengan_Lembaga'].mean():.2f}%")

# =============================
# Grafik 5 provinsi teratas
# =============================
st.subheader(f"🏫 5 Provinsi Teratas - {pilihan_jenis.replace('_',' ')}")

top5 = df.sort_values(pilihan_jenis, ascending=False).head(5)
plt.figure(figsize=(8, 4))
sns.barplot(x='Provinsi', y=pilihan_jenis, data=top5, palette='viridis')
plt.title(f'5 Provinsi dengan {pilihan_jenis.replace("_"," ")} Terbanyak')
plt.xticks(rotation=45)
st.pyplot(plt.gcf())
plt.close()

# =============================
# Peta interaktif GeoPandas + Folium
# =============================
st.subheader("🗺️ Peta Sebaran Lembaga Pelatihan")

gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df['Longitude'], df['Latitude']), crs="EPSG:4326")
m = folium.Map(location=[-2.5, 117], zoom_start=5)

for _, row in gdf.iterrows():
    tooltip = (
        f"<b>{row['Provinsi']}</b><br>"
        f"Total Lembaga: {int(row['Total_Lembaga'])}<br>"
        f"{pilihan_jenis.replace('_',' ')}: {int(row[pilihan_jenis])}<br>"
        f"Persentase Desa dengan Lembaga: {row['Persentase_Desa_Dengan_Lembaga']:.2f}%"
    )
    folium.CircleMarker(
        location=[row['Latitude'], row['Longitude']],
        radius=6 + (row[pilihan_jenis] / df[pilihan_jenis].max()) * 6,
        color='blue',
        fill=True,
        fill_opacity=0.6,
        tooltip=tooltip
    ).add_to(m)

st_folium(m, width=1200, height=600)

# =============================
# Korelasi antar jenis lembaga
# =============================
st.subheader("🔗 Korelasi antar Jenis Lembaga")
corr = df.iloc[:, 1:-4].corr()
plt.figure(figsize=(10, 6))
sns.heatmap(corr, cmap='coolwarm', annot=False)
plt.title("Korelasi antar Jenis Lembaga Pelatihan")
st.pyplot(plt.gcf())
plt.close()

# =============================
# Tabel data
# =============================
st.subheader("📋 Data Provinsi Lengkap")
st.dataframe(df)

st.markdown("---")
st.markdown("© 2025 Dashboard Potensi Desa Indonesia | Dibuat oleh Fridha Megantara Putra 💻")
