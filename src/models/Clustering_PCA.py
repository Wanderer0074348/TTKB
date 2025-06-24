import pandas as pd
import numpy as np
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
import matplotlib.pyplot as plt

# 1) Load & label your two datasets
df_all = pd.read_csv('amazon_unknown_geoglyph_data.csv')
df_all['is_geoglyph'] = 0

df_known = pd.read_csv('amazon_known_geoglyph_data.csv')
df_known['is_geoglyph'] = 1

# 2) Concatenate into one DataFrame
df = pd.concat([df_all, df_known], ignore_index=True)

# 3) Select your feature columns
features = [
    'temp_seasonality',
    'temp_annual_range',
    'precip_driest_quarter',
    'max_temp_warmest_month',
    'annual_precipitation',
    'precip_coldest_quarter',
    'isothermality',
    'elevation',
    'sand_frac_pct',
    'gravel_frac_pct'
]
X = df[features].values

# 4) CLEANING: Impute any missing values (NaNs) with the column mean
imputer = SimpleImputer(strategy='mean')
X_imputed = imputer.fit_transform(X)

# 5) SCALE to zero mean & unit variance
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X_imputed)

# 6) FIT PCA → 2 components
pca = PCA(n_components=2, random_state=0)
X_2d = pca.fit_transform(X_scaled)

mask = (
    (np.abs(X_2d[:,0]) < 5 * X_2d[:,0].std()) &
    (np.abs(X_2d[:,1]) < 5 * X_2d[:,1].std())
)
X_2d = X_2d[mask]
df    = df[mask]  

# 7) PRINT PCA LOADINGS for each original feature
print("Explained variance ratio:", pca.explained_variance_ratio_)
for i, comp in enumerate(pca.components_):
    print(f"\nPC{i+1} loadings:")
    for feat, loading in zip(features, comp):
        print(f"  {feat}: {loading:.2f}")

# 8) SUBSAMPLE for plotting (so it isn’t millions of points)
n_samples = X_2d.shape[0]
sub_idx = np.random.choice(n_samples, size=200_000, replace=False)

X_sub = X_2d[sub_idx]
y_sub = df['is_geoglyph'].values[sub_idx].astype(bool)

# 9) PLOT the 2D projection
plt.figure(figsize=(10,10))
plt.scatter(
    X_sub[~y_sub, 0], X_sub[~y_sub, 1],
    s=2, alpha=0.3, label='Grid points'
)
plt.scatter(
    X_sub[y_sub, 0], X_sub[y_sub, 1],
    s=8, alpha=0.8, color='red', label='Known geoglyphs'
)
plt.xlabel('PC1')
plt.ylabel('PC2')
plt.title('2D PCA of Environmental Features')
plt.legend(markerscale=4)
plt.show()
