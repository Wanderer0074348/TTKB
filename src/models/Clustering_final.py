import pandas as pd
import numpy as np
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
import hdbscan
# 0) Tweak these to adjust strictness
MIN_CLUSTER_SIZE = 200    # minimum size of any accepted cluster
MIN_SAMPLES      = 20     # how conservative core‐point selection is
PROB_THRESHOLD   = 0.7    # minimum membership probability to keep a candidate

# 1) Load your full unknown & known datasets
df_unknown = pd.read_csv('amazon_reduced_unknown_geoglyph_data.csv')
df_unknown['is_geoglyph'] = 0

df_known = pd.read_csv('amazon_known_geoglyph_data.csv')
df_known['is_geoglyph'] = 1

# 2) Combine into one DataFrame
df = pd.concat([df_unknown, df_known], ignore_index=True)

# 3) Select the features you used previously
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

# 4) Extract & clean the feature matrix
X = df[features].values
X = SimpleImputer(strategy='mean').fit_transform(X)
X = StandardScaler().fit_transform(X)

# 5) Run HDBSCAN on all ~9.7M points
clusterer = hdbscan.HDBSCAN(
    min_cluster_size=MIN_CLUSTER_SIZE,
    min_samples=MIN_SAMPLES,
    prediction_data=True,
    core_dist_n_jobs=4
)
labels       = clusterer.fit_predict(X)
probabilities = clusterer.probabilities_

# 6) Attach results back to the DataFrame
df['hdbscan_label']       = labels
df['hdbscan_probability'] = probabilities

# 7) Find which cluster IDs contain known geoglyphs
known_labels = set(df.loc[df.is_geoglyph == 1, 'hdbscan_label'])
known_labels.discard(-1)   # ignore noise if any

# 8) Pull unknown points in those clusters with high confidence
mask_candidates = (
    (df.is_geoglyph == 0) &
    (df.hdbscan_label.isin(known_labels)) &
    (df.hdbscan_probability >= PROB_THRESHOLD)
)
df_candidates = df.loc[mask_candidates].copy()

# 9) Save only the high-priority candidate coords & features
cols_to_keep = ['longitude', 'latitude'] + features
df_candidates[cols_to_keep].to_csv(
    'amazon_high_priority_candidates.csv',
    index=False
)

print(f"Clusters containing known sites: {sorted(known_labels)}")
print(f"Total unknown points retained: {len(df_candidates)}")
print("Wrote amazon_high_priority_candidates.csv")
