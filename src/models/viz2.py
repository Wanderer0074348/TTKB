import geopandas as gpd
import matplotlib.pyplot as plt

new_amazon = gpd.read_file('amazon_grid.shp')
print(new_amazon.head())
fig, ax = plt.subplots(figsize=(8,8))
new_amazon.boundary.plot(ax=ax, linewidth=0.5, edgecolor='black')
ax.set_title("Brazilian Amazon Grid Boundaries")
plt.show()
new_amazon.plot()
plt.show()
