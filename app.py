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
# 1. Muat Data
# =============================
@st.cache_data
def load_data():
    df = pd.read_csv('./output/data_provinsi.csv')
    return df

df = load_data()

# =============================
# 2. Sidebar untuk interaksi
# =============================
st.sidebar.header("🔍 Filter Data")
jenis_lembaga = df.columns[1:-3].tolist()
pilihan_jenis = st.sidebar.selectbox("Pilih Jenis Lembaga Pelatihan:", jenis_lembaga)

wilayah_opsi = st.sidebar.multiselect(
    "Pilih Provinsi (opsional):",
    df['Provinsi'].tolist(),
    default=[]
)

# Filter berdasarkan provinsi jika dipilih
if wilayah_opsi:
    df_filtered = df[df['Provinsi'].isin(wilayah_opsi)]
else:
    df_filtered = df

# =============================
# 3. Ringkasan Data
# =============================
st.subheader("📊 Ringkasan Data Nasional")
col1, col2, col3 = st.columns(3)

col1.metric("Total Provinsi", df['Provinsi'].nunique())
col2.metric("Total Lembaga Pelatihan", int(df['Total_Lembaga'].sum()))
col3.metric("Rata-rata Persentase Desa dengan Lembaga", f"{df['Persentase_Desa_Dengan_Lembaga'].mean():.2f}%")

st.divider()

# =============================
# 4. Visualisasi Bar Chart
# =============================
st.subheader(f"🏫 5 Provinsi dengan {pilihan_jenis.replace('_', ' ')} Terbanyak")

top5 = df.sort_values(pilihan_jenis, ascending=False).head(5)
plt.figure(figsize=(8, 4))
sns.barplot(x='Provinsi', y=pilihan_jenis, data=top5, palette='viridis')
plt.title(f'5 Provinsi dengan {pilihan_jenis.replace("_", " ")} Terbanyak')
plt.xticks(rotation=45, ha='right')
st.pyplot(plt.gcf())
plt.close()

# =============================
# 5. Peta Interaktif (GeoPandas + Folium)
# =============================
st.subheader("🗺️ Peta Sebaran Lembaga Pelatihan per Provinsi")

# Buat GeoDataFrame dari dataframe
gdf = gpd.GeoDataFrame(
    df,
    geometry=gpd.points_from_xy(df['Longitude'], df['Latitude']),
    crs="EPSG:4326"
)

# Hitung warna berdasarkan jumlah lembaga
m = folium.Map(location=[-2.5, 117], zoom_start=5)

for _, row in gdf.iterrows():
    tooltip_text = (
        f"<b>{row['Provinsi']}</b><br>"
        f"Total Lembaga: {int(row['Total_Lembaga'])}<br>"
        f"{pilihan_jenis.replace('_', ' ')}: {int(row[pilihan_jenis])}<br>"
        f"Persentase Desa dengan Lembaga: {row['Persentase_Desa_Dengan_Lembaga']:.2f}%"
    )
    folium.CircleMarker(
        location=[row['Latitude'], row['Longitude']],
        radius=7 + (row[pilihan_jenis] / df[pilihan_jenis].max()) * 8,
        color='blue',
        fill=True,
        fill_opacity=0.6,
        popup=tooltip_text,
        tooltip=tooltip_text
    ).add_to(m)

# Tampilkan peta
st_data = st_folium(m, width=1200, height=600)

# =============================
# 6. Korelasi antar Jenis Lembaga
# =============================
st.subheader("🔗 Korelasi antar Jenis Lembaga Pelatihan")
corr_matrix = df.iloc[:, 1:-3].corr()

plt.figure(figsize=(10, 6))
sns.heatmap(corr_matrix, annot=False, cmap='coolwarm')
plt.title('Korelasi antar Jenis Lembaga Pelatihan', fontsize=12)
st.pyplot(plt.gcf())
plt.close()

# =============================
# 7. Tabel Data
# =============================
st.subheader("📋 Data Lengkap Provinsi")
st.dataframe(df_filtered)

st.markdown("---")
st.markdown("© 2025 Dashboard Potensi Desa Indonesia | Dibuat dengan ❤️ oleh Fridha Megantara Putra")
