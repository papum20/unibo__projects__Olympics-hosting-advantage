import sys
sys.path.append('src/scripts/')

import argparse
import os
from typing import Literal

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import scipy.stats as stats
import seaborn as sns

# pylint: disable=E0401
from util.load_ds import (
	get_hosts_unique_list,
	get_top_countries_by_medals,
	load_medals_homeDiff,
	DsGdpDataType,
	DsMedalsDataType,
	DsMedalsAggrType,
	DsPopDataType,
	DS_GDP_WBOD_PATH,
	DS_GDPPC_MADDISON_PATH,
	DF_COL_AM_HISTORY,
	DF_COL_EVENTS,
	DF_COL_EVENTS_HOME,
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
	DF_COL_MEDALS_AVAILABLE,
	DF_COL_MEDALS_AVAILABLE_HOME,
	DF_COL_MEDALS_AWAY,
	DF_COL_MEDALS_HOME,
	DF_COL_MEDALS_HOME_DIFF,
	DF_COL_NOC,
	DF_COL_POPULATION,
)
from util.common import Logger, LoggerType

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

P_VALUE_SIGNIFICANCE_LEVEL = 0.05

DF_COL_EVENTS_AWAY		= 'Events_Away'

DF_COL_MEDALS_HOME_EXPECTED	= 'Medals_Home_Expected'
DF_COL_MEDALS_AWAY_EXPECTED	= 'Medals_Away_Expected'
DF_COL_MEDAL_WON			= 'Medal_Won'
DF_COL_MEDAL_NOT_WON		= 'Medal_Not_Won'

DF_COL_CHI_STAT			= 'Chi2_Stat'
DF_COL_CHI_P			= 'Chi2_PValue'
DF_COL_CHI_DOF			= 'Chi2_DOF'
DF_COL_CHI_EXP_FREQ 	= 'Chi2_ExpectedFreq'
DF_COL_P_SIGNIFICANT	= f'P < {P_VALUE_SIGNIFICANCE_LEVEL}'



#
# NORMALITY
#

def plot_normality(medal_diff_df, title_prefix='', show_plots=False):
	# Histogram with KDE: Lets you see if the data forms a "bell curve."
	# Q-Q Plot (Quantile-Quantile): Plots your data against a theoretical normal distribution.
	# If the data is perfectly normal, the points will lie exactly on the straight diagonal red line.

	medal_diff = medal_diff_df[DF_COL_MEDALS_HOME_DIFF]

	# Set up the figure
	fig, ax = plt.subplots(1, 2, figsize=(12, 5))

	# 1. Histogram and Density Plot
	sns.histplot(medal_diff, kde=True, ax=ax[0], color='blue')
	ax[0].set_title('Histogram of Medal Differences')

	# 2. Q-Q Plot
	stats.probplot(medal_diff, dist="norm", plot=ax[1])
	ax[1].set_title('Q-Q Plot')

	plt.tight_layout()
	if show_plots:
		plt.show()



# Shapiro-Wilk Test
def perform_shapiro_wilk_test(medal_diff_df):
	# The Shapiro-Wilk test is generally considered the most powerful test for normality, 
	# especially for small to medium sample sizes (N < 5000).

	medal_diff = medal_diff_df[DF_COL_MEDALS_HOME_DIFF]
	
	stat, p_value = stats.shapiro(medal_diff)

	print(f"Shapiro-Wilk Test Statistic: {stat:.4f}")
	print(f"P-value: {p_value:.4f}")

	# Interpretation
	alpha = 0.05
	if p_value > alpha:
		print("Conclusion: We fail to reject the null hypothesis. The data looks normally distributed.")
	else:
		print("Conclusion: We reject the null hypothesis. The data does NOT look normally distributed.")



# D'Agostino's K-squared Test
def perform_dagostino_k2_test(medal_diff_df):
	# If you have a very large dataset (e.g., analyzing thousands of individual athletes instead of countries), 
	# you might want to use D'Agostino's K-squared test, which looks specifically at skewness and kurtosis:

	medal_diff = medal_diff_df[DF_COL_MEDALS_HOME_DIFF]

	stat, p_value = stats.normaltest(medal_diff)

	if p_value > 0.05:
		print("Data looks normally distributed (Fail to reject H0)")
	else:
		print("Data does not look normally distributed (Reject H0)")



#
# CHI CONTINGENCY TABLE
#

def perform_chiSquared_test(medal_diff_df, is_verbose=False) -> stats.contingency.Chi2ContingencyResult:
	# The chi-squared test of independence is used to determine if there is a significant association between two categorical variables. 
	# In our case, we want to see if there is an association between "competing at home" (Host vs Non-Host) and "winning a medal" (Won Medal vs Did Not Win Medal).

	# 1. Create a Contingency Table
	# Format:	[[Home_Medals, Home_No_Medals], 
	#			[Away_Medals, Away_No_Medals]]
	data = [
		# Home
		[medal_diff_df[DF_COL_MEDALS_HOME].sum(), medal_diff_df[DF_COL_MEDALS_AVAILABLE].sum() - medal_diff_df[DF_COL_MEDALS_HOME].sum()],
		# Away
		[medal_diff_df[DF_COL_MEDALS_AWAY].sum(), medal_diff_df[DF_COL_MEDALS_AVAILABLE].sum() - medal_diff_df[DF_COL_MEDALS_AWAY].sum()]
	]

	# Convert to a pandas DataFrame for nice visualization
	contingency_table_df = pd.DataFrame(
		data, 
		columns=[DF_COL_MEDAL_WON, DF_COL_MEDAL_NOT_WON] 
		#index=['Home (Host)', 'Away (Non-Host)']
	)

	if is_verbose:
		print("\n--- Contingency Table ---")
		print(contingency_table_df)
		print("\n")

	# 2. Perform the Chi-Squared Test of Independence
	res = stats.chi2_contingency(contingency_table_df)
	chi2_stat, p_value, dof, expected_freq = res

	if is_verbose:
		print(f"Chi-Squared Statistic: {chi2_stat:.4f}")
		print(f"P-value: {p_value:.6f}")
		print(f"Degrees of Freedom: {dof}")
		print("Expected Frequencies:")
		print(expected_freq)

	# Interpretation
	alpha = 0.05
	if is_verbose:
		if p_value < alpha:	# type: ignore
			print("\nConclusion: Reject the null hypothesis.")
			print("There is a statistically significant relationship between competing at home and winning a medal (Home Advantage confirmed!).")
		else:
			print("\nConclusion: Fail to reject the null hypothesis.")
			print("There is no significant difference in medal-winning rates between home and away games.")

	return res


# observed vs expected:
# compare, for the hosted editions, medals won from the host vs Rest Of the World
def perform_chiSquared_goodnessOfFit_ROW(medal_diff_df, is_verbose=False) -> tuple[float, float]:
	# The chi-squared goodness of fit test is used to determine if a sample data matches a population with a specific distribution. 
	# In our case, we want to see if the observed medal counts for the host country differ significantly from what we would expect based on historical averages.

	# Suppose in the host year there were 1000 total medals awarded.
	# Based on historical average, the host country usually wins 4% (Expected = 40 medals).
	# However, during their host year, they actually won 60 medals (Observed = 60).
	# The rest of the world won the remaining medals.

	won_tot		= medal_diff_df[DF_COL_MEDALS_HOME].sum() + medal_diff_df[DF_COL_MEDALS_AWAY].sum()
	host_rate	= medal_diff_df[DF_COL_EVENTS_HOME].sum() / medal_diff_df[DF_COL_EVENTS].sum()

	# [Host Country Medals, Rest of the World Medals]
	observed = [
		medal_diff_df[DF_COL_MEDALS_HOME].sum(),
		medal_diff_df[DF_COL_MEDALS_AVAILABLE_HOME].sum() - medal_diff_df[DF_COL_MEDALS_HOME].sum()
	]
	expected = [
		host_rate * won_tot,
		medal_diff_df[DF_COL_MEDALS_AVAILABLE_HOME].sum() - host_rate * won_tot
	]

	if is_verbose:
		print("\n--- Observed vs Expected ---")
		print(f"Observed (Home, Away): {observed}")
		print(f"Expected (Home, Away): {expected}")
		print("\n")
		
	# Perform Chi-Squared Goodness of Fit test
	chi2_stat, p_value = stats.chisquare(f_obs=observed, f_exp=expected)

	print(f"Chi-Squared Statistic: {chi2_stat:.4f}")
	print(f"P-value: {p_value:.6f}")

	if is_verbose:
		if p_value < 0.05:
			print("\nConclusion: Reject the null hypothesis.")
			print("The country won a significantly different amount of medals than expected (Home Advantage confirmed).")
		else:
			print("\nConclusion: Fail to reject the null hypothesis.")
			print("The medal count is in line with historical expectations.")

	return chi2_stat, p_value


# observed vs expected:
# compare, for a country, medals won hosting vs away
def perform_chiSquared_goodnessOfFit_own(medal_diff_df, is_verbose=False) -> tuple[float, float]:
	won_tot		= medal_diff_df[DF_COL_MEDALS_HOME].sum() + medal_diff_df[DF_COL_MEDALS_AWAY].sum()

	# [Won Home, Won Away]
	observed = [
		medal_diff_df[DF_COL_MEDALS_HOME].sum(),
		medal_diff_df[DF_COL_MEDALS_AWAY].sum()
	]
	expected = [
		won_tot / medal_diff_df[DF_COL_EVENTS].sum() * medal_diff_df[DF_COL_EVENTS_HOME].sum(),
		won_tot / medal_diff_df[DF_COL_EVENTS].sum() * (medal_diff_df[DF_COL_EVENTS].sum() - medal_diff_df[DF_COL_EVENTS_HOME].sum())
	]

	if is_verbose:
		print("\n--- Observed vs Expected ---")
		print(f"Observed (Home, Away): {observed}")
		print(f"Expected (Home, Away): {expected}")
		print("\n")

	# Perform Chi-Squared Goodness of Fit test
	chi2_stat, p_value = stats.chisquare(f_obs=observed, f_exp=expected)

	print(f"Chi-Squared Statistic: {chi2_stat:.4f}")
	print(f"P-value: {p_value:.6f}")

	if is_verbose:
		if p_value < 0.05:
			print("\nConclusion: Reject the null hypothesis.")
			print("The country won a significantly different amount of medals than expected (Home Advantage confirmed).")
		else:
			print("\nConclusion: Fail to reject the null hypothesis.")
			print("The medal count is in line with historical expectations.")

	return chi2_stat, p_value



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
			help='Country code(s) (NOC) - space-separated list (noc-top and noc-hosts have priority) - default: all countries (no filter)'
		)
		
		parser.add_argument(
			'--noc-top',
			type=int,
			default=0,
			help='Use the top n countries (noc-hosts has priority) - default: 0 (all)'
		)

		parser.add_argument(
			'--noc-hosts',
			action='store_true',
			help='Use the all and only countries hosting in the selected years (priority over other noc options) (flag, no value needed)'
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
			'--exclude-boycott',
			action='store_true',
			help='Exclude boycott years from the analysis (flag, no value needed)'
		)

		parser.add_argument(
			'--pre-host',
			action='store_true',
			help='Consider only years up until the country\'s first time hosting (inclusive) (flag, no value needed)'
		)
		parser.add_argument(
			'--post-host',
			action='store_true',
			help='Consider only years from the country\'s last time hosting (pre-host has priority) (inclusive) (flag, no value needed)'
		)

		parser.add_argument(
			'--min-events',
			type=int,
			default=0,
			help='Minimum number of events for a country to be included - default: 0 (no filter)'
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
			'--save',
			action='store_true',
			help='Save plots to file (flag, no value needed)'
		)

		parser.add_argument(
			'--show',
			action='store_true',
			help='Show plotss (flag, no value needed)'
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
		noc_hosts			= args.noc_hosts
		medals_season		= args.season
		save_plot_flag		= args.save
		year_start			= args.start_year
		year_end			= args.end_year
		min_events			= args.min_events
		
		exclude_boycott		= args.exclude_boycott
		use_pre_host		= args.pre_host
		use_from_last_host	= args.post_host
		use_gdp_mean		= args.gdp_avg
		use_gdp_tot			= args.gdp_tot
		use_population_mean	= args.pop_avg

		gdp_type = DsGdpDataType.LN_DIFF if args.gdp_logdiff else DsGdpDataType.LN if args.gdp_log else DsGdpDataType.DEFAULT
		pop_type = DsPopDataType.LN_DIFF if args.pop_logdiff else DsPopDataType.LN if args.pop_log else DsPopDataType.DEFAULT
		medals_data_type = DsMedalsDataType.LN_DIFF if args.med_logdiff else DsMedalsDataType.PERCENTAGE if args.med_perc else DsMedalsDataType.DEFAULT

		log_output			= args.log
		show_plots			= args.show
		verbose				= args.verbose

		DS_GDP_PATH = DS_GDP_WBOD_PATH if use_gdp_tot else DS_GDPPC_MADDISON_PATH

		if noc_hosts:
			noc_list = get_hosts_unique_list(medals_season=medals_season, year_start=year_start, year_end=year_end, remove_boycott=exclude_boycott)
			noc_top = 0
			print(f"Using all host countries in the selected years (total hosts: {len(noc_list)}):\n{', '.join(noc_list)}\n")
		elif noc_top != 0:
			noc_list = get_top_countries_by_medals(year_start=year_start, year_end=year_end, n=noc_top,
										medals_season=medals_season, is_verbose=verbose)
			print(f"No specific NOCs provided. Using top {noc_top} NOCs by total medals: {noc_list}")


		if log_output:
			sys.stdout = Logger(
				logger_type=LoggerType.CHI_SQUARED,
				noc=noc_top if noc_top != 0 else noc_list,
				year_start=year_start,
				year_end=year_end,
				lag_min=0,
				lag_max=0,
				gdp_type=gdp_type.name,
				pop_type=pop_type.name,
				use_gpd_avg=use_gdp_mean,
				use_pop_avg=use_population_mean
			)

		print(f"Running with args: {args}")



		res_chi_squared = pd.DataFrame(columns=[
			DF_COL_NOC,
			DF_COL_EVENTS_HOME,
			DF_COL_EVENTS_AWAY,
			DF_COL_MEDALS,
			DF_COL_MEDALS_HOME,
			DF_COL_MEDALS_HOME_EXPECTED,
			DF_COL_MEDALS_AWAY,
			DF_COL_MEDALS_AWAY_EXPECTED,
			DF_COL_CHI_STAT,
			DF_COL_CHI_P,
			DF_COL_P_SIGNIFICANT,
			DF_COL_CHI_DOF,
			DF_COL_CHI_EXP_FREQ
		])

		res_chi_squared_goodnessOfFit_own = pd.DataFrame(columns=[
			DF_COL_NOC,
			DF_COL_EVENTS_HOME,
			DF_COL_EVENTS_AWAY,
			DF_COL_MEDALS,
			DF_COL_MEDALS_HOME,
			DF_COL_MEDALS_HOME_EXPECTED,
			DF_COL_MEDALS_AWAY,
			DF_COL_MEDALS_AWAY_EXPECTED,
			DF_COL_CHI_STAT,
			DF_COL_CHI_P,
			DF_COL_P_SIGNIFICANT
		])

		res_chi_squared_goodnessOfFit_ROW = pd.DataFrame(columns=[
			DF_COL_NOC,
			DF_COL_EVENTS_HOME,
			DF_COL_EVENTS_AWAY,
			DF_COL_MEDALS,
			DF_COL_MEDALS_HOME,
			DF_COL_MEDALS_HOME_EXPECTED,
			DF_COL_MEDALS_AWAY,
			DF_COL_MEDALS_AWAY_EXPECTED,
			DF_COL_CHI_STAT,
			DF_COL_CHI_P,
			DF_COL_P_SIGNIFICANT
		])

		# Aggregated

		medal_diff_df, country_name = load_medals_homeDiff(
				countries_list			= noc_list,
				medals_season			= medals_season,
				year_start				= year_start,
				year_end				= year_end,
				min_events_n			= min_events,
				remove_boycott			= exclude_boycott,
				until_first_host		= use_pre_host,
				from_last_host			= use_from_last_host,
				medals_data_type		= medals_data_type,
				medals_aggr_type		= DsMedalsAggrType.SUM,
				is_verbose				= verbose
			)

		if verbose:
			print(medal_diff_df.to_string())
		
		plot_normality(medal_diff_df, title_prefix=f"{country_name} - " if country_name else '', show_plots=show_plots)
		perform_shapiro_wilk_test(medal_diff_df)
		perform_dagostino_k2_test(medal_diff_df)

		res = perform_chiSquared_test(medal_diff_df, is_verbose=verbose)

		res_chi_squared = pd.concat([res_chi_squared, pd.DataFrame([{
				DF_COL_NOC: 'ALL',
				DF_COL_EVENTS_HOME: medal_diff_df[DF_COL_EVENTS_HOME].sum(),
				DF_COL_EVENTS_AWAY: medal_diff_df[DF_COL_EVENTS].sum() - medal_diff_df[DF_COL_EVENTS_HOME].sum(),
				DF_COL_MEDALS: medal_diff_df[DF_COL_MEDALS_HOME].sum() + medal_diff_df[DF_COL_MEDALS_AWAY].sum(),
				DF_COL_MEDALS_HOME: medal_diff_df[DF_COL_MEDALS_HOME].sum(),
				DF_COL_MEDALS_HOME_EXPECTED: res[3][0, 0],	# type: ignore
				DF_COL_MEDALS_AWAY: medal_diff_df[DF_COL_MEDALS_AWAY].sum(),
				DF_COL_MEDALS_AWAY_EXPECTED: res[3][1, 0],	# type: ignore
				DF_COL_CHI_STAT: res[0],
				DF_COL_CHI_P: round(res[1], 4),	# type: ignore
				DF_COL_P_SIGNIFICANT: res[1] < P_VALUE_SIGNIFICANCE_LEVEL,	# type: ignore
				DF_COL_CHI_DOF: res[2],
				DF_COL_CHI_EXP_FREQ: res[3]
			}])
		])
		
		stat, pval			= perform_chiSquared_goodnessOfFit_own(medal_diff_df, is_verbose=verbose)
		won_tot				= medal_diff_df[DF_COL_MEDALS_HOME].sum() + medal_diff_df[DF_COL_MEDALS_AWAY].sum()
		expected_home_own	= won_tot / medal_diff_df[DF_COL_EVENTS].sum() * medal_diff_df[DF_COL_EVENTS_HOME].sum()
		expected_away_own	= won_tot / medal_diff_df[DF_COL_EVENTS].sum() * (medal_diff_df[DF_COL_EVENTS].sum() - medal_diff_df[DF_COL_EVENTS_HOME].sum())

		res_chi_squared_goodnessOfFit_own = pd.concat([res_chi_squared_goodnessOfFit_own, pd.DataFrame([{
				DF_COL_NOC: 'ALL',
				DF_COL_EVENTS_HOME: medal_diff_df[DF_COL_EVENTS_HOME].sum(),
				DF_COL_EVENTS_AWAY: medal_diff_df[DF_COL_EVENTS].sum() - medal_diff_df[DF_COL_EVENTS_HOME].sum(),
				DF_COL_MEDALS: won_tot,
				DF_COL_MEDALS_HOME: medal_diff_df[DF_COL_MEDALS_HOME].sum(),
				DF_COL_MEDALS_HOME_EXPECTED: expected_home_own,
				DF_COL_MEDALS_AWAY: medal_diff_df[DF_COL_MEDALS_AWAY].sum(),
				DF_COL_MEDALS_AWAY_EXPECTED: expected_away_own,
				DF_COL_CHI_STAT: stat,
				DF_COL_CHI_P: round(pval, 4),
				DF_COL_P_SIGNIFICANT: pval < P_VALUE_SIGNIFICANCE_LEVEL	# type: ignore
			}])
		])

		stat, pval = perform_chiSquared_goodnessOfFit_ROW(medal_diff_df, is_verbose=verbose)
		won_tot = medal_diff_df[DF_COL_MEDALS_HOME].sum() + medal_diff_df[DF_COL_MEDALS_AWAY].sum()
		host_rate = medal_diff_df[DF_COL_EVENTS_HOME].sum() / medal_diff_df[DF_COL_EVENTS].sum()
		expected_home_row = host_rate * won_tot
		expected_away_row = won_tot - expected_home_row

		res_chi_squared_goodnessOfFit_ROW = pd.concat([res_chi_squared_goodnessOfFit_ROW, pd.DataFrame([{
				DF_COL_NOC: 'ALL',
				DF_COL_EVENTS_HOME: medal_diff_df[DF_COL_EVENTS_HOME].sum(),
				DF_COL_EVENTS_AWAY: medal_diff_df[DF_COL_EVENTS].sum() - medal_diff_df[DF_COL_EVENTS_HOME].sum(),
				DF_COL_MEDALS: won_tot,
				DF_COL_MEDALS_HOME: medal_diff_df[DF_COL_MEDALS_HOME].sum(),
				DF_COL_MEDALS_HOME_EXPECTED: expected_home_row,
				DF_COL_MEDALS_AWAY: medal_diff_df[DF_COL_MEDALS_AWAY].sum(),
				DF_COL_MEDALS_AWAY_EXPECTED: expected_away_row,
				DF_COL_CHI_STAT: stat,
				DF_COL_CHI_P: round(pval, 4),
				DF_COL_P_SIGNIFICANT: pval < P_VALUE_SIGNIFICANCE_LEVEL	# type: ignore
			}])
		])



		# by NOC

		for noc in noc_list:

			if verbose:
				print(f"\n\n=== Analyzing NOC: {noc} ===")
				
			medal_diff_df, country_name = load_medals_homeDiff(
					countries_list			= [noc],
					medals_season			= medals_season,
					year_start				= year_start,
					year_end				= year_end,
					min_events_n			= min_events,
					remove_boycott			= exclude_boycott,
					until_first_host		= use_pre_host,
					from_last_host			= use_from_last_host,
					medals_data_type		= medals_data_type,
					medals_aggr_type		= DsMedalsAggrType.SUM,
					is_verbose				= verbose
				)
			
			if medal_diff_df.empty:
				if verbose:
					print(f"No data available for NOC {noc} after applying filters. Skipping.")
				continue
			
			res = perform_chiSquared_test(medal_diff_df, is_verbose=verbose)

			res_chi_squared = pd.concat([res_chi_squared, pd.DataFrame([{
					DF_COL_NOC: noc,
					DF_COL_EVENTS_HOME: medal_diff_df[DF_COL_EVENTS_HOME].sum(),
					DF_COL_EVENTS_AWAY: medal_diff_df[DF_COL_EVENTS].sum() - medal_diff_df[DF_COL_EVENTS_HOME].sum(),
					DF_COL_MEDALS: medal_diff_df[DF_COL_MEDALS_HOME].sum() + medal_diff_df[DF_COL_MEDALS_AWAY].sum(),
					DF_COL_MEDALS_HOME: medal_diff_df[DF_COL_MEDALS_HOME].sum(),
					DF_COL_MEDALS_HOME_EXPECTED: res[3][0, 0],	# type: ignore
					DF_COL_MEDALS_AWAY: medal_diff_df[DF_COL_MEDALS_AWAY].sum(),
					DF_COL_MEDALS_AWAY_EXPECTED: res[3][1, 0],	# type: ignore
					DF_COL_CHI_STAT: res[0],
					DF_COL_CHI_P: round(res[1], 4),	# type: ignore
					DF_COL_P_SIGNIFICANT: res[1] < P_VALUE_SIGNIFICANCE_LEVEL,	# type: ignore
					DF_COL_CHI_DOF: res[2],
					DF_COL_CHI_EXP_FREQ: res[3]
				}])
			])

			stat, pval = perform_chiSquared_goodnessOfFit_own(medal_diff_df, is_verbose=verbose)
			won_tot = medal_diff_df[DF_COL_MEDALS_HOME].sum() + medal_diff_df[DF_COL_MEDALS_AWAY].sum()
			expected_home_own = won_tot / medal_diff_df[DF_COL_EVENTS].sum() * medal_diff_df[DF_COL_EVENTS_HOME].sum()
			expected_away_own = won_tot / medal_diff_df[DF_COL_EVENTS].sum() * (medal_diff_df[DF_COL_EVENTS].sum() - medal_diff_df[DF_COL_EVENTS_HOME].sum())

			res_chi_squared_goodnessOfFit_own = pd.concat([res_chi_squared_goodnessOfFit_own, pd.DataFrame([{
					DF_COL_NOC: noc,
					DF_COL_EVENTS_HOME: medal_diff_df[DF_COL_EVENTS_HOME].sum(),
					DF_COL_EVENTS_AWAY: medal_diff_df[DF_COL_EVENTS].sum() - medal_diff_df[DF_COL_EVENTS_HOME].sum(),
					DF_COL_MEDALS: won_tot,
					DF_COL_MEDALS_HOME: medal_diff_df[DF_COL_MEDALS_HOME].sum(),
					DF_COL_MEDALS_HOME_EXPECTED: expected_home_own,
					DF_COL_MEDALS_AWAY: medal_diff_df[DF_COL_MEDALS_AWAY].sum(),
					DF_COL_MEDALS_AWAY_EXPECTED: expected_away_own,
					DF_COL_CHI_STAT: stat,
					DF_COL_CHI_P: round(pval, 4),
					DF_COL_P_SIGNIFICANT: pval < P_VALUE_SIGNIFICANCE_LEVEL	# type: ignore
				}])
			])
			
			stat, pval = perform_chiSquared_goodnessOfFit_ROW(medal_diff_df, is_verbose=verbose)
			won_tot = medal_diff_df[DF_COL_MEDALS_HOME].sum() + medal_diff_df[DF_COL_MEDALS_AWAY].sum()
			host_rate = medal_diff_df[DF_COL_EVENTS_HOME].sum() / medal_diff_df[DF_COL_EVENTS].sum()
			expected_home_row = host_rate * won_tot
			expected_away_row = won_tot - expected_home_row

			res_chi_squared_goodnessOfFit_ROW = pd.concat([res_chi_squared_goodnessOfFit_ROW, pd.DataFrame([{
					DF_COL_NOC: noc,
					DF_COL_EVENTS_HOME: medal_diff_df[DF_COL_EVENTS_HOME].sum(),
					DF_COL_EVENTS_AWAY: medal_diff_df[DF_COL_EVENTS].sum() - medal_diff_df[DF_COL_EVENTS_HOME].sum(),
					DF_COL_MEDALS: won_tot,
					DF_COL_MEDALS_HOME: medal_diff_df[DF_COL_MEDALS_HOME].sum(),
					DF_COL_MEDALS_HOME_EXPECTED: expected_home_row,
					DF_COL_MEDALS_AWAY: medal_diff_df[DF_COL_MEDALS_AWAY].sum(),
					DF_COL_MEDALS_AWAY_EXPECTED: expected_away_row,
					DF_COL_CHI_STAT: stat,
					DF_COL_CHI_P: round(pval, 4),
					DF_COL_P_SIGNIFICANT: pval < P_VALUE_SIGNIFICANCE_LEVEL	# type: ignore
				}])
			])

		res_chi_squared						= res_chi_squared.sort_values(by=[DF_COL_CHI_P, DF_COL_NOC], na_position='last').reset_index(drop=True)
		res_chi_squared_goodnessOfFit_own	= res_chi_squared_goodnessOfFit_own.sort_values(by=[DF_COL_CHI_P, DF_COL_NOC], na_position='last').reset_index(drop=True)
		res_chi_squared_goodnessOfFit_ROW	= res_chi_squared_goodnessOfFit_ROW.sort_values(by=[DF_COL_CHI_P, DF_COL_NOC], na_position='last').reset_index(drop=True)

		print("\n\n=== Final Results: Chi-Squared Test of Independence ===")
		print(res_chi_squared.to_string(float_format=lambda x: f'{x:.4f}'))

		print("\n\n=== Final Results: Chi-Squared Goodness of Fit (Own vs Expected) ===")
		print(res_chi_squared_goodnessOfFit_own.to_string(float_format=lambda x: f'{x:.4f}'))

		print("\n\n=== Final Results: Chi-Squared Goodness of Fit (Host vs Rest of the World) ===")
		print(res_chi_squared_goodnessOfFit_ROW.to_string(float_format=lambda x: f'{x:.4f}'))
		
	except Exception as e:
		# so will also print to log
		print(f"[ERROR]: {e}")
		raise e

