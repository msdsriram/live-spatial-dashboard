import folium
from folium.plugins import HeatMap, MarkerCluster
from data_fetcher import fetch_air_quality_data

def get_color(aqi):
    if aqi <= 50:   return "green"
    elif aqi <= 100: return "blue"
    elif aqi <= 150: return "orange"
    elif aqi <= 200: return "red"
    else:            return "darkred"

def build_map():
    gdf = fetch_air_quality_data()

    m = folium.Map(
        location=[20.5937, 78.9629],
        zoom_start=5,
        tiles="CartoDB dark_matter"
    )

    cluster = MarkerCluster(name="Stations").add_to(m)

    for _, row in gdf.iterrows():
        folium.CircleMarker(
            location=[row["latitude"], row["longitude"]],
            radius=10,
            color=get_color(row["aqi"]),
            fill=True,
            fill_opacity=0.8,
            popup=folium.Popup(
                f"""
                <b>{row['name']}</b><br>
                City: {row['city']}<br>
                AQI: {row['aqi']}<br>
                Status: {'Good' if row['aqi'] <= 50 else 'Moderate' if row['aqi'] <= 100 else 'Unhealthy'}
                """,
                max_width=200
            )
        ).add_to(cluster)

    heat_data = [[row["latitude"], row["longitude"], row["aqi"]] for _, row in gdf.iterrows()]
    HeatMap(heat_data, name="Heatmap", radius=40).add_to(m)

    folium.LayerControl().add_to(m)

    m.save("map_output.html")
    print("Map saved as map_output.html")
    return m

if __name__ == "__main__":
    build_map()