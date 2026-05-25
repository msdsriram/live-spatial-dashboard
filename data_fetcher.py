import pandas as pd
import geopandas as gpd
from shapely.geometry import Point

def fetch_air_quality_data():
    print("Loading sample air quality data for India...")

    rows = [
        {"name": "Anand Vihar",      "city": "Delhi",     "country": "IN", "latitude": 28.6469, "longitude": 77.3152, "aqi": 185},
        {"name": "Punjabi Bagh",     "city": "Delhi",     "country": "IN", "latitude": 28.6663, "longitude": 77.1313, "aqi": 162},
        {"name": "Mandir Marg",      "city": "Delhi",     "country": "IN", "latitude": 28.6350, "longitude": 77.2090, "aqi": 143},
        {"name": "Bandra",           "city": "Mumbai",    "country": "IN", "latitude": 19.0596, "longitude": 72.8295, "aqi": 87},
        {"name": "Worli",            "city": "Mumbai",    "country": "IN", "latitude": 19.0176, "longitude": 72.8162, "aqi": 94},
        {"name": "Borivali",         "city": "Mumbai",    "country": "IN", "latitude": 19.2307, "longitude": 72.8567, "aqi": 102},
        {"name": "Velachery",        "city": "Chennai",   "country": "IN", "latitude": 12.9815, "longitude": 80.2180, "aqi": 76},
        {"name": "Manali",           "city": "Chennai",   "country": "IN", "latitude": 13.1674, "longitude": 80.2594, "aqi": 134},
        {"name": "Adyar",            "city": "Chennai",   "country": "IN", "latitude": 13.0012, "longitude": 80.2565, "aqi": 68},
        {"name": "Whitefield",       "city": "Bangalore", "country": "IN", "latitude": 12.9698, "longitude": 77.7500, "aqi": 55},
        {"name": "BTM Layout",       "city": "Bangalore", "country": "IN", "latitude": 12.9166, "longitude": 77.6101, "aqi": 61},
        {"name": "Hebbal",           "city": "Bangalore", "country": "IN", "latitude": 13.0450, "longitude": 77.5950, "aqi": 73},
        {"name": "Salt Lake",        "city": "Kolkata",   "country": "IN", "latitude": 22.5697, "longitude": 88.4018, "aqi": 118},
        {"name": "Jadavpur",         "city": "Kolkata",   "country": "IN", "latitude": 22.4994, "longitude": 88.3711, "aqi": 125},
        {"name": "Sector 62",        "city": "Noida",     "country": "IN", "latitude": 28.6274, "longitude": 77.3650, "aqi": 177},
        {"name": "Talwade",          "city": "Pune",      "country": "IN", "latitude": 18.6530, "longitude": 73.7903, "aqi": 65},
        {"name": "Shivaji Nagar",    "city": "Pune",      "country": "IN", "latitude": 18.5308, "longitude": 73.8474, "aqi": 71},
        {"name": "Chandkheda",       "city": "Ahmedabad", "country": "IN", "latitude": 23.1144, "longitude": 72.5680, "aqi": 95},
        {"name": "Bopal",            "city": "Ahmedabad", "country": "IN", "latitude": 23.0395, "longitude": 72.4694, "aqi": 88},
        {"name": "Salem",            "city": "Salem",     "country": "IN", "latitude": 11.6643, "longitude": 78.1460, "aqi": 58},
    ]

    df = pd.DataFrame(rows)
    print(f"Stations loaded: {len(df)}")
    print(df.head(10))

    geometry = [Point(lon, lat) for lon, lat in zip(df["longitude"], df["latitude"])]
    gdf = gpd.GeoDataFrame(df, geometry=geometry, crs="EPSG:4326")

    print(f"\nGeoDataFrame created successfully!")
    print(f"Columns: {list(gdf.columns)}")
    print(f"Shape: {gdf.shape}")

    return gdf

if __name__ == "__main__":
    gdf = fetch_air_quality_data()