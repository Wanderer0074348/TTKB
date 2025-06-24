import pandas as pd
import rasterio

df = pd.read_csv('amazon_known_geoglyph_data.csv')
coords = list(zip(df.longitude, df.latitude))

with rasterio.open('HWSD2_Map_unit_4326.tif') as src:
    df['MU_GLOBAL'] = [val[0] for val in src.sample(coords)]

soil_raw = pd.read_csv(
    'code/HWSD_DATA.csv',
    usecols=['MU_GLOBAL','T_SAND','T_GRAVEL']
)

soil = (
    soil_raw
    .dropna(subset=['T_SAND','T_GRAVEL'])
    .groupby('MU_GLOBAL', as_index=False)
    .agg({
        'T_SAND':   'mean',
        'T_GRAVEL': 'mean'
    })
)

print(f"Collapsed from {len(soil_raw)} to {len(soil)} unique MU_GLOBAL units")

df = df.merge(
    soil,
    how='left',
    on='MU_GLOBAL',
    validate='many_to_one'
)

df = df.rename(columns={
    'T_SAND':   'sand_frac_pct',
    'T_GRAVEL': 'gravel_frac_pct'
})

df.to_csv('amazon_known_geoglyph_data.csv', index=False)
print("Done—rows:", len(df))
