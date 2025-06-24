import rasterio
from rasterio.warp import calculate_default_transform, reproject, Resampling

src_path = 'HWSD2.bil'
dst_path = 'HWSD2_Map_unit_4326.tif'
dst_crs  = 'EPSG:4326'

with rasterio.open(src_path) as src:
    transform, width, height = calculate_default_transform(
        src.crs, dst_crs,
        src.width, src.height,
        *src.bounds
    )
    kwargs = src.meta.copy()
    kwargs.update({
        'crs': dst_crs,
        'transform': transform,
        'width': width,
        'height': height,
        'driver': 'GTiff'
    })

    # Create the destination file and reproject each band
    with rasterio.open(dst_path, 'w', **kwargs) as dst:
        for i in range(1, src.count + 1):
            reproject(
                source=rasterio.band(src, i),
                destination=rasterio.band(dst, i),
                src_transform=src.transform,
                src_crs=src.crs,
                dst_transform=transform,
                dst_crs=dst_crs,
                resampling=Resampling.nearest
            )

print(f"Reprojected to {dst_path} in {dst_crs}.")
