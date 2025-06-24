import pandas as pd

df = pd.read_csv('amazon_unknown_geoglyph_data.csv')

mask = (
    (df.longitude >= -72) &
    (df.longitude <= -55) &
    (df.latitude  >= -16) &
    (df.latitude  <=   -2)
)

df2 = df[mask].reset_index(drop=True)

print("Length of original DataFrame:", len(df))
print("Length of reduced DataFrame:", len(df2))

df2.to_csv('amazon_reduced_unknown_geoglyph_data.csv', index=False)
