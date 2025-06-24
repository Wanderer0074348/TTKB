import pandas as pd
import rasterio

df = pd.read_csv('code/amazon_geoglyph_coords.csv')
coords = list(zip(df.longitude, df.latitude))

rasters = {
    'temp_seasonality': 'WorldClim Dataset/wc2.1_5m_bio_4.tif',
    'temp_annual_range': 'WorldClim Dataset/wc2.1_5m_bio_7.tif',
    'precip_driest_quarter': 'WorldClim Dataset/wc2.1_5m_bio_17.tif',
    'max_temp_warmest_month': 'WorldClim Dataset/wc2.1_5m_bio_5.tif',
    'annual_precipitation': 'WorldClim Dataset/wc2.1_5m_bio_12.tif',
    'precip_coldest_quarter': 'WorldClim Dataset/wc2.1_5m_bio_19.tif',
    'isothermality': 'WorldClim Dataset/wc2.1_5m_bio_3.tif',
    'elevation': 'code/elevation_south_america.tif'

}

for var_name, path in rasters.items():
    with rasterio.open(path) as src:
        # sample returns a generator of 1-element arrays
        vals = [val[0] for val in src.sample(coords)]
        df[var_name] = vals

df.to_csv('amazon_known_geoglyph_data.csv', index=False)
print("Done—wrote amazon_known_geoglyph_data.csv with shape", df.shape)
