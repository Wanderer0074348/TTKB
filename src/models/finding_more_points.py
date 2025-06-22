import geopandas as gpd
import numpy as np
from shapely.geometry import Point

grid = gpd.read_file('amazon_grid.shp')

# Prepare a list to hold all sample points
sample_pts = []
step = 500  # step distance in metres  

# 4. Iterate over each grid cell polygon
for idx, row in grid.iterrows():
    poly = row.geometry
    minx, miny, maxx, maxy = poly.bounds   #.bounds returns the the maximum and minimum values across the x and y axes
    
    # build 1D arrays of X and Y coordinates at 500 m intervals
    xs = np.arange(minx, maxx + step, step)
    ys = np.arange(miny, maxy + step, step)
    
    # for each grid intersection, test if it's inside the polygon
    for x in xs:
        for y in ys:
            pt = Point(x, y)
            if poly.contains(pt):
                sample_pts.append(pt)

# Turn that list into a GeoDataFrame
pts_gdf = gpd.GeoDataFrame(geometry=sample_pts, crs=grid.crs)

#  Save out your new sample-point layer
pts_gdf.to_file('amazon_500m_samples.shp')
print(f"Generated {len(pts_gdf)} sample points at 500 m spacing.") 
