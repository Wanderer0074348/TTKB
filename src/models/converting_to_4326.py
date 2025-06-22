import geopandas as gpd

am = gpd.read_file('amazon_500m_samples.shp')
am.to_crs("epsg:4326", inplace=True)  # Reproject to WGS 84

am.to_file('amazon_500m_latlon.shp')

