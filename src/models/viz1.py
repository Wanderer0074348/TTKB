import geopandas as gp
import matplotlib.pyplot as plt

gdf = gp.read_file('Limites_Amazonia_Legal_2022.shp')

print(gdf.head())

print(gdf.crs)
gdf.plot()
plt.show()
