from enum import Enum

import numpy as np
import pandas as pd


DS_GDP_PATH			= 'dataset/worldBankOpenData_GDP_USD.csv'
DS_MEDALS_PATH		= 'dataset/country-medals-by-year.csv'
DS_MEDALS_FULL_PATH	= 'dataset/country-medals-by-year_full.csv'

GDP_YEAR_FIRST			= 1960
GDP_YEAR_LAST			= 2025
MEDALS_FULL_YEAR_FIRST	= 1896
MEDALS_FULL_YEAR_LAST	= 2026



class DsGdpDataType(Enum):
	DEFAULT		= "default"
	# first difference of logarithms (GDP growth rate)
	LN_DIFF		= "ln_diff"


class DsMedalsDataType(Enum):
	DEFAULT		= "default"
	# first difference of logarithms
	LN_DIFF		= "ln_diff"
	# percentage on available medals on that year
	PERCENTAGE	= "percentage"



def get_series_log_diff(series: pd.Series) -> pd.Series:
	"""Helper function to get the log-differenced series.
	@param series: pandas Series values indexed by year
	@return: pandas Series of log-differenced values (growth rates)
	"""
	# Take the natural log of the series
	ln_series = np.log(series)
	# Take the first difference of the log (% growth rate)
	growth_rate = ln_series.diff().dropna()	# type: ignore
	return growth_rate

def get_medal_series_percentage(country_series: pd.Series, full_df: pd.DataFrame) -> pd.Series:
	"""Helper function to get the percentage series.
	@param series: pandas Series values indexed by year
	@return: pandas Series of percentage values (relative to total medals that year)
	"""
	# Calculate the total medals for each year
	total_medals_by_year = full_df.groupby('Year')['Total_Medals'].sum()
	# Calculate the given Country's percentage of medals for each year
	percentage_series = ((country_series / total_medals_by_year) * 100).dropna()
	return percentage_series



def load_gdp_series(
	country_code	: str,
	year_start		: int			= GDP_YEAR_FIRST,
	year_end		: int			= GDP_YEAR_LAST,
	dataset_path	: str			= DS_GDP_PATH,
	data_type		: DsGdpDataType = DsGdpDataType.DEFAULT
) -> tuple[pd.Series, str]:
	"""@param country_code: Mandatory country code to filter by.
	@return: A pandas Series indexed by Year with GDP values and the country name.
	"""

	# Load the dataset
	df = pd.read_csv(dataset_path)
	
	# Filter for specific country
	country_df = df[df['Country Code'] == country_code]
	
	if country_df.empty:
		raise ValueError(f"Country code '{country_code}' not found in dataset")
	
	# Get the first row (should be unique by country code and indicator)
	country_data = country_df.iloc[0]
	
	# Extract year columns (1960-2025) and create a series
	years		= [str(year) for year in range(year_start, year_end + 1)]
	gdp_values	= []
	valid_years	= []
	
	for year in years:
		if year in country_data.index:
			value = country_data[year]
			if pd.notna(value):  # Skip NaN values
				try:
					gdp_values.append(float(value))
					valid_years.append(int(year))
				except (ValueError, TypeError):
					pass
	
	# Create pandas Series with Year as index
	gdp_series = pd.Series(gdp_values, index=valid_years, name='GDP')

	if data_type == DsGdpDataType.LN_DIFF:
		gdp_series = get_series_log_diff(gdp_series)	
	
	return gdp_series, country_data['Country Name']


def load_medals_series(
	country			: str|None			= None,
	year_start		: int				= MEDALS_FULL_YEAR_FIRST,
	year_end		: int				= MEDALS_FULL_YEAR_LAST,
	medals_season	: str				= 'S',
	dataset_path	: str				= DS_MEDALS_FULL_PATH,
	data_type		: DsMedalsDataType	= DsMedalsDataType.DEFAULT
) -> pd.Series:
	"""@param country: Optional country code (NOC) to filter by. If None, aggregates across all countries.
	@param medals_season: Season of medals to include (S for Summer, W for Winter, B for Both).
	@return: A pandas Series indexed by Year with total medals as values.
	"""

	# Load the dataset with specified columns
	df = pd.read_csv(dataset_path, usecols=['Year', 'Season', 'NOC', 'Total_Medals', 'Gold', 'Silver', 'Bronze', 'Men_Medals', 'Women_Medals', 'Is_Host'])

	# Filter by year range
	df = df[(df['Year'] >= year_start) & (df['Year'] <= year_end)]
	
	
	# Filter by medals type
	if medals_season == 'S':
		df = df[df['Season'] == 'Summer']
	elif medals_season == 'W':
		df = df[df['Season'] == 'Winter']
	elif medals_season == 'B':
		df = df[df['Season'].isin(['Summer', 'Winter'])]
	
	if country is None:
		# Aggregate total medals by year (summing across all countries)
		medals_by_year = df.groupby('Year')['Total_Medals'].sum()
	else:
		# Filter for specific country and aggregate by year
		country_df		= df[df['NOC'] == country]
		medals_by_year	= country_df.groupby('Year')['Total_Medals'].sum()
	
	# Convert to pandas Series with Year as index
	medals_series = pd.Series(medals_by_year.values, index=medals_by_year.index, name='Total_Medals')

	if data_type == DsMedalsDataType.LN_DIFF:
		medals_series = get_series_log_diff(medals_series)
	elif data_type == DsMedalsDataType.PERCENTAGE:
		medals_series = get_medal_series_percentage(medals_series, df)

	return medals_series


def merge_series(
	series1			: pd.Series,
	series2			: pd.Series,
	series1_name	: str		= 'Variable1',
	series2_name	: str		= 'Variable2'
) -> pd.DataFrame:
    """Merge two time series (e.g. for Granger causality testing).
    @param series1: First pandas Series indexed by year
    @param series2: Second pandas Series indexed by year
    @param series1_name: Name for the first series column
    @param series2_name: Name for the second series column
    @return: pandas DataFrame with aligned series, NaN values dropped
    """
    # Create a DataFrame from both series
    merged_df = pd.DataFrame({
        series1_name: series1,
        series2_name: series2
    })
    
    # Drop rows with NaN values
    merged_df = merged_df.dropna()
    
    return merged_df