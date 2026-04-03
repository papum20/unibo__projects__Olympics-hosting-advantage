import sys
sys.path.append('src/scripts/')

import os

import matplotlib.pyplot as plt

from util.load_ds import load_medals_series, GDP_WBOD_YEAR_FIRST, GDP_WBOD_YEAR_LAST



PLOT_OUT_PATH = 'out/plot/'



def print_usage():
	print(f"""
	   Usage:
		python plot_medals.py <S|W|B> [NOC] [0|1] [START_YEAR] [END_YEAR]
		- S|W|B: flag to indicate the season of medals (Summer, Winter, or Both).
		- NOC: Optional country code (NOC) to filter by. If not provided, defaults to 'USA'.
		- 0|1: Optional flag to indicate whether save the plot to file (default 0)
		- START_YEAR: Optional start year for the plot (default {GDP_WBOD_YEAR_FIRST})
		- END_YEAR: Optional end year for the plot (default {GDP_WBOD_YEAR_LAST})
	""")


def save_plot(
	fig,
	noc,
	year_start,
	year_end,
	medals_season='S',
	out_file_tag=None
):
	"""Save the plot with a timestamp in the filename."""
	os.makedirs(PLOT_OUT_PATH, exist_ok=True)
	#timestamp	= datetime.now().strftime('%Y%m%d-%H%M%S')
	#filename	= f"{PLOT_OUT_PATH}medals_{noc}_{medals_season}_{timestamp}.png"
	if out_file_tag is not None:
		filename	= f"{PLOT_OUT_PATH}medals_{noc}_{medals_season}_{year_start}-{year_end}_{out_file_tag}.png"
	else:
		filename	= f"{PLOT_OUT_PATH}medals_{noc}_{medals_season}_{year_start}-{year_end}.png"
	fig.savefig(filename, dpi=100, bbox_inches='tight')
	print(f"Plot saved to {filename}")
	return filename


def plot_medals(
	medals_series,
	noc,
	year_start		: int,
	year_end		: int,
	medals_season					= 'S',
	y_min			: float|None	= 0,
	out_file_tag					= None,
	save							= False
):
	"""Plot the medals series and optionally save to file.
	@param medals_series: pandas Series with medals data indexed by year
	@param noc: Country code (NOC)
	@param year_start: Start year for the plot
	@param year_end: End year for the plot
	@param medals_season: Season of medals ('S' for Summer, 'W' for Winter, 'B' for Both)
	@param y_min: Minimum value for the y-axis
	@param out_file_tag: Optional tag to append to the output filename
	@param save: Boolean flag to save the plot to file (default False)
	"""
	fig, ax = plt.subplots(figsize=(12, 6))
	ax.plot(medals_series, linewidth=2, marker='o')
	ax.set_xlabel('Year', fontsize=12)
	ax.set_ylabel('Total Medals', fontsize=12)
	ax.set_title(f'{noc} Total Medals by Year', fontsize=14)
	
	# Generate x-axis ticks based on medal type
	if medals_season == 'S':
		# Summer Olympics: every 4 years starting from 1896
		x_ticks = list(range(1896, 2028, 4))
	elif medals_season == 'W':
		# Winter Olympics: 1896-1992 every 4 years, then 1994 onwards every 4 years
		x_ticks = list(range(1896, 1996, 4)) + list(range(1994, 2028, 4))
		x_ticks = sorted(set(x_ticks))  # Remove duplicates and sort
	else:  # medals_type == 'B'
		# Both: every 4 years starting from 1896
		x_ticks = list(range(1896, 2028, 4))
	
	ax.set_xticks(x_ticks)
	ax.set_xticklabels([str(year) for year in x_ticks], rotation=45)
	
	# Set y-axis to start from 0
	ax.set_ylim(bottom=y_min)
	ax.yaxis.set_major_locator(plt.MaxNLocator(nbins=10, min_n_ticks=1))	# type: ignore
	
	# Add gridlines only on x (every 4 years) and y
	ax.grid(True, which='major', alpha=0.3, axis='both')
	ax.set_axisbelow(True)
	
	plt.tight_layout()
	
	# Save the plot if requested
	if save:
		save_plot(fig, noc, medals_season=medals_season, out_file_tag=out_file_tag, year_start=year_start, year_end=year_end)



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

	# Get start and end years from command line arguments, default to 1896 and 2026
	year_start	= int(sys.argv[4]) if len(sys.argv) > 4 else GDP_WBOD_YEAR_FIRST
	year_end	= int(sys.argv[5]) if len(sys.argv) > 5 else GDP_WBOD_YEAR_LAST

	# Load the medals series
	medals_series = load_medals_series(country=noc, medals_season=medals_type, year_start=year_start, year_end=year_end)
	print(f"Loaded medals series for {noc} (printing head):")
	print(medals_series.head())

	# Plot the medals
	plot_medals(medals_series, noc, year_start=year_start, year_end=year_end, medals_season=medals_type, save=(save_plot_flag == '1'))
