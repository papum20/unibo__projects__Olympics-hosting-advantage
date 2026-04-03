import sys
sys.path.append('src/scripts/')

import argparse
import os

import matplotlib.pyplot as plt
import statsmodels.api as sm
from statsmodels.tsa.stattools import adfuller, grangercausalitytests

from util.load_ds import (
	load_gdp_series,
	load_medals_series,
	merge_series,
	DsGdpDataType,
	DsMedalsDataType
)
from util.plot_gdp import plot_gdp
from util.plot_medals import plot_medals
from util.util import print_ds



PLOT_OUT_PATH = 'out/plot/'





def perform_tests(merged_df):
	
	# ADF GDP
	result = adfuller(merged_df['GDP'], regression='c')
	print(f'ADF Statistic: {result[0]}')
	print(f'p-value: {result[1]}')

	# ADF medals
	result = adfuller(merged_df['Medals'], regression='c')
	print(f'ADF Statistic: {result[0]}')
	print(f'p-value: {result[1]}')

	# Granger
	# maxlag=2 means we check the previous 1 and 2 Olympics
	results = grangercausalitytests(merged_df, maxlag=2)
	print("\nGranger causality test results:")
	for lag, test_results in results.items():
		print(f"Lag {lag}:")
		for key, value in test_results[0].items():
			print(f"  {key}: {value}")


def save_plot(fig, country_code, out_file_tag=None):
	"""Save the plot to file."""
	os.makedirs(PLOT_OUT_PATH, exist_ok=True)
	if out_file_tag is not None:
		filename = f"{PLOT_OUT_PATH}merged_{country_code}_medals_gdp_{out_file_tag}.png"
	else:
		filename = f"{PLOT_OUT_PATH}merged_{country_code}_medals_gdp.png"
	fig.savefig(filename, dpi=100, bbox_inches='tight')
	print(f"Plot saved to {filename}")
	return filename


def plot_merged_series(medals_series, gdp_series, country_code, country_name, out_file_tag=None, save=False):
	"""Plot both medals and GDP series side by side.
	@param medals_series: pandas Series with medals data indexed by year
	@param gdp_series: pandas Series with GDP data indexed by year
	@param country_code: Country code (NOC)
	@param country_name: Country name for title
	@param save: Boolean flag to save the plot to file (default False)
	"""
	fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
	
	# Plot medals
	ax1.plot(medals_series, linewidth=2, marker='o', color='#1f77b4')
	ax1.set_xlabel('Year', fontsize=12)
	ax1.set_ylabel('Medals', fontsize=12)
	ax1.set_title(f'{country_name} Medals Over Time', fontsize=14)
	ax1.set_ylim(bottom=0)
	ax1.grid(True, which='major', alpha=0.3, axis='both')
	ax1.set_axisbelow(True)
	
	# Generate x-axis ticks every 10 years
	x_ticks = list(range(int(medals_series.index.min()), int(medals_series.index.max()) + 1, 10))
	ax1.set_xticks(x_ticks)
	ax1.set_xticklabels([str(year) for year in x_ticks], rotation=45)
	
	# Plot GDP
	ax2.plot(gdp_series, linewidth=2, marker='o', color='#ff7f0e')
	ax2.set_xlabel('Year', fontsize=12)
	ax2.set_ylabel('GDP (log-differenced)', fontsize=12)
	ax2.set_title(f'{country_name} GDP Growth Over Time', fontsize=14)
	ax2.grid(True, which='major', alpha=0.3, axis='both')
	ax2.set_axisbelow(True)
	
	# Generate x-axis ticks every 10 years
	x_ticks = list(range(int(gdp_series.index.min()), int(gdp_series.index.max()) + 1, 10))
	ax2.set_xticks(x_ticks)
	ax2.set_xticklabels([str(year) for year in x_ticks], rotation=45)
	
	plt.tight_layout()
	
	# Save the plot if requested
	if save:
			save_plot(fig, country_code, out_file_tag=out_file_tag)

def plot_merged_series2(medals_series, gdp_series, country_code, country_name, out_file_tag=None, save=False):
	"""Plot both medals and GDP series side by side.
	@param medals_series: pandas Series with medals data indexed by year
	@param gdp_series: pandas Series with GDP data indexed by year
	@param country_code: Country code (NOC)
	@param country_name: Country name for title
	@param save: Boolean flag to save the plot to file (default False)
	"""
	fig, ax = plt.subplots(figsize=(14, 6))
	
	# Normalize medals by dividing by 100 (since it's a percentage)
	medals_normalized = medals_series / 100.0
	
	# Plot both series
	ax.plot(medals_normalized, linewidth=2, marker='o', color='#1f77b4', label='Medals (% / 100)')
	ax.plot(gdp_series, linewidth=2, marker='s', color='#ff7f0e', label='GDP Growth (log-diff)')
	
	# Plot medals
	ax.set_xlabel('Year', fontsize=12)
	ax.set_ylabel('Value (normalized scale)', fontsize=12)
	ax.set_title(f'{country_name} Medals vs GDP Growth', fontsize=14)
	ax.legend(fontsize=11, loc='best')
	ax.grid(True, which='major', alpha=0.3, axis='both')
	ax.set_axisbelow(True)
	
	# Generate x-axis ticks every 10 years
	min_year = min(int(medals_normalized.index.min()), int(gdp_series.index.min()))
	max_year = max(int(medals_normalized.index.max()), int(gdp_series.index.max()))
	x_ticks = list(range(min_year, max_year + 1, 10))
	ax.set_xticks(x_ticks)
	ax.set_xticklabels([str(year) for year in x_ticks], rotation=45)

	plt.tight_layout()
	
	# Save the plot if requested
	if save:
			save_plot(fig, country_code, out_file_tag=out_file_tag)



if __name__ == "__main__":

	parser = argparse.ArgumentParser(
		description='Perform ADF stationarity test on Olympic medals data'
	)
	
	# Required arguments
	parser.add_argument(
		'-s', '--season',
		type=str,
		default='S',
		choices=['S', 'W', 'B'],
		help='Season: S (Summer), W (Winter), B (Both) - default: S'
	)
	
	# Optional arguments
	parser.add_argument(
		'-n', '--noc',
		type=str,
		default='USA',
		help='Country code (NOC) - default: USA'
	)
	
	parser.add_argument(
		'--start-year',
		type=int,
		default=1896,
		help='Starting year for the data - default: 1896'
	)
	
	parser.add_argument(
		'--end-year',
		type=int,
		default=2026,
		help='Ending year for the data - default: 2026'
	)
	
	parser.add_argument(
		'--save',
		action='store_true',
		help='Save plots to file (flag, no value needed)'
	)

	parser.add_argument(
		'-v', '--verbose',
		action='store_true',
		help='Verbose output (flag, no value needed)'
	)
	
	args = parser.parse_args()

	noc				= args.noc
	medals_season	= args.season
	save_plot_flag	= args.save
	year_start		= args.start_year
	year_end		= args.end_year
	verbose			= args.verbose


	COL_GDP		= 'GDP'
	COL_MEDALS	= 'Medals'


	#
	# Default
	#

	gdp_series, country_name = load_gdp_series(noc, year_start=year_start, year_end=year_end,
									data_type=DsGdpDataType.LN_DIFF)
	medals_series = load_medals_series(country=noc, medals_season=medals_season,
						year_start=year_start, year_end=year_end, data_type=DsMedalsDataType.PERCENTAGE)

	merged_df = merge_series(medals_series, gdp_series, series1_name=COL_MEDALS, series2_name=COL_GDP)

	actual_year_start	= max(merged_df.index.min(), year_start)
	actual_year_end		= min(merged_df.index.max(), year_end)
	print(f"Using data from {actual_year_start} to {actual_year_end} (requested: {year_start}-{year_end})")

	print_ds(merged_df[COL_GDP],	f"{country_name} GDP series",	verbose)
	print_ds(merged_df[COL_MEDALS],	f"{noc} medals series",			verbose)

	perform_tests(merged_df)

	# Plot
	plot_gdp(gdp_series, noc, country_name, y_min=None,
		out_file_tag=f'{actual_year_start}-{actual_year_end}_log_diff', save=save_plot_flag)

	plot_medals(medals_series, noc, medals_season=medals_season,
		out_file_tag=f'{actual_year_start}-{actual_year_end}_perc', save=save_plot_flag)
	
	plot_merged_series2(merged_df[COL_MEDALS], merged_df[COL_GDP], noc, country_name,
			out_file_tag=f'{actual_year_start}-{actual_year_end}', save=save_plot_flag)

