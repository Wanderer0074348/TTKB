import pandas as pd
import rasterio

# 1. Load your grid‐points
df = pd.read_csv('amazon_500m_with_worldclim_vars.csv')
coords = list(zip(df.longitude, df.latitude))

# 2. Sample the map‐unit TIF to pull MU_GLOBAL
with rasterio.open('HWSD2_Map_unit_4326.tif') as src:
    df['MU_GLOBAL'] = [val[0] for val in src.sample(coords)]

# 3. Read the full HWSD_DATA table
soil_raw = pd.read_csv(
    'code/HWSD_DATA.csv',
    usecols=['MU_GLOBAL','T_SAND','T_GRAVEL']
)

# 4. Aggregate to one row per MU_GLOBAL
soil = (
    soil_raw
    # drop rows missing T_SAND/T_GRAVEL if you want
    .dropna(subset=['T_SAND','T_GRAVEL'])
    .groupby('MU_GLOBAL', as_index=False)
    .agg({
        'T_SAND':   'mean',
        'T_GRAVEL': 'mean'
    })
)

print(f"Collapsed from {len(soil_raw)} to {len(soil)} unique MU_GLOBAL units")

# 5. Merge into your main DataFrame
df = df.merge(
    soil,
    how='left',
    on='MU_GLOBAL',
    validate='many_to_one'
)

# 6. Rename for clarity and save
df = df.rename(columns={
    'T_SAND':   'sand_frac_pct',
    'T_GRAVEL': 'gravel_frac_pct'
})

df.to_csv('amazon_unknown_geoglyph_data.csv', index=False)
print("Done—rows:", len(df))
