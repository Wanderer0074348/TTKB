import geopandas as gpd


# Load the clipped grid

grid = gpd.read_file('amazon_grid.shp')

# Compute centroids
grid['centroid'] = grid.geometry.centroid
centroids = grid.set_geometry('centroid').drop(columns='geometry')

# Save centroids
centroids.to_file('amazon_centroids.shp')
print(f"Saved {len(centroids)} centroids")
