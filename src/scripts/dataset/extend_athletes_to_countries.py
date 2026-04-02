import pandas as pd
import numpy as np

# File paths

# dataset generated from the other converter script
DS_ORIGINAL_PATH = 'dataset/country-medals-by-year.csv'
# years missing from main dataset
DS_MISSING_PATH  = 'dataset/country-medals-by-year_missing_2018-2026.csv'
DS_HOSTS_PATH    = 'dataset/hosts.csv'
DS_OUTPUT_PATH   = 'dataset/country-medals-by-year_full.csv'

def merge_missing_olympics():
	print("Loading original historical dataset...")
	original_df = pd.read_csv(DS_ORIGINAL_PATH)
	
	print("Loading missing olympics dataset (2018-2026)...")
	missing_df = pd.read_csv(DS_MISSING_PATH)
		
	print("Loading hosts dataset...")
	hosts_df = pd.read_csv(DS_HOSTS_PATH)
	
	# Handle the Men/Women columns. We set them to NaN because we don't 
	# have the exact gender split for these newer games.
	missing_df['Men_Medals'] = np.nan
	missing_df['Women_Medals'] = np.nan
	
	# Add the Hosting Nation logic dynamically from hosts.csv
	print("Applying Host Country flags dynamically...")
	# Merge the hosts_df to find out who hosted that Year and Season
	missing_df = pd.merge(missing_df, hosts_df, on=['Year', 'Season'], how='left')
	
	# Create the 'Is_Host' column: if the participating NOC matches the Host_NOC, it's a 1
	missing_df['Is_Host'] = (missing_df['NOC'] == missing_df['Host_NOC']).astype(int)
	
	# Clean up by dropping the temporary columns from the merge
	missing_df = missing_df.drop(columns=['Host_NOC', 'City'])
	
	# Concatenate the two datasets
	print("Merging datasets together...")
	combined_df = pd.concat([original_df, missing_df], ignore_index=True)
	
	# Sort chronologically and by total medals for readability
	combined_df = combined_df.sort_values(by=['Year', 'Season', 'Total_Medals'], ascending=[True, True, False])
	
	# Clean up data types (Pandas might try to make counts Floats after concating with NaN)
	cols_to_int =['Year', 'Total_Medals', 'Gold', 'Silver', 'Bronze', 'Is_Host']
	combined_df[cols_to_int] = combined_df[cols_to_int].astype(int)
	
	# Save the final extended file
	combined_df.to_csv(DS_OUTPUT_PATH, index=False)
	print(f"Success! Extended dataset saved to '{DS_OUTPUT_PATH}'.")

if __name__ == "__main__":
	merge_missing_olympics()