import pandas as pd
import rasterio

df = pd.read_csv('code/amazon_500m_features.csv')
coords = list(zip(df.longitude, df.latitude))   #coordinates 

rasters = {
    'temp_seasonality': 'WorldClim Dataset/wc2.1_5m_bio_4.tif',
    'temp_annual_range': 'WorldClim Dataset/wc2.1_5m_bio_7.tif',
    'precip_driest_quarter': 'WorldClim Dataset/wc2.1_5m_bio_17.tif',
    'max_temp_warmest_month': 'WorldClim Dataset/wc2.1_5m_bio_5.tif',
    'annual_precipitation': 'WorldClim Dataset/wc2.1_5m_bio_12.tif',
    'precip_coldest_quarter': 'WorldClim Dataset/wc2.1_5m_bio_19.tif',
    'isothermality': 'WorldClim Dataset/wc2.1_5m_bio_3.tif'
    'elevation': 'code/elevation_south_america.tif'
}   #the key here representsthe variable and the item has the location to the tif variable that has data for that variable

#  Loop through each raster and sample
for var_name, path in rasters.items():
    with rasterio.open(path) as src:
        # sample returns a generator of 1-element arrays
        vals = [val[0] for val in src.sample(coords)]
        df[var_name] = vals


df.to_csv('amazon_500m_with_worldclim_vars.csv', index=False)
print("Done—wrote amazon_500m_with_worldclim_vars.csv with shape", df.shape)
