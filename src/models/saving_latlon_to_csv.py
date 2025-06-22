#converting the amazon_laton shp file into a csv file

import geopandas as gpd
import pandas as pd

# Load your shapefile with sampled variables already attached
pts = gpd.read_file('amazon_centroids_latlon.shp')

pts['longitude'] = pts.geometry.x
pts['latitude']  = pts.geometry.y

vars_to_keep = ['longitude', 'latitude']
df = pts[vars_to_keep].copy()

df = df.replace({-9999: pd.NA}).dropna()   # Handle nodata if you like (e.g., drop rows where any var == src.nodata)

df.to_csv('amazon_centroids_features.csv', index=False)
print(f"Written {len(df)} points with {len(vars_to_keep)} columns to amazon_centroids_features.csv")
