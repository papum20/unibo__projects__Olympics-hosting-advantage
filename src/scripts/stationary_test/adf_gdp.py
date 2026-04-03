import sys
sys.path.append('src/scripts/')

import argparse
from statsmodels.tsa.stattools import adfuller

from util.load_ds import load_gdp_series, get_series_log_diff
from util.plot_gdp import load_gdp_series, plot_gdp
from util.common import print_ds



PLOT_OUT_PATH = 'out/plot/'


def perform_adf_test(series):
	result = adfuller(series, regression='ct')
	print(f'ADF Statistic: {result[0]}')
	print(f'p-value: {result[1]}')



if __name__ == "__main__":

	parser = argparse.ArgumentParser(
		description='Perform ADF stationarity test on Olympic medals data'
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

	country_code	= args.noc
	save_plot_flag	= args.save
	year_start		= args.start_year
	year_end		= args.end_year
	verbose			= args.verbose
	skip_log_diff	= args.skip_log_diff
	skip_percentage	= args.skip_percentage


	# Load the GDP series
	try:
		gdp_series, country_name = load_gdp_series(country_code, year_start=year_start, year_end=year_end)
		print_ds(gdp_series, f"{country_code} GDP series", verbose)
	except ValueError as e:
		print(f"Error: {e}")
		sys.exit(1)

	#
	# GDP 
	#
	
	# Apply the ADF test function
	print(f"\nPerforming ADF test on {country_code} GDP series:")
	perform_adf_test(gdp_series)

	# Plot the GDP
	plot_gdp(gdp_series, country_code, country_name, year_start, year_end,
		save=save_plot_flag)


	#
	# GDP log-differenced
	#

	gdp_ln_diff = get_series_log_diff(gdp_series)
	print_ds(gdp_ln_diff, f"{country_code} GDP series (log-differenced)", verbose)

	print(f"\nPerforming ADF test on {country_code} GDP series (log-differenced):")
	perform_adf_test(gdp_ln_diff)

	plot_gdp(gdp_ln_diff, country_code, country_name, year_start, year_end, y_min=None,
		out_file_tag='log_diff', save=save_plot_flag)


