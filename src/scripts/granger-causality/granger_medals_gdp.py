# Gemini, to review

import pandas as pd
import numpy as np
from statsmodels.tsa.stattools import adfuller, grangercausalitytests

# Assume 'df' is your expanded historical dataset with columns: Year, NOC, Total_Medals, GDP

# 1. Filter to a single country with a long history (e.g., Great Britain)
uk_df = df[df['NOC'] == 'GBR'].copy()
uk_df = uk_df.sort_values('Year').reset_index(drop=True)

# 2. Transform variables to make them stationary
# A. Log-Difference of GDP (GDP Growth Rate)
uk_df['ln_GDP'] = np.log(uk_df['GDP'])
uk_df['GDP_Growth'] = uk_df['ln_GDP'].diff()

# B. First Difference of Medals (Change in Medals)
uk_df['Medals_Diff'] = uk_df['Total_Medals'].diff()

# Drop the NaN row created by differencing (the first year, 1896)
uk_df = uk_df.dropna(subset=['GDP_Growth', 'Medals_Diff'])

# 3. Check Stationarity with ADF
print("--- ADF Test: Medals Differenced ---")
adf_medals = adfuller(uk_df['Medals_Diff'], regression='c')
print(f"P-value: {adf_medals[1]:.4f} (If < 0.05, it is stationary)")

print("\n--- ADF Test: GDP Growth ---")
adf_gdp = adfuller(uk_df['GDP_Growth'], regression='c')
print(f"P-value: {adf_gdp[1]:.4f} (If < 0.05, it is stationary)")

# 4. Run Granger Causality
# We want to test if GDP_Growth (column 2) Granger-causes Medals_Diff (column 1).
# We test up to 2 lags (e.g., does GDP growth from 1 or 2 Olympics ago predict today's medals?)
print("\n--- Granger Causality: Does GDP Growth cause Changes in Medals? ---")

# grangercausalitytests expects a 2D array: [Target_Variable, Predictor_Variable]
data_for_granger = uk_df[['Medals_Diff', 'GDP_Growth']]

# maxlag=2 means we check the previous 1 and 2 Olympics
results = grangercausalitytests(data_for_granger, maxlag=2)