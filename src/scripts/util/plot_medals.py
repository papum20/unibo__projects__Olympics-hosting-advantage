import os
import sys

import matplotlib.pyplot as plt
import pandas as pd



DS_PATH = 'dataset/country-medals-by-year.csv'
PLOT_OUT_PATH = 'out/plot/'



def print_usage():
	print("""
	   Usage:
		python granger_calculator.py <S|W|B> [NOC] [0|1]
		- S|W|B: flag to indicate the type of medals (Summer, Winter, or Both).
		- NOC: Optional country code (NOC) to filter by. If not provided, defaults to 'USA'.
		- 0|1: Optional flag to indicate whether save the plot to file (default 0)
	""")


def load_medals_series(country=None, medals_type='S'):
	"""@param country: Optional country code (NOC) to filter by. If None, aggregates across all countries.
	@param medals_type: Type of medals to include (S for Summer, W for Winter, B for Both).
	@return: A pandas Series indexed by Year with total medals as values.
	"""

	# Load the dataset with specified columns
	df = pd.read_csv(DS_PATH, usecols=['Year', 'Season', 'NOC', 'Total_Medals', 'Gold', 'Silver', 'Bronze', 'Men_Medals', 'Women_Medals', 'Is_Host'])
	
	# Filter by medals type
	if medals_type == 'S':
		df = df[df['Season'] == 'Summer']
	elif medals_type == 'W':
		df = df[df['Season'] == 'Winter']
	elif medals_type == 'B':
		df = df[df['Season'].isin(['Summer', 'Winter'])]
	
	if country is None:
		# Aggregate total medals by year (summing across all countries)
		medals_by_year = df.groupby('Year')['Total_Medals'].sum()
	else:
		# Filter for specific country and aggregate by year
		country_df = df[df['NOC'] == country]
		medals_by_year = country_df.groupby('Year')['Total_Medals'].sum()
	
	# Convert to pandas Series with Year as index
	medals_series = pd.Series(medals_by_year.values, index=medals_by_year.index, name='Total_Medals')
	
	return medals_series


def save_plot(fig, noc, medals_type='S'):
	"""Save the plot with a timestamp in the filename."""
	os.makedirs(PLOT_OUT_PATH, exist_ok=True)
	#timestamp	= datetime.now().strftime('%Y%m%d-%H%M%S')
	#filename	= f"{PLOT_OUT_PATH}medals_{noc}_{medals_type}_{timestamp}.png"
	filename	= f"{PLOT_OUT_PATH}medals_{noc}_{medals_type}.png"
	fig.savefig(filename, dpi=100, bbox_inches='tight')
	print(f"Plot saved to {filename}")
	return filename


def plot_medals(medals_series, noc, medals_type='S', save=False):
	"""Plot the medals series and optionally save to file.
	@param medals_series: pandas Series with medals data indexed by year
	@param noc: Country code (NOC)
	@param medals_type: Type of medals ('S' for Summer, 'W' for Winter, 'B' for Both)
	@param save: Boolean flag to save the plot to file (default False)
	"""
	fig, ax = plt.subplots(figsize=(12, 6))
	ax.plot(medals_series, linewidth=2, marker='o')
	ax.set_xlabel('Year', fontsize=12)
	ax.set_ylabel('Total Medals', fontsize=12)
	ax.set_title(f'{noc} Total Medals by Year', fontsize=14)
	
	# Generate x-axis ticks based on medal type
	if medals_type == 'S':
		# Summer Olympics: every 4 years starting from 1896
		x_ticks = list(range(1896, 2028, 4))
	elif medals_type == 'W':
		# Winter Olympics: 1896-1992 every 4 years, then 1994 onwards every 4 years
		x_ticks = list(range(1896, 1996, 4)) + list(range(1994, 2028, 4))
		x_ticks = sorted(set(x_ticks))  # Remove duplicates and sort
	else:  # medals_type == 'B'
		# Both: every 4 years starting from 1896
		x_ticks = list(range(1896, 2028, 4))
	
	ax.set_xticks(x_ticks)
	ax.set_xticklabels([str(year) for year in x_ticks], rotation=45)
	
	# Set y-axis to start from 0
	ax.set_ylim(bottom=0)
	ax.yaxis.set_major_locator(plt.MaxNLocator(nbins=10, min_n_ticks=1))	# type: ignore
	
	# Add gridlines only on x (every 4 years) and y
	ax.grid(True, which='major', alpha=0.3, axis='both')
	ax.set_axisbelow(True)
	
	plt.tight_layout()
	
	# Save the plot if requested
	if save:
		save_plot(fig, noc, medals_type=medals_type)



if __name__ == "__main__":

	if len(sys.argv) <= 1:
		print_usage()
		sys.exit(1)
	
	# Get medals type from command line argument, default to 'S' (Summer)
	medals_type = sys.argv[1] if len(sys.argv) > 1 else 'S'
	if medals_type not in ['S', 'W', 'B']:
		print("Invalid medals type. Use 'S' for Summer, 'W' for Winter, 'B' for Both.")
		sys.exit(1)

	# Get NOC from command line argument, default to 'USA'
	noc = sys.argv[2] if len(sys.argv) > 2 else 'USA'
	
	# Get save_plot flag from command line argument, default to 0
	save_plot_flag = sys.argv[3] if len(sys.argv) > 3 else '0'
	if save_plot_flag not in ['0', '1']:
		print("Invalid save_plot flag. Use '0' for no save, '1' to save the plot.")
		sys.exit(1)

	# Load the medals series
	medals_series = load_medals_series(country=noc, medals_type=medals_type)
	print(f"Loaded medals series for {noc} (printing head):")
	print(medals_series.head())

	# Plot the medals
	plot_medals(medals_series, noc, medals_type=medals_type, save=(save_plot_flag == '1'))
