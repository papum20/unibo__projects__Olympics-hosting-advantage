import sys
sys.path.append('src/scripts/')

import argparse
import os
from typing import Literal

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import statsmodels.api as sm
from statsmodels.stats.outliers_influence import variance_inflation_factor
from statsmodels.discrete.count_model import ZeroInflatedNegativeBinomialP
from statsmodels.tsa.stattools import adfuller, grangercausalitytests

from util.load_ds import (
	get_top_countries_by_medals,
	load_gdp_series,
	load_medals_series,
	load_stacked_countries,
	merge_series,
	DsGdpDataType,
	DsMedalsDataType,
	DsPopDataType,
	DS_GDP_WBOD_PATH,
	DS_GDPPC_MADDISON_PATH,
	DF_COL_AM_HISTORY,
	DF_COL_GDP,
	DF_COL_IS_BOYCOTT_URS,
	DF_COL_IS_BOYCOTT_USA,
	DF_COL_IS_COMMUNIST,
	DF_COL_IS_HOST,
	DF_COL_IS_HOST_PRE,
	DF_COL_IS_HOST_POST,
	DF_COL_IS_HOST_CLOSE_CENTER,
	DF_COL_IS_HOST_CLOSE_GMT1,
	DF_COL_IS_HOST_CLOSE_MAIN,
	DF_COL_IS_HOST_CLOSE_WEST,
	DF_COL_IS_HOST_CLOSE_WIDE,
	DF_COL_MEDALS,
	DF_COL_POPULATION,
	is_dfCol_yearDummy,
	is_dfCol_isHostOg_separate,
	is_dfCol_isHostPre_separate,
	is_dfCol_isHostPost_separate,
	is_dfCol_isHostCloseCenter_separate,
	is_dfCol_isHostClose_GMT1_separate,
	is_dfCol_isHostClose_Main_separate,
	is_dfCol_isHostClose_West_separate,
	is_dfCol_isHostClose_Wide_separate
)
from util.plot_gdp import plot_gdp
from util.plot_medals import plot_medals
from util.common import Logger, print_ds



PLOT_OUT_PATH = 'out/plot/'

CTRL_VARS_DICT = {
	'AM'			: DF_COL_AM_HISTORY,
	'GDP'			: DF_COL_GDP,
	'POP'			: DF_COL_POPULATION,
	'BOYCOTT_URS'	: DF_COL_IS_BOYCOTT_URS,
	'BOYCOTT_USA'	: DF_COL_IS_BOYCOTT_USA,
	'COMM'			: DF_COL_IS_COMMUNIST,
	'HOST'			: DF_COL_IS_HOST,
	'PRE'			: DF_COL_IS_HOST_PRE,
	'POST'			: DF_COL_IS_HOST_POST,
	'CLOSE_CENTER'	: DF_COL_IS_HOST_CLOSE_CENTER,
	'CLOSE_GMT1'	: DF_COL_IS_HOST_CLOSE_GMT1,
	'CLOSE_MAIN'	: DF_COL_IS_HOST_CLOSE_MAIN,
	'CLOSE_WEST'	: DF_COL_IS_HOST_CLOSE_WEST,
	'CLOSE_WIDE'	: DF_COL_IS_HOST_CLOSE_WIDE
}
CTRL_VARS_HOST_BY_YEAR = [
	'HOST',
	'PRE',
	'POST',
]
CTRL_VARS_CLOSE_BY_YEAR = [
	'CLOSE_CENTER',
	'CLOSE_GMT1',
	'CLOSE_MAIN',
	'CLOSE_WEST',
	'CLOSE_WIDE'
]
CTRL_VARS_BY_YEAR = CTRL_VARS_HOST_BY_YEAR + CTRL_VARS_CLOSE_BY_YEAR
CTRL_VARS = set(CTRL_VARS_DICT.keys()) | {
	'YEAR'
}



def perform_global_panel_regression(
	global_df: pd.DataFrame, use_separate_host_vars=False, use_separate_close_vars=False, ctrl_vars=CTRL_VARS,
	cov_type: Literal['nonrobust', 'fixed scale', 'HC0', 'HC1', 'HC2', 'HC3', 'HAC', 'hac-panel', 'hac-groupsum', 'cluster'] = 'nonrobust',
	use_zinb = False
):
	"""
	Perform a global panel regression with multiple countries stacked together.
	`Is_Host` is always used as predictor control variable, while the others can be included optionally.
	@param global_df: DataFrame containing the merged data for all countries, with columns for medals, GDP, population, host status, etc.
	@param use_separate_host_vars: Whether to use separate binary variables for hosting, pre-hosting, and post-hosting instead of a single Is_Host variable
	@param use_sep_close_vars: Whether to use separate binary variables for close to host variables
	@param ctrl_vars: Use this list of control variables instead of all
	"""

	print("\n--- Running Global Panel OLS Regression ---")
	# Define our variables
	Y = global_df[DF_COL_MEDALS]
	
	col_headers = global_df.columns
	predictors = []
	
	# Include all the control variables in X
	# Notice we use Population, GDP, Host, Pre, Post, Communist, and Boycott all at once.
	predictors += [CTRL_VARS_DICT.get(var) for var in ctrl_vars
		if var in CTRL_VARS_DICT and var not in CTRL_VARS_BY_YEAR]

	if 'YEAR' in ctrl_vars:
		predictors += [col for col in col_headers if is_dfCol_yearDummy(col)]

	if use_separate_host_vars:
		if 'HOST' in ctrl_vars:
			predictors += [col for col in col_headers if is_dfCol_isHostOg_separate(col)]
		if 'PRE' in ctrl_vars:
			predictors += [col for col in col_headers if is_dfCol_isHostPre_separate(col)]
		if 'POST' in ctrl_vars:
			predictors += [col for col in col_headers if is_dfCol_isHostPost_separate(col)]
	else:
		predictors += [CTRL_VARS_DICT.get(var) for var in ctrl_vars
			if var in CTRL_VARS_HOST_BY_YEAR]

	if use_separate_close_vars:
		if 'CLOSE_CENTER' in ctrl_vars:
			predictors += [col for col in col_headers if is_dfCol_isHostCloseCenter_separate(col)]
		if 'CLOSE_GMT1' in ctrl_vars:
			predictors += [col for col in col_headers if is_dfCol_isHostClose_GMT1_separate(col)]
		if 'CLOSE_MAIN' in ctrl_vars:
			predictors += [col for col in col_headers if is_dfCol_isHostClose_Main_separate(col)]
		if 'CLOSE_WEST' in ctrl_vars:
			predictors += [col for col in col_headers if is_dfCol_isHostClose_West_separate(col)]
		if 'CLOSE_WIDE' in ctrl_vars:
			predictors += [col for col in col_headers if is_dfCol_isHostClose_Wide_separate(col)]
	else:
		predictors += [CTRL_VARS_DICT.get(var) for var in ctrl_vars
			if var in CTRL_VARS_CLOSE_BY_YEAR]

	print(f"{predictors = }")
	print(f"{len(predictors) = }")

	# Ensure they are numeric
	X = global_df[predictors].astype(float)


	# Remove columns that are all zeros (empty dummies)
	cols_before = X.shape[1]
	X = X.loc[:, (X != 0).any(axis=0)]
	cols_after = X.shape[1]
	
	if cols_before != cols_after:
		print(f"Removed {cols_before - cols_after} empty/zero predictor columns.")
		print(f"Kept predictors ({cols_after}): {X.columns.tolist()}")


	# Check for multicollinearity using VIF
	try:
		vif_data = pd.DataFrame()
		vif_data["feature"] = X.columns

		vif_data["VIF"] = [variance_inflation_factor(X.values, i)
								for i in range(len(X.columns))]
		print("Check multiocollinearity using VIF:\n" + vif_data.to_string())
	except Exception as e:
		print(f"Error calculating VIF: {e}")
		print("Skipping VIF calculation.")


	X = sm.add_constant(X)

	# Add near-zero variance check
	#low_variance = X.columns[X.var() < 1e-6].tolist()
	#if low_variance:
	#	print(f"Warning: These columns have near-zero variance and may cause singularity: {low_variance}")
	#if use_zinb:
	#	try:
	#		# Try adding a small amount of regularization or changing the solver if it fails
	#		model = ZeroInflatedNegativeBinomialP(Y, X).fit(cov_type=cov_type, maxiter=500, method='bfgs')
	#	except np.linalg.LinAlgError:
	#		print("Singular matrix detected in ZINB. Standardizing X to improve condition number...")
	#		# Center and scale non-dummy variables (GDP, Population)
	#		X['GDP'] = (X['GDP'] - X['GDP'].mean()) / X['GDP'].std()
	#		X['Population'] = (X['Population'] - X['Population'].mean()) / X['Population'].std()
	#		model = ZeroInflatedNegativeBinomialP(Y, X).fit(cov_type=cov_type, maxiter=500, method='bfgs')

	# Run the massive multi-variable OLS
	# HC3 is standard for robust errors (heteroskedasticity-consistent)
	if use_zinb:
		# Check for rank sufficiency
		rank = np.linalg.matrix_rank(X.values)	# type: ignore
		if rank < X.shape[1]:
			print(f"Warning: Matrix is rank deficient ({rank} < {X.shape[1]}). "
				"Check for collinear predictors.")

		model = ZeroInflatedNegativeBinomialP(Y, X).fit(cov_type=cov_type, maxiter=500, method='bfgs')
	else:
		model = sm.OLS(Y, X).fit(cov_type=cov_type)
	print(model.summary())


def perform_adf(merged_df):
	
	# ADF GDP
	result = adfuller(merged_df[DF_COL_GDP], regression='c')
	print(f'ADF Statistic: {result[0]}')
	print(f'p-value: {result[1]}')

	# ADF medals
	result = adfuller(merged_df[DF_COL_MEDALS], regression='c')
	print(f'ADF Statistic: {result[0]}')
	print(f'p-value: {result[1]}')


def perform_granger(merged_df):

	# Granger
	# maxlag=2 means we check the previous 1 and 2 Olympics
	results = grangercausalitytests(merged_df[[DF_COL_GDP, DF_COL_MEDALS]], maxlag=2)
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

def plot_merged_series2(medals_series, gdp_series, country_code, country_name, normalize_gdp=True, out_file_tag=None, save=False):
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
	if normalize_gdp:
		gdp_normalized = gdp_series / gdp_series.max()
		ax.plot(gdp_normalized, linewidth=2, marker='s', color='#ff7f0e', label='GDP Growth (normalized)')
	else:
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

	try:

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
			default=[],
			help='Country code(s) (NOC) - space-separated list (noc-top has priority) - default: all countries (no filter)'
		)
		
		parser.add_argument(
			'--noc-top',
			type=int,
			default=0,
			help='Use the top n countries (noc-top has priority) - default: 0 (all)'
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
			'--min-lag',
			type=int,
			default=0,
			help='Minimum lag for the Granger causality test - default: 0'
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
			'--gdp-log',
			action='store_true',
			help='Use GDP logarithms (gdp-logdiff has priority) (flag, no value needed)'
		)

		parser.add_argument(
			'--gdp-logdiff',
			action='store_true',
			help='Use GDP logarithms difference (gdp-logdiff has priority) (flag, no value needed)'
		)

		parser.add_argument(
			'--med-logdiff',
			action='store_true',
			help='Use Medals logarithms difference (med-logdiff has priority) (flag, no value needed)'
		)

		parser.add_argument(
			'--med-perc',
			action='store_true',
			help='Use Medals as percentages (med-logdiff has priority) (flag, no value needed)'
		)

		parser.add_argument(
			'--pop-avg',
			action='store_true',
			help='Use 4-year geometric mean of population instead of raw values (flag, no value needed)'
		)

		parser.add_argument(
			'--pop-log',
			action='store_true',
			help='Use population logarithms (pop-logdiff has priority) (flag, no value needed)'
		)

		parser.add_argument(
			'--pop-logdiff',
			action='store_true',
			help='Use population logarithms difference (pop-logdiff has priority) (flag, no value needed)'
		)
		
		parser.add_argument(
			'--sep-host',
			action='store_true',
			help='Use separate binary variables for hosting, pre-hosting, and post-hosting and YEAR instead of a single Is_Host variable (flag, no value needed)'
		)
		
		parser.add_argument(
			'--sep-close',
			action='store_true',
			help='Use separate binary variables for close to host variables (flag, no value needed)'
		)
		
		parser.add_argument(
			'--reg-zinb',
			action='store_true',
			help='Use Zero-Inflated Negative Binomial regression (flag, no value needed)'
		)
		
		parser.add_argument(
			'--reg-hc0',
			action='store_true',
			help='Use HC0, for robust errors (HC0 has priority) (flag, no value needed)'
		)

		parser.add_argument(
			'--reg-hc3',
			action='store_true',
			help='Use HC3, for robust errors (HC0 has priority) (flag, no value needed)'
		)
		
		parser.add_argument(
			'--save',
			action='store_true',
			help='Save plots to file (flag, no value needed)'
		)

		parser.add_argument(
			'--log',
			action='store_true',
			help='Save output to a log file in out/regression/ (flag, no value needed)'
		)

		parser.add_argument(
			'-v', '--verbose',
			action='store_true',
			help='Verbose output (flag, no value needed)'
		)
		
		args = parser.parse_args()

		noc_list: list[str]	= args.noc
		noc_top				= args.noc_top
		medals_season		= args.season
		save_plot_flag		= args.save
		year_start			= args.start_year
		year_end			= args.end_year
		min_lag				= args.min_lag
		max_lag				= args.max_lag
		
		ctrl_vars			= args.ctrl_vars
		exclude_boycott		= args.exclude_boycott
		use_gdp_mean		= args.gdp_avg
		use_gdp_tot			= args.gdp_tot
		use_population_mean	= args.pop_avg
		use_sep_host_vars	= args.sep_host
		use_sep_close_vars	= args.sep_close
		use_reg_zinb		= args.reg_zinb
		use_reg_hc0			= args.reg_hc0
		use_reg_hc3			= args.reg_hc3

		gdp_type = DsGdpDataType.LN_DIFF if args.gdp_logdiff else DsGdpDataType.LN if args.gdp_log else DsGdpDataType.DEFAULT
		pop_type = DsPopDataType.LN_DIFF if args.pop_logdiff else DsPopDataType.LN if args.pop_log else DsPopDataType.DEFAULT
		medals_data_type = DsMedalsDataType.LN_DIFF if args.med_logdiff else DsMedalsDataType.PERCENTAGE if args.med_perc else DsMedalsDataType.DEFAULT

		if 'BOYCOTT' in ctrl_vars:
			ctrl_vars.remove('BOYCOTT')
			ctrl_vars += ['BOYCOTT_URS', 'BOYCOTT_USA']
		
		log_output			= args.log
		verbose				= args.verbose

		if any(var not in CTRL_VARS for var in ctrl_vars):
			print(f"Error: Invalid control variable specified in --ctrl-vars-custom. Allowed values are: {', '.join(CTRL_VARS)}")
			sys.exit(1)

		DS_GDP_PATH = DS_GDP_WBOD_PATH if use_gdp_tot else DS_GDPPC_MADDISON_PATH

		cov_type='HC0' if use_reg_hc0 else 'HC3' if use_reg_hc3 else 'nonrobust'

		if noc_top != 0:
			noc_list = get_top_countries_by_medals(year_start=year_start, year_end=year_end, n=noc_top,
										medals_season=medals_season, is_verbose=verbose)
			print(f"No specific NOCs provided. Using top {noc_top} NOCs by total medals: {noc_list}")


		if log_output:
			sys.stdout = Logger(
				noc=noc_top if noc_top != 0 else noc_list,
				year_start=year_start,
				year_end=year_end,
				lag_min=min_lag,
				lag_max=max_lag,
				reg_type='ZINB' if use_reg_zinb else 'OLS',
				cov_type=cov_type,
				gdp_type=gdp_type.name,
				pop_type=pop_type.name,
				use_gpd_avg=use_gdp_mean,
				use_pop_avg=use_population_mean,
				sep_host_vars=use_sep_host_vars,
				sep_close_vars=use_sep_close_vars,
				ctrl_vars=ctrl_vars
			)

		print(f"Running with args: {args}")


		#
		# Granger
		#

		if len(noc_list) == 1:
		
			noc = noc_list[0]
		
			gdp_series, country_name = load_gdp_series(noc, year_start=year_start, year_end=year_end,
											data_type=gdp_type, dataset_path=DS_GDP_PATH)

			medals_series = load_medals_series(country=noc, medals_season=medals_season,
								year_start=year_start, year_end=year_end, data_type=medals_data_type)

			merged_df = merge_series(medals_series, gdp_series, series1_name=DF_COL_MEDALS, series2_name=DF_COL_GDP)

			actual_year_start	= max(merged_df.index.min(), year_start)
			actual_year_end		= min(merged_df.index.max(), year_end)
			print(f"Using data from {actual_year_start} to {actual_year_end} (requested: {year_start}-{year_end})")

			print_ds(merged_df[DF_COL_GDP],	f"{country_name} GDP series",	verbose)
			print_ds(merged_df[DF_COL_MEDALS],	f"{noc} medals series",			verbose)

			perform_adf(merged_df)
			perform_granger(merged_df)

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

		for shift in range(min_lag, max_lag + 1):
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
				use_separate_close_vars	= use_sep_close_vars,
				medals_data_type		= medals_data_type,
				gdp_data_type			= gdp_type,
				population_data_type	= pop_type,
				gdp_dataset_path		= DS_GDP_PATH,
				is_verbose				= verbose
			)

			actual_year_start	= max(merged_df.index.min(), year_start)
			actual_year_end		= min(merged_df.index.max(), year_end)
			print(f"Using data from {actual_year_start} to {actual_year_end} (requested: {year_start}-{year_end})")

			print_ds(merged_df,		f"{country_name} stacked data",			verbose, n=20)

			if verbose:
				print("\nMerged DataFrame:")
				print(merged_df.to_string())

			if len(noc_list) == 1:
				perform_adf(merged_df)
				perform_granger(merged_df)

			perform_global_panel_regression(merged_df, use_separate_host_vars=use_sep_host_vars, use_separate_close_vars=use_sep_close_vars, ctrl_vars=ctrl_vars,
				cov_type=cov_type, use_zinb=use_reg_zinb)

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



	except Exception as e:
		# so will also print to log
		print(f"[ERROR]: {e}")
		raise e


