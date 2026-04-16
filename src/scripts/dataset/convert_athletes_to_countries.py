# Convert dataset by athlete to dataset by country
#
# Resulting columns:
# Year | Season | NOC | Total_Medals | Gold | Silver | Bronze | Men_Medals | Women_Medals | Is_Host

import pandas as pd



DS_BY_ATHLETE_PATH	= 'dataset/rgiffin_athletes.csv'
DS_HOSTS_PATH		= 'dataset/hosts.csv'
DS_OUTPUT_PATH		= 'dataset/country-medals-by-year.csv'



def process_olympic_data(input_file, hosts_file, output_file):
	print("Loading dataset...")
	df = pd.read_csv(input_file)
	hosts_df = pd.read_csv(hosts_file)
	
	# GET ALL PARTICIPATING COUNTRIES
	print("Mapping participating countries...")
	participation_df = df[['Year', 'Season', 'NOC']].drop_duplicates()
	
	# FILTER TO WINNERS ONLY (Temporary, to count medals)
	medals_df = df.dropna(subset=['Medal']).copy()
	
	# TEAM SPORT TRAP: Drop duplicates so a team sport (e.g., 12 Basketball players) only counts as 1 total medal for the country
	medals_df = medals_df.drop_duplicates(subset=['Year', 'Season', 'NOC', 'Event', 'Medal'])
	
	# Create dummy columns for easy counting
	medals_df['Total_Medals'] = 1
	medals_df['Gold']   = (medals_df['Medal'] == 'Gold').astype(int)
	medals_df['Silver'] = (medals_df['Medal'] == 'Silver').astype(int)
	medals_df['Bronze'] = (medals_df['Medal'] == 'Bronze').astype(int)
	
	# Create columns for Men and Women
	medals_df['Men_Medals']     = (medals_df['Sex'] == 'M').astype(int)
	medals_df['Women_Medals']   = (medals_df['Sex'] == 'F').astype(int)
	
	# Group by Year, Season, and NOC (Country code)
	print("Aggregating by Country and Year...")
	medal_counts = medals_df.groupby(['Year', 'Season', 'NOC']).agg({
		'Total_Medals': 'sum',
		'Gold': 'sum',
		'Silver': 'sum',
		'Bronze': 'sum',
		'Men_Medals': 'sum',
		'Women_Medals': 'sum'
	}).reset_index()
	
	# MERGE MEDALS BACK TO PARTICIPATION MASTER LIST
	# a 'left' join ensures countries that participated 
	# but didn't win anything will have 'NaN' instead of being deleted.
	final_df = pd.merge(participation_df, medal_counts, on=['Year', 'Season', 'NOC'], how='left')
	
	# Fill the 'NaN' values with 0 (since they won 0 medals)
	columns_to_fill =['Total_Medals', 'Gold', 'Silver', 'Bronze', 'Men_Medals', 'Women_Medals']
	final_df[columns_to_fill] = final_df[columns_to_fill].fillna(0).astype(int)
	
	# ADD THE HOST DUMMY VARIABLE
	print("Applying Host Country flags...")
	# Merge the hosts_df to find out who hosted that Year and Season
	final_df = pd.merge(final_df, hosts_df, on=['Year', 'Season'], how='left')
	
	# Create the 'Is_Host' column: if the participating NOC matches the Host_NOC, it's a 1
	final_df['Is_Host'] = (final_df['NOC'] == final_df['Host_NOC']).astype(int)
	
	# Clean up by dropping the temporary columns from the merge
	final_df = final_df.drop(columns=['Host_NOC', 'City'])
	
	# Sort data chronologically and alphabetically for readability
	final_df = final_df.sort_values(by=['Year', 'Season', 'Total_Medals'], ascending=[True, True, False])
	
	# SAVE TO CSV
	final_df.to_csv(output_file, index=False)
	print(f"Success! Final data saved to '{output_file}' with zero-medal rows perfectly preserved.")



if __name__ == "__main__":
	# Run the function
	process_olympic_data(DS_BY_ATHLETE_PATH, DS_HOSTS_PATH, DS_OUTPUT_PATH)