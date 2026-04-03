import os
import sys

import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator

from util.load_ds import load_gdp_series



PLOT_OUT_PATH = 'out/plot/'



def print_usage():
	print("""
	   Usage:
		python plot_gdp.py <Country_Code> [0|1] [START_YEAR] [END_YEAR]
		- Country_Code: Mandatory country code (e.g., USA, GBR, CHN, etc.)
		- 0|1: Optional flag to indicate whether save the plot to file (default 0)
		- START_YEAR: Optional start year for the plot (default 1960)
		- END_YEAR: Optional end year for the plot (default 2025)
	""")


def save_plot(fig, country_code, out_file_tag=None):
	"""Save the plot to file."""
	os.makedirs(PLOT_OUT_PATH, exist_ok=True)
	if out_file_tag is not None:
		filename = f"{PLOT_OUT_PATH}gdp_{country_code}_{out_file_tag}.png"
	else:
		filename = f"{PLOT_OUT_PATH}gdp_{country_code}.png"
	fig.savefig(filename, dpi=100, bbox_inches='tight')
	print(f"Plot saved to {filename}")
	return filename


def plot_gdp(gdp_series, country_code, country_name, y_min: float|None=0, out_file_tag=None, save=False):
	"""Plot the GDP series and optionally save to file.
	@param gdp_series: pandas Series with GDP data indexed by year
	@param country_code: Country code
	@param country_name: Country name for title
	@param y_min: Minimum value for y-axis (default 0)
	@param out_file_tag: Tag for the output file name
	@param save: Boolean flag to save the plot to file (default False)
	"""
	fig, ax = plt.subplots(figsize=(12, 6))
	ax.plot(gdp_series, linewidth=2, marker='o')
	ax.set_xlabel('Year', fontsize=12)
	ax.set_ylabel('GDP (USD)', fontsize=12)
	ax.set_title(f'{country_name} ({country_code}) GDP Over Time', fontsize=14)
	
	# Generate x-axis ticks every 5 years starting from 1960
	x_ticks = list(range(1960, 2026, 5))
	ax.set_xticks(x_ticks)
	ax.set_xticklabels([str(year) for year in x_ticks], rotation=45)
	
	# Set y-axis to start from 0
	ax.set_ylim(bottom=y_min)
	ax.yaxis.set_major_locator(plt.MaxNLocator(nbins=10, min_n_ticks=1))	# type: ignore
	ax.yaxis.set_minor_locator(AutoMinorLocator())	# type: ignore
	
	# Add gridlines for both major and minor ticks
	ax.grid(True, which='major', alpha=0.3, axis='both')
	ax.grid(True, which='minor', alpha=0.15, axis='y')
	ax.set_axisbelow(True)
	
	plt.tight_layout()
	
	# Save the plot if requested
	if save:
		save_plot(fig, country_code, out_file_tag=out_file_tag)
	


if __name__ == "__main__":

	if len(sys.argv) <= 1:
		print_usage()
		sys.exit(1)
	
	# Get country code from command line argument (mandatory)
	country_code = sys.argv[1]
	
	# Get save_plot flag from command line argument, default to 0
	save_plot_flag = sys.argv[2] if len(sys.argv) > 2 else '0'
	if save_plot_flag not in ['0', '1']:
		print("Invalid save_plot flag. Use '0' for no save, '1' to save the plot.")
		sys.exit(1)

	# Get start and end years from command line arguments, default to 1960 and 2025
	year_start	= int(sys.argv[3]) if len(sys.argv) > 3 else 1960
	year_end	= int(sys.argv[4]) if len(sys.argv) > 4 else 2025

	# Load the GDP series
	try:
		gdp_series, country_name = load_gdp_series(country_code, year_start=year_start, year_end=year_end)
		print(f"Loaded GDP series for {country_name} ({country_code}):")
		print(gdp_series.head())
	except ValueError as e:
		print(f"Error: {e}")
		sys.exit(1)

	# Plot the GDP
	plot_gdp(gdp_series, country_code, country_name, save=(save_plot_flag == '1'))