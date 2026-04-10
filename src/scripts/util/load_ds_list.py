from enum import Enum

import numpy as np
import pandas as pd


# World Bank Open Data
DS_GDP_WBOD_PATH			= 'dataset/worldBankOpenData_GDP_USD.csv'
DS_GDPPC_PERC_WBOD_PATH		= 'dataset/worldBankOpenData_GDPpc_perc.csv'
# Maddison Project Database
DS_GDPPC_MADDISON_PATH		= 'dataset/maddisonProjectDatabase_GDPpc_2023.csv'
DS_MEDALS_PATH				= 'dataset/country-medals-by-year.csv'
DS_MEDALS_FULL_PATH			= 'dataset/country-medals-by-year_full.csv'
DS_POPULATION_WBOD_PATH		= 'dataset/worldBankOpenData_population.csv'
DS_POPULATION_MADDISON_PATH	= 'dataset/maddisonProjectDatabase_population_2023.csv'

GDP_WBOD_YEAR_FIRST				= 1960
GDP_WBOD_YEAR_LAST				= 2025
GDPPC_PERC_WBOD_YEAR_LAST		= 2024
GDP_MADDISON_YEAR_START_DFLT	= 1800
GDP_MADDISON_YEAR_END_DFLT		= 2025
GDP_MADDISON_YEAR_LAST			= 2022
MEDALS_FULL_YEAR_FIRST			= 1896
MEDALS_FULL_YEAR_LAST			= 2026
POPULATION_WBOD_YEAR_LAST		= 2024
POPULATION_MADDISON_YEAR_LAST	= 2022

YEAR_BOYCOTT_URS	= 1980	# hosted by URS, boycotted by USA bloc
YEAR_BOYCOTT_USA	= 1984

# Columns names in returned DataFrames
DF_COL_GDP			= 'GDP'
DF_COL_IS_BOYCOTT	= 'Is_Boycott'
DF_COL_IS_COMMUNIST	= 'Is_Communist'
DF_COL_IS_HOST		= 'Is_Host'
DF_COL_MEDALS		= 'Medals'
DF_COL_POPULATION	= 'Population'

COMMUNIST_BLOC_COUNTRIES = {
	'ALB', 'BGD', 'BLR', 'BGR', 'CHN', 'CUB', 'CSK', 'DDR', 'EST', 'HUN', 'KAZ',
	'KGZ', 'LAO', 'LVA', 'LTU', 'MDA', 'MNG', 'PRK', 'ROU', 'RUS', 'TJK', 'TKM',
	'UKR', 'UZB', 'YUG'
}



class DsGdpDataType(Enum):
	DEFAULT		= "default"
	# first difference of logarithms (GDP growth rate)
	LN_DIFF		= "ln_diff"


class DsPopDataType(Enum):
	DEFAULT		= "default"
	# first difference of logarithms (growth rate)
	LN_DIFF		= "ln_diff"


class DsMedalsDataType(Enum):
	DEFAULT		= "default"
	# first difference of logarithms
	LN_DIFF		= "ln_diff"
	# percentage on available medals on that year
	PERCENTAGE	= "percentage"



#
# Utilities
#


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



#
# GDP
#


def load_gdppc_maddison_series(
	country_code	: str | list[str],
	year_start		: int			= GDP_MADDISON_YEAR_START_DFLT,
	year_end		: int			= GDP_MADDISON_YEAR_END_DFLT,
	dataset_path	: str			= DS_GDPPC_MADDISON_PATH,
	data_type		: DsGdpDataType = DsGdpDataType.DEFAULT
) -> tuple[pd.Series, str]:
	"""Load GDP per capita from Maddison Project Database.
	@param country_code: Mandatory country code(s) (3-letter) to filter by. Can be a single string or list of strings.
	@param year_start: Starting year for the data
	@param year_end: Ending year for the data
	@param dataset_path: Path to the Maddison CSV file
	@param data_type: Type of transformation to apply (DEFAULT or LN_DIFF)
	@return: A pandas Series indexed by Year with GDP per capita values and the country name.
	"""
	
	# Convert single string to list
	if isinstance(country_code, str):
		country_code = [country_code]
	
	# Load the dataset, skipping the first 2 rows (metadata/regions)
	# Row 3 (index 2) contains the actual column names (year, country codes, etc)
	df = pd.read_csv(dataset_path, skiprows=2)
	
	# The first column is 'year' (or similar), and subsequent columns are country codes
	# Rename the first column to 'Year' if it's not already
	if 'year' in df.columns[0].lower():
		df = df.rename(columns={df.columns[0]: 'Year'})
	
	# Validate country codes
	for code in country_code:
		if code not in df.columns:
			raise ValueError(f"Country code '{code}' not found in dataset. Available countries: {', '.join(df.columns[1:])}")
	
	# Extract year and country data
	gdppc_data = df[['Year'] + country_code].copy()
	gdppc_data['Year'] = pd.to_numeric(gdppc_data['Year'], errors='coerce')
	for code in country_code:
		gdppc_data[code] = pd.to_numeric(gdppc_data[code], errors='coerce')
	
	# Remove rows with NaN values
	gdppc_data = gdppc_data.dropna()
	
	# Filter by year range
	gdppc_data = gdppc_data[(gdppc_data['Year'] >= year_start) & (gdppc_data['Year'] <= year_end)]
	
	# Aggregate countries if multiple provided
	if len(country_code) > 1:
		gdppc_values = gdppc_data[country_code].mean(axis=1)
		country_name = '+'.join(country_code)
	else:
		gdppc_values = gdppc_data[country_code[0]]
		country_name = country_code[0]
	
	# Create Series with Year as index
	gdppc_series = pd.Series(
		gdppc_values.values,
		index=gdppc_data['Year'].astype(int).values,
		name='GDP_per_capita'
	)
	
	if data_type == DsGdpDataType.LN_DIFF:
		gdppc_series = get_series_log_diff(gdppc_series)
	
	return gdppc_series, country_name


def load_gdppc_extended_series(
	country_code	: str | list[str],
	year_start		: int			= GDP_MADDISON_YEAR_START_DFLT,
	year_end		: int			= GDPPC_PERC_WBOD_YEAR_LAST,
	dataset_path	: str			= DS_GDPPC_PERC_WBOD_PATH,
	data_type		: DsGdpDataType = DsGdpDataType.DEFAULT
) -> tuple[pd.Series, str]:
	"""Load GDP per capita from Maddison (until 2022) and extend with WBOD percentage changes (2023-2024).
	@param country_code: Mandatory country code(s) (3-letter) to filter by. Can be a single string or list of strings.
	@param year_start: Starting year for the data
	@param year_end: Ending year for the data (up to 2024)
	@param dataset_path: Path to the WBOD percentage changes CSV file
	@param data_type: Type of transformation to apply (DEFAULT or LN_DIFF)
	@return: A pandas Series indexed by Year with GDP per capita values and the country name.
	"""
	
	# Convert single string to list
	if isinstance(country_code, str):
		country_code = [country_code]
	
	# Load Maddison data (1800-2022)
	gdppc_series, country_name = load_gdppc_maddison_series(
		country_code=country_code,
		year_start=year_start,
		year_end=GDP_MADDISON_YEAR_LAST,
		data_type=DsGdpDataType.DEFAULT  # Don't apply transformation yet
	)
	
	# If year_end <= 2022, just return the Maddison data
	if year_end <= GDP_MADDISON_YEAR_LAST:
		if data_type == DsGdpDataType.LN_DIFF:
			gdppc_series = get_series_log_diff(gdppc_series)
		return gdppc_series, country_name
	
	# Load percentage changes from WBOD for years 2023-2024
	df_perc = pd.read_csv(dataset_path)
	
	# Filter for specific countries
	country_df = df_perc[df_perc['Country Code'].isin(country_code)]
	
	if country_df.empty:
		# If no percentage data available, just return Maddison data
		if data_type == DsGdpDataType.LN_DIFF:
			gdppc_series = get_series_log_diff(gdppc_series)
		return gdppc_series, country_name
	
	# Aggregate percentage changes across countries (average)
	country_perc_avg = country_df.set_index('Country Code').mean()
	last_gdppc_value = gdppc_series.iloc[-1]  # Last value from Maddison (2022)
	
	# Extend with percentage changes
	extended_values = dict(gdppc_series)  # Convert to dict
	current_value = last_gdppc_value
	
	for year in range(GDP_MADDISON_YEAR_LAST + 1, year_end + 1):
		year_str = str(year)
		perc_changes = []
		for _, row in country_df.iterrows():
			if year_str in row.index:
				perc_change = row[year_str]
				if pd.notna(perc_change):
					try:
						perc_changes.append(float(perc_change))
					except (ValueError, TypeError):
						pass
		
		if perc_changes:
			avg_perc_change = np.mean(perc_changes) / 100.0
			current_value = current_value * (1 + avg_perc_change)
			extended_values[year] = current_value
	
	# Create extended Series
	gdppc_series = pd.Series(extended_values, name='GDP_per_capita')
	gdppc_series = gdppc_series.sort_index()
	
	if data_type == DsGdpDataType.LN_DIFF:
		gdppc_series = get_series_log_diff(gdppc_series)
	
	return gdppc_series, country_name


def load_gdp_wbod_series(
	country_code	: str | list[str],
	year_start		: int			= GDP_WBOD_YEAR_FIRST,
	year_end		: int			= GDP_WBOD_YEAR_LAST,
	dataset_path	: str			= DS_GDP_WBOD_PATH,
	data_type		: DsGdpDataType = DsGdpDataType.DEFAULT
) -> tuple[pd.Series, str]:
	"""@param country_code: Mandatory country code(s) to filter by. Can be a single string or list of strings.
	@return: A pandas Series indexed by Year with GDP values and the country name.
	"""

	# Convert single string to list
	if isinstance(country_code, str):
		country_code = [country_code]
	
	# Load the dataset
	df = pd.read_csv(dataset_path)
	
	# Filter for specific countries
	country_df = df[df['Country Code'].isin(country_code)]
	
	if country_df.empty:
		raise ValueError(f"Country code(s) {country_code} not found in dataset")
	
	# Extract year columns (1960-2025) and create a series
	years		= [str(year) for year in range(year_start, year_end + 1)]
	gdp_values	= []
	valid_years	= []
	
	for year in years:
		year_values = []
		for _, row in country_df.iterrows():
			if year in row.index:
				value = row[year]
				if pd.notna(value):
					try:
						year_values.append(float(value))
					except (ValueError, TypeError):
						pass
		if year_values:
			gdp_values.append(np.mean(year_values))
			valid_years.append(int(year))
	
	# Create pandas Series with Year as index
	gdp_series = pd.Series(gdp_values, index=valid_years, name='GDP')
	country_name = '+'.join(country_code) if len(country_code) > 1 else country_df.iloc[0].get('Country Name', country_code[0])

	if data_type == DsGdpDataType.LN_DIFF:
		gdp_series = get_series_log_diff(gdp_series)	
	
	return gdp_series, country_name


def load_gdp_series(
	country_code	: str | list[str],
	year_start		: int			= GDP_MADDISON_YEAR_START_DFLT,
	year_end		: int			= GDP_MADDISON_YEAR_END_DFLT,
	dataset_path	: str			= DS_GDPPC_MADDISON_PATH,
	data_type		: DsGdpDataType = DsGdpDataType.DEFAULT
) -> tuple[pd.Series, str]:
	"""
	@param country_code: Mandatory country code(s) to filter by. Can be a single string or list of strings.
	@param year_start: Starting year for the data
	@param year_end: Ending year for the data
	@param dataset_path: Path to the dataset CSV file. One of the two datasets (World Bank Open Data or Maddison Project Database) can be used, depending on the file path provided.
	@param data_type: Type of transformation to apply (DEFAULT or LN_DIFF)
	@return: A pandas Series indexed by Year with GDP values and the country name.
	"""

	if dataset_path == DS_GDP_WBOD_PATH:
		return load_gdp_wbod_series(country_code, year_start, year_end, dataset_path, data_type)
	elif dataset_path == DS_GDPPC_MADDISON_PATH:
		# Use extended version that includes WBOD data for 2023-2024
		if year_end > GDP_MADDISON_YEAR_LAST:
			return load_gdppc_extended_series(country_code, year_start, year_end, data_type=data_type)
		else:
			return load_gdppc_maddison_series(country_code, year_start, year_end, dataset_path, data_type)

	else:
		raise ValueError(f"Unsupported dataset path: {dataset_path}")



#
# Medals
#


def load_medals(
	country			: str | list[str] | None = None,
	year_start		: int				= MEDALS_FULL_YEAR_FIRST,
	year_end		: int				= MEDALS_FULL_YEAR_LAST,
	medals_season	: str				= 'S',
	dataset_path	: str				= DS_MEDALS_FULL_PATH,
	data_type		: DsMedalsDataType	= DsMedalsDataType.DEFAULT
) -> pd.DataFrame:
	"""Load medals data with Is_Host and Is_Boycott columns.
	@param country: Optional country code(s) (NOC) to filter by. Can be a single string, list of strings, or None.
	@param medals_season: Season of medals to include (S for Summer, W for Winter, B for Both).
	@param data_type: Type of transformation to apply to the medals series (DEFAULT, LN_DIFF, PERCENTAGE)
	@return: DataFrame indexed by Year with Total_Medals, Is_Host, and Is_Boycott columns.
	"""
	
	# Load the dataset
	df = pd.read_csv(dataset_path, usecols=['Year', 'Season', 'NOC', 'Total_Medals', 'Is_Host'])
	
	# Filter by year range
	medals_df = df[(df['Year'] >= year_start) & (df['Year'] <= year_end)]
	
	# Filter by medals season
	if medals_season == 'S':
		medals_df = medals_df[medals_df['Season'] == 'Summer']
	elif medals_season == 'W':
		medals_df = medals_df[medals_df['Season'] == 'Winter']
	elif medals_season == 'B':
		medals_df = medals_df[medals_df['Season'].isin(['Summer', 'Winter'])]
	
	# Filter for specific country/countries if provided
	if country:
		if isinstance(country, str):
			medals_df = medals_df[medals_df['NOC'] == country]
		else:
			medals_df = medals_df[medals_df['NOC'].isin(country)]
	
	# Group by year and aggregate
	medals_df = medals_df.groupby('Year').agg({
		'Total_Medals'	: 'sum',
		'Is_Host'		: 'any'  # True if any entry for that year is a host
	}).reset_index()
	
	# Add Is_Boycott column
	medals_df['Is_Boycott'] = medals_df['Year'].isin([YEAR_BOYCOTT_URS, YEAR_BOYCOTT_USA])
	
	# Set Year as index
	medals_df = medals_df.set_index('Year')

	if data_type == DsMedalsDataType.LN_DIFF:
		medals_df['Total_Medals'] = get_series_log_diff(medals_df['Total_Medals'])
	elif data_type == DsMedalsDataType.PERCENTAGE:
		medals_df['Total_Medals'] = get_medal_series_percentage(medals_df['Total_Medals'], df)
	
	return medals_df


def load_medals_series(
	country			: str | list[str] | None = None,
	year_start		: int				= MEDALS_FULL_YEAR_FIRST,
	year_end		: int				= MEDALS_FULL_YEAR_LAST,
	medals_season	: str				= 'S',
	dataset_path	: str				= DS_MEDALS_FULL_PATH,
	data_type		: DsMedalsDataType	= DsMedalsDataType.DEFAULT
) -> pd.Series:
	"""@param country: Optional country code(s) (NOC) to filter by. Can be a single string, list of strings, or None. If None, aggregates across all countries.
	@param medals_season: Season of medals to include (S for Summer, W for Winter, B for Both).
	@param data_type: Type of transformation to apply to the medals series (DEFAULT, LN_DIFF, PERCENTAGE).
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
		# Filter for specific country/countries and aggregate by year
		if isinstance(country, str):
			country_df = df[df['NOC'] == country]
		else:
			country_df = df[df['NOC'].isin(country)]
		medals_by_year = country_df.groupby('Year')['Total_Medals'].sum()
	
	# Convert to pandas Series with Year as index
	medals_series = pd.Series(medals_by_year.values, index=medals_by_year.index, name='Total_Medals')

	if data_type == DsMedalsDataType.LN_DIFF:
		medals_series = get_series_log_diff(medals_series)
	elif data_type == DsMedalsDataType.PERCENTAGE:
		medals_series = get_medal_series_percentage(medals_series, df)

	return medals_series



#
# Population
#


def load_population_maddison_series(
	country_code	: str | list[str],
	year_start		: int			= GDP_MADDISON_YEAR_START_DFLT,
	year_end		: int			= GDP_MADDISON_YEAR_END_DFLT,
	dataset_path	: str			= DS_POPULATION_MADDISON_PATH,
	data_type		: DsPopDataType = DsPopDataType.DEFAULT
) -> tuple[pd.Series, str]:
	"""Load population from Maddison Project Database.
	@param country_code: Mandatory country code(s) (3-letter) to filter by. Can be a single string or list of strings.
	@param year_start: Starting year for the data
	@param year_end: Ending year for the data
	@param dataset_path: Path to the Maddison CSV file
	@param data_type: Type of transformation to apply (DEFAULT or LN_DIFF)
	@return: A pandas Series indexed by Year with population values and the country name.
	"""
	
	# Convert single string to list
	if isinstance(country_code, str):
		country_code = [country_code]
	
	# Load the dataset, skipping the first 2 rows (metadata/regions)
	# Row 3 (index 2) contains the actual column names (year, country codes, etc)
	df = pd.read_csv(dataset_path, skiprows=2)
	
	# The first column is 'year' (or similar), and subsequent columns are country codes
	# Rename the first column to 'Year' if it's not already
	if 'year' in df.columns[0].lower():
		df = df.rename(columns={df.columns[0]: 'Year'})
	
	# Validate country codes
	for code in country_code:
		if code not in df.columns:
			raise ValueError(f"Country code '{code}' not found in dataset. Available countries: {', '.join(df.columns[1:])}")
	
	# Extract year and country data
	population_data = df[['Year'] + country_code].copy()
	population_data['Year'] = pd.to_numeric(population_data['Year'], errors='coerce')
	for code in country_code:
		population_data[code] = pd.to_numeric(population_data[code], errors='coerce')
	
	# Remove rows with NaN values
	population_data = population_data.dropna()
	
	# Filter by year range
	population_data = population_data[(population_data['Year'] >= year_start) & (population_data['Year'] <= year_end)]
	
	# Aggregate countries if multiple provided
	if len(country_code) > 1:
		population_values = population_data[country_code].sum(axis=1)
		country_name = '+'.join(country_code)
	else:
		population_values = population_data[country_code[0]]
		country_name = country_code[0]
	
	# Create Series with Year as index
	population_series = pd.Series(
		population_values.values,
		index=population_data['Year'].astype(int).values,
		name='Population'
	)
	
	if data_type == DsPopDataType.LN_DIFF:
		population_series = get_series_log_diff(population_series)
	
	return population_series, country_name


def load_population_extended_series(
	country_code	: str | list[str],
	year_start		: int			= GDP_MADDISON_YEAR_START_DFLT,
	year_end		: int			= GDPPC_PERC_WBOD_YEAR_LAST,
	dataset_path	: str			= DS_POPULATION_WBOD_PATH,
	data_type		: DsPopDataType = DsPopDataType.DEFAULT
) -> tuple[pd.Series, str]:
	"""Load population from Maddison (until 2022) and extend with WBOD data (2023-2024).
	@param country_code: Mandatory country code(s) (3-letter) to filter by. Can be a single string or list of strings.
	@param year_start: Starting year for the data
	@param year_end: Ending year for the data (up to 2024)
	@param dataset_path: Path to the WBOD population CSV file
	@param data_type: Type of transformation to apply (DEFAULT or LN_DIFF)
	@return: A pandas Series indexed by Year with population values and the country name.
	"""
	
	# Convert single string to list
	if isinstance(country_code, str):
		country_code = [country_code]
	
	# Load Maddison data (1800-2022)
	population_series, country_name = load_population_maddison_series(
		country_code=country_code,
		year_start=year_start,
		year_end=POPULATION_MADDISON_YEAR_LAST,
		data_type=DsPopDataType.DEFAULT  # Don't apply transformation yet
	)
	
	# If year_end <= 2022, just return the Maddison data
	if year_end <= POPULATION_MADDISON_YEAR_LAST:
		if data_type == DsPopDataType.LN_DIFF:
			population_series = get_series_log_diff(population_series)
		return population_series, country_name
	
	# Load population data from WBOD for years 2023-2024
	df_wbod = pd.read_csv(dataset_path)
	
	# Filter for specific countries
	country_df = df_wbod[df_wbod['Country Code'].isin(country_code)]
	
	if country_df.empty:
		# If no WBOD data available, just return Maddison data
		if data_type == DsPopDataType.LN_DIFF:
			population_series = get_series_log_diff(population_series)
		return population_series, country_name
	
	# Extend with WBOD data for years 2023 onwards
	extended_values = dict(population_series)  # Convert to dict
	
	for year in range(POPULATION_MADDISON_YEAR_LAST + 1, year_end + 1):
		year_str = str(year)
		pop_values = []
		for _, row in country_df.iterrows():
			if year_str in row.index:
				pop_value = row[year_str]
				if pd.notna(pop_value):
					try:
						pop_values.append(float(pop_value))
					except (ValueError, TypeError):
						pass
		if pop_values:
			extended_values[year] = sum(pop_values)
	
	# Create extended Series
	population_series = pd.Series(extended_values, name='Population')
	population_series = population_series.sort_index()
	
	if data_type == DsPopDataType.LN_DIFF:
		population_series = get_series_log_diff(population_series)
	
	return population_series, country_name


def load_population_series(
	country_code	: str | list[str],
	year_start		: int			= GDP_MADDISON_YEAR_START_DFLT,
	year_end		: int			= GDP_MADDISON_YEAR_END_DFLT,
	dataset_path	: str			= DS_POPULATION_MADDISON_PATH,
	data_type		: DsPopDataType = DsPopDataType.DEFAULT
) -> tuple[pd.Series, str]:
	"""
	@param country_code: Mandatory country code(s) to filter by. Can be a single string or list of strings.
	@param year_start: Starting year for the data
	@param year_end: Ending year for the data
	@param dataset_path: Path to the dataset CSV file. One of the two datasets (World Bank Open Data or Maddison Project Database) can be used, depending on the file path provided.
	@param data_type: Type of transformation to apply (DEFAULT or LN_DIFF)
	@return: A pandas Series indexed by Year with population values and the country name.
	"""

	#if dataset_path == DS_POPULATION_WBOD_PATH:
	#    # For WBOD, we would need a separate load function, but for now just use extended
	#    if year_end > POPULATION_MADDISON_YEAR_LAST:
	#        return load_population_extended_series(country_code, year_start, year_end, data_type=data_type)
	#    else:
	#        return load_population_maddison_series(country_code, year_start, year_end, DS_POPULATION_MADDISON_PATH, data_type)
	if dataset_path == DS_POPULATION_MADDISON_PATH:
		# Use extended version that includes WBOD data for 2023-2024
		if year_end > POPULATION_MADDISON_YEAR_LAST:
			return load_population_extended_series(country_code, year_start, year_end, data_type=data_type)
		else:
			return load_population_maddison_series(country_code, year_start, year_end, dataset_path, data_type)

	else:
		raise ValueError(f"Unsupported dataset path: {dataset_path}")
	


#
# Merge
#


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


GDP_MEAN_WINDOW_SIZE = 4

def load_medals_gdp_and_population_aligned(
	country				: str | list[str],
	year_start			: int				= MEDALS_FULL_YEAR_FIRST,
	year_end			: int				= MEDALS_FULL_YEAR_LAST,
	medals_season		: str				= 'S',
	gdp_year_shift		: int				= 0,
	population_year_shift		: int		= 0,
	use_gdp_mean		: bool				= False,
	use_population_mean	: bool				= False,
	use_communist_bloc	: bool				= False,
	remove_boycott		: bool				= False,
	medals_data_type	: DsMedalsDataType	= DsMedalsDataType.DEFAULT,
	gdp_data_type		: DsGdpDataType		= DsGdpDataType.DEFAULT,
	population_data_type	: DsPopDataType	= DsPopDataType.DEFAULT,
	medals_dataset_path	: str				= DS_MEDALS_FULL_PATH,
	gdp_dataset_path	: str				= DS_GDPPC_MADDISON_PATH,
	population_dataset_path	: str			= DS_POPULATION_MADDISON_PATH
) -> tuple[pd.DataFrame, str]:
	"""Load Olympic medals, GDP per capita, and population data with year alignment/shift.
	@param country: Country code(s) (NOC for medals, 3-letter for GDP and population). Can be a single string or list of strings.
	@param year_start: Starting year for medals data
	@param year_end: Ending year for medals data
	@param medals_season: Season of medals ('S' for Summer, 'W' for Winter, 'B' for Both)
	@param gdp_year_shift: Number of years to shift GDP backwards
	@param population_year_shift: Number of years to shift population backwards
	@param use_gdp_mean: Whether to use 4-year arithmetic mean of GDP
	@param use_population_mean: Whether to use 4-year arithmetic mean of population
	@param use_communist_bloc: Add a variable indicating whether the country is communist/was part of the communist bloc
	@param remove_boycott: Whether to remove years affected by boycotts (1980 and 1984)
	@param medals_data_type: Type of transformation for medals (DEFAULT, LN_DIFF, PERCENTAGE)
	@param gdp_data_type: Type of transformation for GDP (DEFAULT, LN_DIFF)
	@param population_data_type: Type of transformation for population (DEFAULT, LN_DIFF)
	@param medals_dataset_path: Path to medals CSV
	@param gdp_dataset_path: Path to GDP CSV
	@param population_dataset_path: Path to population CSV
	@return: tuple of (DataFrame with aligned 'Medals', 'GDP', and 'Population' columns indexed by Olympics year, country_name)
	"""
	
	# Load medals data
	medals_df = load_medals(
		country=country,
		year_start=year_start,
		year_end=year_end,
		medals_season=medals_season,
		dataset_path=medals_dataset_path,
		data_type=medals_data_type
	)
	

	# Load GDP per capita data with extended range to account for shift
	gdp_year_start	= year_start	- gdp_year_shift
	gdp_year_end	= year_end		- gdp_year_shift
	if use_gdp_mean:
		gdp_year_start -= GDP_MEAN_WINDOW_SIZE - 1
	
	gdp_series, country_name = load_gdp_series(
		country_code=country,
		year_start=gdp_year_start,
		year_end=gdp_year_end,
		dataset_path=gdp_dataset_path,
		data_type=gdp_data_type
	)
	
	# Create a shifted GDP series indexed by Olympics year
	# If gdp_year_shift=2, GDP from year 1998 becomes indexed as 2000
	gdp_shifted = pd.Series(
		gdp_series.values,
		index=gdp_series.index + gdp_year_shift,
		name='GDP'
	)

	if use_gdp_mean:
		# Calculate 4-year geometric mean of GDP to smooth out fluctuations
		# arithmetic mean of log = log of geometric mean
		gdp_shifted = gdp_shifted.rolling(window=GDP_MEAN_WINDOW_SIZE, min_periods=1).mean()
	

	# Load population data with extended range to account for shift
	pop_year_start	= year_start	- population_year_shift
	pop_year_end	= year_end		- population_year_shift
	if use_population_mean:
		pop_year_start -= GDP_MEAN_WINDOW_SIZE - 1
	
	population_series, _ = load_population_series(
		country_code=country,
		year_start=pop_year_start,
		year_end=pop_year_end,
		dataset_path=population_dataset_path,
		data_type=population_data_type
	)
	
	# Create a shifted population series indexed by Olympics year
	population_shifted = pd.Series(
		population_series.values,
		index=population_series.index + population_year_shift,
		name='Population'
	)

	if use_population_mean:
		population_shifted = population_shifted.rolling(window=GDP_MEAN_WINDOW_SIZE, min_periods=1).mean()
	
	
	# Merge the two series
	merged_df = pd.DataFrame({
		DF_COL_MEDALS		: medals_df['Total_Medals'],
		DF_COL_GDP			: gdp_shifted,
		DF_COL_POPULATION	: population_shifted,
		DF_COL_IS_HOST		: medals_df['Is_Host'],
		DF_COL_IS_BOYCOTT	: medals_df['Is_Boycott']
	})
	
	# Drop rows with NaN values
	merged_df = merged_df.dropna()

	# Optionally add Is_Communist column
	if use_communist_bloc:
		merged_df[DF_COL_IS_COMMUNIST] = country in COMMUNIST_BLOC_COUNTRIES

	# Optionally remove years affected by boycotts
	if remove_boycott:
		merged_df = merged_df[~merged_df.index.isin([YEAR_BOYCOTT_URS, YEAR_BOYCOTT_USA])]
	
	return merged_df, country_name

