import rasterio
import numpy as np
import matplotlib.pyplot as plt
from scipy import ndimage
from skimage import filters

# Load your elevation data
with rasterio.open('rasters_COP90/output_hh.tif') as src:
    elevation = src.read(1)
    bounds = src.bounds
    
print(f"Data shape: {elevation.shape}")
print(f"Elevation range: {elevation.min():.1f}m to {elevation.max():.1f}m")
print(f"Geographic bounds: {bounds}")

# Basic visualization
plt.figure(figsize=(10, 8))
plt.imshow(elevation, cmap='terrain')
plt.colorbar(label='Elevation (m)')
plt.title('Your Amazon DEM Data')
plt.show()
