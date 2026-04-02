import sys
sys.path.append('src/scripts/')

import numpy as np
from statsmodels.tsa.stattools import adfuller

from util.plot_gdp import load_gdp_series, plot_gdp



DS_PATH = 'dataset/worldBankOpenData_GDP_USA.csv'
PLOT_OUT_PATH = 'out/plot/'



def print_usage():
	print("""
	   Usage:
		python adf_gdp.py <Country_Code> [0|1]
		- Country_Code: Mandatory country code (e.g., USA, GBR, CHN, etc.)
		- 0|1: Optional flag to indicate whether save the plot to file (default 0)
	""")


def perform_adf_test(series):
	result = adfuller(series, regression='ct')
	print(f'ADF Statistic: {result[0]}')
	print(f'p-value: {result[1]}')
	

def get_series_log_diff(series):
	"""Helper function to get the log-differenced series for plotting.
	@param series: pandas Series with GDP values indexed by year
	@return: pandas Series of log-differenced GDP (growth rates)
	"""
    # Take the natural log of GDP
	ln_gdp = np.log(series)
    # Take the first difference of the log (% growth rate)
	gdp_growth_rate = ln_gdp.diff().dropna()
	return gdp_growth_rate



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


	# Load the GDP series
	try:
		gdp_series, country_name = load_gdp_series(country_code)
		print(f"Loaded GDP series for {country_name} ({country_code}):")
		print(gdp_series.head())
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
	plot_gdp(gdp_series, country_code, country_name, save=(save_plot_flag == '1'))


	#
	# GDP log-differenced
	#

	gdp_ln_diff = get_series_log_diff(gdp_series)
	print(f"\nLog-differenced GDP series for {country_code} (printing head):")
	print(gdp_ln_diff.head())

	print(f"\nPerforming ADF test on {country_code} GDP series (log-differenced):")
	perform_adf_test(gdp_ln_diff)

	plot_gdp(gdp_ln_diff, country_code, country_name, y_min=None, out_file_tag='log_diff', save=(save_plot_flag == '1'))


