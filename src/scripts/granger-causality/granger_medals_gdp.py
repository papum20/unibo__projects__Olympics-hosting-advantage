import sys
sys.path.append('src/scripts/')

import argparse
import os

import matplotlib.pyplot as plt
import pandas as pd
import statsmodels.api as sm
from statsmodels.tsa.stattools import adfuller, grangercausalitytests
from statsmodels.discrete.count_model import ZeroInflatedNegativeBinomialP

from util.load_ds import (
	load_gdp_series,
	load_medals_series,
	load_stacked_countries,
	merge_series,
	DsGdpDataType,
	DsMedalsDataType,
	DsPopDataType,
	DS_GDP_WBOD_PATH,
	DS_GDPPC_MADDISON_PATH,
	DF_COL_GDP,
	DF_COL_IS_BOYCOTT,
	DF_COL_IS_COMMUNIST,
	DF_COL_IS_HOST,
	DF_COL_IS_HOST_PRE,
	DF_COL_IS_HOST_POST,
	DF_COL_MEDALS,
	DF_COL_POPULATION,
	DF_COL_IS_HOST_OG_YEAR,
	DF_COL_IS_HOST_PRE_YEAR,
	DF_COL_IS_HOST_POST_YEAR
)
from util.plot_gdp import plot_gdp
from util.plot_medals import plot_medals
from util.common import print_ds



PLOT_OUT_PATH = 'out/plot/'

CTRL_VARS_DICT = {
	'GDP':		DF_COL_GDP,
	'POP':		DF_COL_POPULATION,
	'BOYCOTT':	DF_COL_IS_BOYCOTT,
	'COMM':		DF_COL_IS_COMMUNIST,
	'HOST':		DF_COL_IS_HOST,
	'PRE':		DF_COL_IS_HOST_PRE,
	'POST':		DF_COL_IS_HOST_POST
}
CTRL_VARS = CTRL_VARS_DICT.keys()



def perform_granger_manual(merged_df: pd.DataFrame, ctrl_vars=CTRL_VARS):
	"""
	Do Granger manually, without lag, possibly using an already lagged dataset.
	Granger wouldn't allow to not use lags, so we need to use a standard OLS regression.
	"""

	# ADF GDP
	result = adfuller(merged_df[DF_COL_GDP], regression='c')
	print(f'ADF Statistic: {result[0]}')
	print(f'p-value: {result[1]}')

	# ADF medals
	result = adfuller(merged_df[DF_COL_MEDALS], regression='c')
	print(f'ADF Statistic: {result[0]}')
	print(f'p-value: {result[1]}')

	# Granger (manual)
	# Equation: Medal_Share = intercept + coefficient * ln_GDP_Lag_2

	# X = predictor
	# X (predictors) with multiple variables
	# OLS requires numbers, not bool
	ctrl_vars_cols = [CTRL_VARS_DICT.get(var) for var in ctrl_vars if var in CTRL_VARS_DICT]
	X = merged_df[ctrl_vars_cols]
	for col in [DF_COL_IS_BOYCOTT, DF_COL_IS_COMMUNIST, DF_COL_IS_HOST]:
		if col in X.columns:
			X[col] = X[col].astype(int)

	# Y = what we are predicting
	Y = merged_df[DF_COL_MEDALS]

	# Add a constant (intercept) to the model
	X = sm.add_constant(X)

	model = sm.OLS(Y, X).fit()
	print(model.summary())



def perform_global_panel_regression(global_df: pd.DataFrame, use_separate_host_vars=False, ctrl_vars=CTRL_VARS,
									use_hc3=True, use_zinb=False):
	"""
	Perform a global panel regression with multiple countries stacked together.
	`Is_Host` is always used as predictor control variable, while the others can be included optionally.
	@param global_df: DataFrame containing the merged data for all countries, with columns for medals, GDP, population, host status, etc.
	@param use_separate_host_vars: Whether to use separate binary variables for hosting, pre-hosting, and post-hosting instead of a single Is_Host variable
	@param ctrl_vars: Use this list of control variables instead of all
	"""

	print("\n--- Running Global Panel OLS Regression ---")
	# Define our variables
	Y = global_df[DF_COL_MEDALS]
	
	predictors = []
	
	# Include all the control variables in X
	# Notice we use Population, GDP, Host, Pre, Post, Communist, and Boycott all at once.
	predictors += [CTRL_VARS_DICT.get(var) for var in ctrl_vars
		if var in CTRL_VARS_DICT and var not in ['HOST', 'PRE', 'POST']]


	if use_separate_host_vars:
		years = global_df['Year'].unique()
		if 'HOST' in ctrl_vars:
			predictors += [DF_COL_IS_HOST_OG_YEAR(year)		for year in years]
		if 'PRE' in ctrl_vars:
			predictors += [DF_COL_IS_HOST_PRE_YEAR(year)	for year in years]
		if 'POST' in ctrl_vars:
			predictors += [DF_COL_IS_HOST_POST_YEAR(year)	for year in years]
	else:
		if 'HOST' in ctrl_vars:
			predictors += [DF_COL_IS_HOST]
		if 'PRE' in ctrl_vars:
			predictors += [DF_COL_IS_HOST_PRE]
		if 'POST' in ctrl_vars:
			predictors += [DF_COL_IS_HOST_POST]

	print(f"{predictors = }")
	print(f"{len(predictors) = }")

	# Ensure they are numeric
	X = global_df[predictors].astype(float)
	X = sm.add_constant(X)

	# Run the massive multi-variable OLS
	# HC3 is standard for robust errors (heteroskedasticity-consistent)
	# not working for separate vars
	if use_zinb:
		model = ZeroInflatedNegativeBinomialP(Y, X).fit()
	elif use_hc3:
		model = sm.OLS(Y, X).fit(cov_type='HC3')
	else:
		model = sm.OLS(Y, X).fit()
	print(model.summary())
	


def perform_tests(merged_df):
	
	# ADF GDP
	result = adfuller(merged_df[DF_COL_GDP], regression='c')
	print(f'ADF Statistic: {result[0]}')
	print(f'p-value: {result[1]}')

	# ADF medals
	result = adfuller(merged_df[DF_COL_MEDALS], regression='c')
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

	plt.close(fig)



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
		nargs='+',
		default=['USA'],
		help='Country code(s) (NOC) - space-separated list - default: USA'
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
		'--max-lag',
		type=int,
		default=7,
		help='Maximum lag for the Granger causality test - default: 7'
	)

	parser.add_argument(
		'--ctrl-vars',
		type=str,
		nargs='+',
		default=CTRL_VARS,
		help=f'Custom control variables to include in the regression (space-separated list), in [{", ".join(CTRL_VARS)}]'
	)

	parser.add_argument(
		'--exclude-boycott',
		action='store_true',
		help='Exclude boycott years from the analysis (flag, no value needed)'
	)

	parser.add_argument(
		'--gdp-avg',
		action='store_true',
		help='Use 4-year geometric mean of GDP instead of raw values (flag, no value needed)'
	)

	parser.add_argument(
		'--gdp-tot',
		action='store_true',
		help='Use GDP instead of GDPpc (flag, no value needed)'
	)

	parser.add_argument(
		'--pop-avg',
		action='store_true',
		help='Use 4-year geometric mean of population instead of raw values (flag, no value needed)'
	)
	
	parser.add_argument(
		'--sep-host',
		action='store_true',
		help='Use separate binary variables for hosting, pre-hosting, and post-hosting instead of a single Is_Host variable (flag, no value needed)'
	)
	
	parser.add_argument(
		'--reg-zinb',
		action='store_true',
		help='Use Zero-Inflated Negative Binomial regression (flag, no value needed)'
	)
	
	parser.add_argument(
		'--reg-hc3',
		action='store_true',
		help='Use HC3, for robust errors (flag, no value needed)'
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

	noc_list			= args.noc
	medals_season		= args.season
	save_plot_flag		= args.save
	year_start			= args.start_year
	year_end			= args.end_year
	max_lag				= args.max_lag
	
	ctrl_vars			= args.ctrl_vars
	exclude_boycott		= args.exclude_boycott
	use_gdp_mean		= args.gdp_avg
	use_gdp_tot			= args.gdp_tot
	use_population_mean	= args.pop_avg
	use_sep_host_vars	= args.sep_host
	use_reg_zinb		= args.reg_zinb
	use_reg_hc3			= args.reg_hc3
	verbose				= args.verbose

	if any(var not in CTRL_VARS for var in ctrl_vars):
		print(f"Error: Invalid control variable specified in --ctrl-vars-custom. Allowed values are: {', '.join(CTRL_VARS)}")
		sys.exit(1)

	DS_GDP_PATH = DS_GDP_WBOD_PATH if use_gdp_tot else DS_GDPPC_MADDISON_PATH


	#
	# Granger
	#

	if len(noc_list) == 1:
	
		noc = noc_list[0]
	
		gdp_series, country_name = load_gdp_series(noc, year_start=year_start, year_end=year_end,
										data_type=DsGdpDataType.LN_DIFF, dataset_path=DS_GDP_PATH)

		medals_series = load_medals_series(country=noc, medals_season=medals_season,
							year_start=year_start, year_end=year_end, data_type=DsMedalsDataType.PERCENTAGE)

		merged_df = merge_series(medals_series, gdp_series, series1_name=DF_COL_MEDALS, series2_name=DF_COL_GDP)

		actual_year_start	= max(merged_df.index.min(), year_start)
		actual_year_end		= min(merged_df.index.max(), year_end)
		print(f"Using data from {actual_year_start} to {actual_year_end} (requested: {year_start}-{year_end})")

		print_ds(merged_df[DF_COL_GDP],	f"{country_name} GDP series",	verbose)
		print_ds(merged_df[DF_COL_MEDALS],	f"{noc} medals series",			verbose)

		perform_tests(merged_df)

		# Plot
		plot_gdp(gdp_series, noc, country_name, actual_year_start, actual_year_end, y_min=None,
			out_file_tag='log_diff', save=save_plot_flag)

		plot_medals(medals_series, noc, actual_year_start, actual_year_end, medals_season=medals_season,
			out_file_tag='perc', save=save_plot_flag)
		
		plot_merged_series2(merged_df[DF_COL_MEDALS], merged_df[DF_COL_GDP], noc, country_name,
				out_file_tag=f'{actual_year_start}-{actual_year_end}', save=save_plot_flag)


	#
	# Granger (manual)
	#

	for shift in range(1, max_lag + 1):
		print(f"\nGranger causality test (manual) with lag {shift}:")

		#if len(noc_list) == 1:
		#	noc = noc_list[0]

		#	merged_df, country_name = load_medals_gdp_and_population_aligned(
		#		noc,
		#		medals_season			= medals_season,
		#		year_start				= year_start,
		#		year_end				= year_end,
		#		gdp_year_shift			= shift,
		#		remove_boycott			= exclude_boycott,
		#		use_gdp_mean			= use_gdp_mean,
		#		use_population_mean		= use_population_mean,
		#		use_separate_host_vars	= use_sep_host_vars,
		#		medals_data_type		= DsMedalsDataType.PERCENTAGE,
		#		gdp_data_type			= DsGdpDataType.LN_DIFF,
		#		population_data_type	= DsPopDataType.LN_DIFF,
		#		gdp_dataset_path		= DS_GDP_PATH
		#	)
		#else:

		merged_df, country_name = load_stacked_countries(
			countries_list			= noc_list,
			medals_season			= medals_season,
			year_start				= year_start,
			year_end				= year_end,
			gdp_year_shift			= shift,
			remove_boycott			= exclude_boycott,
			use_gdp_mean			= use_gdp_mean,
			use_population_mean		= use_population_mean,
			use_separate_host_vars	= use_sep_host_vars,
			medals_data_type		= DsMedalsDataType.DEFAULT,
			gdp_data_type			= DsGdpDataType.LN_DIFF,
			population_data_type	= DsPopDataType.LN_DIFF,
			gdp_dataset_path		= DS_GDP_PATH,
			is_verbose				= verbose
		)

		actual_year_start	= max(merged_df.index.min(), year_start)
		actual_year_end		= min(merged_df.index.max(), year_end)
		print(f"Using data from {actual_year_start} to {actual_year_end} (requested: {year_start}-{year_end})")

		print_ds(merged_df[DF_COL_GDP],		f"{country_name} GDP series",			verbose)
		print_ds(merged_df[DF_COL_MEDALS],	f"{'+'.join(noc_list)} medals series",	verbose)

		if verbose:
			print("\nMerged DataFrame:")
			print(merged_df.to_string())

		if len(noc_list) == 1:
			perform_granger_manual(merged_df, ctrl_vars=ctrl_vars)

		else:
			perform_global_panel_regression(merged_df, use_separate_host_vars=use_sep_host_vars, ctrl_vars=ctrl_vars,
				use_hc3=use_reg_hc3, use_zinb=use_reg_zinb)

		# Plot

		if len(noc_list) == 1:

			gdp_series		= pd.Series(merged_df[DF_COL_GDP],		name='GDP')
			medals_series	= pd.Series(merged_df[DF_COL_MEDALS],	name='Medals')

			
			tag_boycott		= f'boycott{"N" if exclude_boycott else "Y"}'
			tag_ctrl_vars	= f'ctrl{"+".join(ctrl_vars)}'
			tag_gdp_mean	= f'gdpmean{"Y" if use_gdp_mean else "N"}'
			
			plot_gdp(gdp_series, noc, country_name, actual_year_start, actual_year_end, y_min=None,
				out_file_tag=f'log_diff_{tag_boycott}_{tag_ctrl_vars}_{tag_gdp_mean}_shift{shift}', save=save_plot_flag)

			plot_medals(medals_series, noc, actual_year_start, actual_year_end, medals_season=medals_season,
				out_file_tag=f'perc_{tag_boycott}_{tag_ctrl_vars}_{tag_gdp_mean}', save=save_plot_flag)
			
			plot_merged_series2(merged_df[DF_COL_MEDALS], merged_df[DF_COL_GDP], noc, country_name,
					out_file_tag=f'{actual_year_start}-{actual_year_end}_shift{shift}_{tag_boycott}_{tag_ctrl_vars}_{tag_gdp_mean}', save=save_plot_flag)

