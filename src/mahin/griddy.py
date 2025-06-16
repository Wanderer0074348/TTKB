import geopandas as gpd
from shapely.geometry import box
import matplotlib.pyplot as plt



amazon = gpd.read_file('Limites_Amazonia_Legal_2022.shp')

amazon = amazon.to_crs("EPSG:5880")  

cell_size = 6000 

minx, miny, maxx, maxy = amazon.total_bounds
cols = list(range(int(minx), int(maxx), cell_size))
rows = list(range(int(miny), int(maxy), cell_size))

grid_cells = []
for x in cols:
    for y in rows:
        grid_cells.append(box(x, y, x+cell_size, y+cell_size))

grid = gpd.GeoDataFrame({'geometry': grid_cells}, crs=amazon.crs)

amazon_grid = gpd.overlay(grid, amazon, how='intersection')


amazon_grid.to_file('amazon_grid.shp')  #Saving the file
print(f"Generated {len(amazon_grid)} grid cells")
