import sys
sys.path.append('src/scripts/')

import argparse
from statsmodels.tsa.stattools import adfuller

from util.load_ds import load_medals_series, get_series_log_diff, DsMedalsDataType
from util.plot_medals import plot_medals
from util.util import print_ds



PLOT_OUT_PATH = 'out/plot/'


def perform_adf_test(series):
	result = adfuller(series)
	print(f'ADF Statistic: {result[0]}')
	print(f'p-value: {result[1]}')
	


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
	
	parser.add_argument(
		'--skip-log-diff',
		action='store_true',
		help='Skip log-differenced analysis'
	)
	
	parser.add_argument(
		'--skip-percentage',
		action='store_true',
		help='Skip percentage analysis'
	)
	
	args = parser.parse_args()

	noc				= args.noc
	medals_season	= args.season
	save_plot_flag	= args.save
	year_start		= args.start_year
	year_end		= args.end_year
	verbose			= args.verbose
	skip_log_diff	= args.skip_log_diff
	skip_percentage	= args.skip_percentage


	#
	# Default
	#

	# Load the medals series
	medals_series = load_medals_series(country=noc, medals_season=medals_season, year_start=year_start, year_end=year_end)
	print_ds(medals_series, f"{noc} medals series", verbose)
	
	# Apply the ADF test function
	print(f"\nPerforming ADF test on {noc} medals series:")
	perform_adf_test(medals_series)

	# Plot the medals
	plot_medals(medals_series, noc, medals_season=medals_season,
			out_file_tag=f'{year_start}-{year_end}', save=save_plot_flag)


	#
	# Log-Differenced
	#
	
	if not args.skip_log_diff:
		medals_log_diff = get_series_log_diff(medals_series)
		print_ds(medals_log_diff, f"{noc} medals series (log-differenced)", verbose)

		print(f"\nPerforming ADF test on {noc} medals series (log-differenced):")
		perform_adf_test(medals_log_diff)

		plot_medals(medals_log_diff, noc, medals_season=medals_season, y_min=None,
			out_file_tag=f'{year_start}-{year_end}_log_diff', save=save_plot_flag)


	#
	# Percentage
	#

	if not args.skip_percentage:
		medals_percentage = load_medals_series(country=noc, medals_season=medals_season,
										data_type=DsMedalsDataType.PERCENTAGE, year_start=year_start, year_end=year_end)
		print_ds(medals_percentage, f"{noc} medals series (percentage)", verbose)

		print(f"\nPerforming ADF test on {noc} medals series (percentage):")
		perform_adf_test(medals_percentage)

		plot_medals(medals_percentage, noc, medals_season=medals_season,
			out_file_tag=f'{year_start}-{year_end}_perc', save=save_plot_flag)

	