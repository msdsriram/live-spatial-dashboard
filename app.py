import streamlit as st
import folium
from folium.plugins import HeatMap, MarkerCluster
from streamlit_folium import st_folium
import plotly.express as px
from data_fetcher import fetch_air_quality_data

st.set_page_config(
    page_title="India Air Quality Dashboard",
    page_icon="🌍",
    layout="wide"
)

st.title("🌍 India Live Air Quality Dashboard")
st.markdown("Real-time air quality index (AQI) across major Indian cities")

gdf = fetch_air_quality_data()

st.sidebar.header("Filters")

cities = ["All"] + sorted(gdf["city"].unique().tolist())
selected_city = st.sidebar.selectbox("Select City", cities)

aqi_range = st.sidebar.slider(
    "AQI Range",
    min_value=0,
    max_value=300,
    value=(0, 300)
)

if selected_city != "All":
    filtered = gdf[gdf["city"] == selected_city]
else:
    filtered = gdf

filtered = filtered[
    (filtered["aqi"] >= aqi_range[0]) &
    (filtered["aqi"] <= aqi_range[1])
]

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Stations",  len(filtered))
col2.metric("Average AQI",     round(filtered["aqi"].mean(), 1))
col3.metric("Highest AQI",     filtered["aqi"].max())
col4.metric("Lowest AQI",      filtered["aqi"].min())

st.subheader("Air Quality Map")

def get_color(aqi):
    if aqi <= 50:    return "green"
    elif aqi <= 100: return "blue"
    elif aqi <= 150: return "orange"
    elif aqi <= 200: return "red"
    else:            return "darkred"

m = folium.Map(location=[20.5937, 78.9629], zoom_start=5, tiles="CartoDB dark_matter")
cluster = MarkerCluster(name="Stations").add_to(m)

for _, row in filtered.iterrows():
    folium.CircleMarker(
        location=[row["latitude"], row["longitude"]],
        radius=10,
        color=get_color(row["aqi"]),
        fill=True,
        fill_opacity=0.8,
        popup=folium.Popup(
            f"<b>{row['name']}</b><br>City: {row['city']}<br>AQI: {row['aqi']}",
            max_width=200
        )
    ).add_to(cluster)

heat_data = [[row["latitude"], row["longitude"], row["aqi"]] for _, row in filtered.iterrows()]
HeatMap(heat_data, name="Heatmap", radius=40).add_to(m)
folium.LayerControl().add_to(m)

st_folium(m, width=1200, height=500)

st.subheader("AQI by Station")
fig = px.bar(
    filtered.sort_values("aqi", ascending=False),
    x="name", y="aqi", color="city",
    labels={"name": "Station", "aqi": "AQI Value"},
    color_discrete_sequence=px.colors.qualitative.Set2
)
st.plotly_chart(fig, use_container_width=True)

st.subheader("Raw Data")
st.dataframe(
    filtered[["name", "city", "aqi"]].sort_values("aqi", ascending=False),
    use_container_width=True
)