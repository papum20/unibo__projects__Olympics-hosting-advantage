from enum import Enum

import numpy as np
import pandas as pd


DS_EXCLUDED_COUNTRIES_PATH	= 'dataset/excluded_countries.csv'
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
DF_COL_AM_HISTORY				= 'Avg_Medals_History'
DF_COL_EVENTS					= 'Events'
DF_COL_EVENTS_HOME				= 'Events_Home'
DF_COL_GDP						= 'GDP'
DF_COL_IS_BOYCOTT_URS			= f'Is_Boycott{YEAR_BOYCOTT_URS}'
DF_COL_IS_BOYCOTT_USA			= f'Is_Boycott{YEAR_BOYCOTT_USA}'
DF_COL_IS_COMMUNIST				= 'Is_Communist'
DF_COL_IS_HOST					= 'Is_Host'
DF_COL_IS_HOST_PRE				= 'Is_Host_Pre'
DF_COL_IS_HOST_POST				= 'Is_Host_Post'
DF_COL_IS_HOST_CLOSE_CENTER		= 'Is_Host_Close_Center'
DF_COL_IS_HOST_CLOSE_GMT1		= 'Is_Host_Close_GMT1'
DF_COL_IS_HOST_CLOSE_MAIN		= 'Is_Host_Close_Main'
DF_COL_IS_HOST_CLOSE_WEST		= 'Is_Host_Close_West'
DF_COL_IS_HOST_CLOSE_WIDE		= 'Is_Host_Close_Wide'
DF_COL_MEDALS					= 'Medals'
DF_COL_MEDALS_AVAILABLE			= 'Medals_Available'
DF_COL_MEDALS_AVAILABLE_HOME	= 'Medals_Available_Home'
DF_COL_MEDALS_HOME				= 'Med_Home'
DF_COL_MEDALS_AWAY				= 'Med_Away'
DF_COL_MEDALS_HOME_DIFF			= 'Med_HomeDiff'
DF_COL_NOC						= 'NOC'
DF_COL_POPULATION				= 'Population'
DF_COL_YEAR						= 'Year'

def DF_COL_YEAR_DUMMY(year: int) -> str:
	return f'YEAR{year}'

def DF_COL_IS_HOST_OG_YEAR(year: int) -> str:
	return f'OG{year}'

def DF_COL_IS_HOST_PRE_YEAR(year: int) -> str:
	return f'PRE{year}'

def DF_COL_IS_HOST_POST_YEAR(year: int) -> str:
	return f'POST{year}'

def DF_COL_IS_HOST_CLOSE_CENTER_YEAR(year: int) -> str:
	return f'CLOSE_CENTER{year}'
def DF_COL_IS_HOST_CLOSE_GMT1_YEAR(year: int) -> str:
	return f'CLOSE_GMT1{year}'
def DF_COL_IS_HOST_CLOSE_MAIN_YEAR(year: int) -> str:
	return f'CLOSE_MAIN{year}'
def DF_COL_IS_HOST_CLOSE_WEST_YEAR(year: int) -> str:
	return f'CLOSE_WEST{year}'
def DF_COL_IS_HOST_CLOSE_WIDE_YEAR(year: int) -> str:
	return f'CLOSE_WIDE{year}'


def is_dfCol_yearDummy(col_name: str) -> bool:
	return col_name.startswith('YEAR') and col_name[4:].isdigit()

def is_dfCol_isHostOg_separate(col_name: str) -> bool:
	return col_name.startswith('OG') and col_name[2:].isdigit()

def is_dfCol_isHostPre_separate(col_name: str) -> bool:
	return col_name.startswith('PRE') and col_name[3:].isdigit()

def is_dfCol_isHostPost_separate(col_name: str) -> bool:
	return col_name.startswith('POST') and col_name[4:].isdigit()

def is_dfCol_isHostCloseCenter_separate(col_name: str) -> bool:
	return col_name.startswith('CLOSE_CENTER') and col_name[13:].isdigit()
def is_dfCol_isHostClose_GMT1_separate(col_name: str) -> bool:
	return col_name.startswith('CLOSE_GMT1') and col_name[11:].isdigit()
def is_dfCol_isHostClose_Main_separate(col_name: str) -> bool:
	return col_name.startswith('CLOSE_MAIN') and col_name[11:].isdigit()
def is_dfCol_isHostClose_West_separate(col_name: str) -> bool:
	return col_name.startswith('CLOSE_WEST') and col_name[11:].isdigit()
def is_dfCol_isHostClose_Wide_separate(col_name: str) -> bool:
	return col_name.startswith('CLOSE_WIDE') and col_name[11:].isdigit()


COMMUNIST_BLOC_COUNTRIES = {
	'ALB', 'BGD', 'BGR', 'BLR', 'CHN', 'CSK', 'CUB', 'DDR', 'EST', 'HUN', 'KAZ',
	'KGZ', 'LAO', 'LTU', 'LVA', 'MDA', 'MNG', 'PRK', 'ROU', 'RUS', 'TJK', 'TKM',
	'UKR', 'URS', 'UZB', 'YUG'
}

CLOSE_GROUP_EU_CENTRAL = [
	'AUT', 'CZE', 'FRG', 'GER', 'HUN', 'POL', 'SLO', 'SVK', 'SWI'
]
CLOSE_GROUP_EU_WEST = [
	'BEL', 'FRA', 'NED', 
]
CLOSE_GROUP_EU_GMT1 = [
	'ESP', 'ITA'
] + CLOSE_GROUP_EU_CENTRAL + CLOSE_GROUP_EU_WEST
CLOSE_GROUP_EU_MAIN = [
	'ESP', 'FRA', 'GER', 'ITA'
]
CLOSE_GROUP_EU_WIDE = [
	'GBR', 'GRE'
] + CLOSE_GROUP_EU_GMT1

# NOC codes that should be treated as RUS (e.g. Olympic Athletes from Russia, Russian Olympic Committee)
NOC_TO_RUS = {
	'OAR': 'RUS',
	'ROC': 'RUS'
}

# IOC to NOC mapping
# IOC codes are used in GDP and Population datasets (Maddison, World Bank)
# NOC codes are used in Medal datasets
IOC_TO_NOC = {
	'AFG': 'AFG', 'ALB': 'ALB', 'DZA': 'ALG', 'ASM': 'ASA', 'AND': 'AND', 'AGO': 'ANG',
	'ATG': 'ANT', 'ARG': 'ARG', 'ARM': 'ARM', 'ABW': 'ARU', 'AUS': 'AUS', 'AUT': 'AUT',
	'AZE': 'AZE',

	'BHS': 'BAH', 'BHR': 'BRN', 'BGD': 'BAN', 'BRB': 'BAR', 'BLR': 'BLR', 'BEL': 'BEL',
	'BLZ': 'BIZ', 'BEN': 'BEN', 'BMU': 'BER', 'BTN': 'BHU', 'BOL': 'BOL', 'BIH': 'BIH',
	'BWA': 'BOT', 'BRA': 'BRA', 'VGB': 'IVB', 'BRN': 'BRU', 'BGR': 'BUL', 'BFA': 'BUR',
	'BDI': 'BDI',

	'KHM': 'CAM', 'CMR': 'CMR', 'CAN': 'CAN', 'CPV': 'CPV', 'CYM': 'CAY', 'CAF': 'CAF',
	'TCD': 'CHA', 'CHL': 'CHI', 'CHN': 'CHN', 'COL': 'COL', 'COM': 'COM', 'COG': 'CGO',
	'COD': 'COD', 'COK': 'COK', 'CRI': 'CRC', 'CIV': 'CIV', 'HRV': 'CRO', 'CSK': 'TCH',
	'CUB': 'CUB', 'CYP': 'CYP', 'CZE': 'CZE',

	'DNK': 'DEN', 'DJI': 'DJI', 'DMA': 'DMA', 'DOM': 'DOM',

	'ECU': 'ECU', 'EGY': 'EGY', 'SLV': 'ESA', 'GNQ': 'GEQ', 'ERI': 'ERI', 'EST': 'EST',
	'ETH': 'ETH',

	'FJI': 'FIJ', 'FIN': 'FIN', 'FRA': 'FRA',

	'GAB': 'GAB', 'GMB': 'GAM', 'GEO': 'GEO', 'DEU': 'GER', 'GHA': 'GHA', 'GRC': 'GRE',
	'GRD': 'GRN', 'GUM': 'GUM', 'GTM': 'GUA', 'GIN': 'GUI', 'GNB': 'GBS', 'GUY': 'GUY',

	'HTI': 'HAI', 'HND': 'HON', 'HKG': 'HKG', 'HUN': 'HUN',

	'ISL': 'ISL', 'IND': 'IND', 'IDN': 'INA', 'IRN': 'IRI', 'IRQ': 'IRQ', 'IRL': 'IRL',
	'ISR': 'ISR', 'ITA': 'ITA', 'ISV': 'ISV',

	'JAM': 'JAM', 'JPN': 'JPN', 'JOR': 'JOR',

	'KAZ': 'KAZ', 'KEN': 'KEN', 'KIR': 'KIR', 'KOR': 'KOR', 'KWT': 'KUW',
	'KGZ': 'KGZ', 'KNA': 'SKN',

	'LAO': 'LAO', 'LVA': 'LAT', 'LBN': 'LIB', 'LSO': 'LES', 'LBR': 'LBR', 'LBY': 'LBA',
	'LIE': 'LIE', 'LTU': 'LTU', 'LUX': 'LUX', 'LCA': 'LCA', 'LKA': 'SRI',

	'MDG': 'MAD', 'MWI': 'MAW', 'MYS': 'MAS', 'MDV': 'MDV', 'MLI': 'MLI', 'MLT': 'MLT',
	'MHL': 'MHL', 'MRT': 'MTN', 'MUS': 'MRI', 'MEX': 'MEX', 'FSM': 'FSM', 'MDA': 'MDA',
	'MCO': 'MON', 'MNG': 'MGL', 'MNE': 'MNE', 'MAR': 'MAR', 'MOZ': 'MOZ', 'MMR': 'MYA',
	'MKD': 'MKD',

	'NAM': 'NAM', 'NRU': 'NRU', 'NPL': 'NEP', 'NLD': 'NED', 'NZL': 'NZL', 'NIC': 'NCA',
	'NER': 'NIG', 'NGA': 'NGR', 'NOR': 'NOR',

	'OMN': 'OMA',

	'PAK': 'PAK', 'PLW': 'PLW', 'PSE': 'PLE', 'PAN': 'PAN', 'PNG': 'PNG', 'PRY': 'PAR',
	'PER': 'PER', 'PHL': 'PHI', 'POL': 'POL', 'PRT': 'POR', 'PRI': 'PUR', 'PRK': 'PRK',

	'QAT': 'QAT',

	'ROU': 'ROU', 'RUS': 'RUS', 'RWA': 'RWA',

	'SMR': 'SMR', 'STP': 'STP', 'SAU': 'KSA', 'SEN': 'SEN', 'SRB': 'SRB',
	'SYC': 'SEY', 'SLE': 'SLE', 'SGP': 'SGP', 'SVK': 'SVK', 'SVN': 'SLO', 'SLB': 'SOL',
	'SOM': 'SOM', 'ZAF': 'RSA', 'SSD': 'SSD', 'ESP': 'ESP', 'SDN': 'SUD', 'SUR': 'SUR',
	'SWZ': 'SWZ', 'SWE': 'SWE', 'CHE': 'SUI', 'SYR': 'SYR',

	'TWN': 'TPE', 'TJK': 'TJK', 'TZA': 'TAN', 'THA': 'THA', 'TLS': 'TLS', 'TGO': 'TOG',
	'TON': 'TGA', 'TTO': 'TTO', 'TUN': 'TUN', 'TUR': 'TUR', 'TKM': 'TKM', 'TUV': 'TUV',

	'UGA': 'UGA', 'UKR': 'UKR', 'ARE': 'UAE', 'GBR': 'GBR', 'USA': 'USA', 'URY': 'URU',
	'UZB': 'UZB',

	'VUT': 'VAN', 'VEN': 'VEN', 'VNM': 'VIE', 'VIN': 'VIN',

	'WSM': 'SAM', 

	'YEM': 'YEM',

	'ZMB': 'ZAM', 'ZWE': 'ZIM'
}


class DsGdpDataType(Enum):
	DEFAULT		= "default"
	LN			= "ln"
	# first difference of logarithms (GDP growth rate)
	LN_DIFF		= "ln_diff"


class DsPopDataType(Enum):
	DEFAULT		= "default"
	LN			= "ln"
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


def get_series_log(series: pd.Series) -> pd.Series:
	"""Helper function to get the natural log of a series.
	@param series: pandas Series values indexed by year
	@return: pandas Series of log values
	"""
	return pd.Series(np.log(series), index=series.index)

def get_series_log_diff(series: pd.Series) -> pd.Series:
	"""Helper function to get the log-differenced series.
	@param series: pandas Series values indexed by year
	@return: pandas Series of log-differenced values (growth rates)
	"""
	# Take the natural log of the series
	ln_series = pd.Series(np.log(series), index=series.index)
	# Take the first difference of the log (% growth rate)
	growth_rate = ln_series.diff().dropna()
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

def ioc_to_noc(country_code: str) -> str:
	"""Convert IOC country code to NOC code if mapping exists.
	@param country_code: IOC country code (3-letter)
	@return: Corresponding NOC code or original code if no mapping exists.
	"""
	return IOC_TO_NOC.get(country_code, country_code)

def rename_df_columns_ioc_to_noc(df: pd.DataFrame) -> pd.DataFrame:
	"""Rename columns of a DataFrame from IOC to NOC codes.
	Useful for datasets where each country is a column (e.g. Maddison).
	@param df: pandas DataFrame with IOC codes as column names
	@return: DataFrame with renamed columns
	"""
	return df.rename(columns=IOC_TO_NOC)

def rename_df_values_ioc_to_noc(df: pd.DataFrame, column_name: str) -> pd.DataFrame:
	"""Rename the values in a column from IOC to NOC code.
	Useful for datasets where each country is a column (e.g. Maddison).
	@param df: pandas DataFrame with IOC codes as column names
	@param column_name: Name of the column to update
	@return: DataFrame with the renamed values in the specified column
	"""
	df[column_name] = df[column_name].map(lambda x: IOC_TO_NOC.get(x, x))	# type: ignore
	return df



#
# GDP
#


def load_gdppc_maddison_series(
	country_code	: str,
	year_start		: int			= GDP_MADDISON_YEAR_START_DFLT,
	year_end		: int			= GDP_MADDISON_YEAR_END_DFLT,
	dataset_path	: str			= DS_GDPPC_MADDISON_PATH,
	data_type		: DsGdpDataType = DsGdpDataType.DEFAULT
) -> tuple[pd.Series, str]:
	"""Load GDP per capita from Maddison Project Database.
	@param country_code: Mandatory country code (3-letter) to filter by.
	@param year_start: Starting year for the data
	@param year_end: Ending year for the data
	@param dataset_path: Path to the Maddison CSV file
	@param data_type: Type of transformation to apply (DEFAULT or LN_DIFF)
	@return: A pandas Series indexed by Year with GDP per capita values and the country name.
	"""
	
	# Load the dataset, skipping the first 2 rows (metadata/regions)
	# Row 3 (index 2) contains the actual column names (year, country codes, etc)
	df = pd.read_csv(dataset_path, skiprows=2)
	
	# The first column is 'year' (or similar), and subsequent columns are country codes
	# Rename the first column to 'Year' if it's not already
	if 'year' in df.columns[0].lower():
		df = df.rename(columns={df.columns[0]: 'Year'})
	
	# Rename IOC columns to NOC
	df = rename_df_columns_ioc_to_noc(df)
	
	# Filter for the specific country column
	if country_code not in df.columns:
		raise ValueError(f"Country code '{country_code}' not found in GDPpc dataset.")
	
	# Extract year and country data
	gdppc_data					= df[['Year', country_code]].copy()
	gdppc_data['Year']			= pd.to_numeric(gdppc_data['Year'], errors='coerce')
	gdppc_data[country_code]	= pd.to_numeric(gdppc_data[country_code], errors='coerce')
	
	# Remove rows with NaN values
	gdppc_data = gdppc_data.dropna()
	
	# Filter by year range
	gdppc_data = gdppc_data[(gdppc_data['Year'] >= year_start) & (gdppc_data['Year'] <= year_end)]
	
	# Create Series with Year as index
	gdppc_series = pd.Series(
		gdppc_data[country_code].values,
		index=gdppc_data['Year'].astype(int).values,
		name='GDP_per_capita'
	)
	
	# Get country name from the first row metadata (optional, fallback to country code)
	country_name = country_code
	
	if data_type == DsGdpDataType.LN:
		gdppc_series = get_series_log(gdppc_series)
	elif data_type == DsGdpDataType.LN_DIFF:
		gdppc_series = get_series_log_diff(gdppc_series)
	
	return gdppc_series, ioc_to_noc(country_name)


def load_gdppc_extended_series(
	country_code	: str,
	year_start		: int			= GDP_MADDISON_YEAR_START_DFLT,
	year_end		: int			= GDPPC_PERC_WBOD_YEAR_LAST,
	dataset_path	: str			= DS_GDPPC_PERC_WBOD_PATH,
	data_type		: DsGdpDataType = DsGdpDataType.DEFAULT
) -> tuple[pd.Series, str]:
	"""Load GDP per capita from Maddison (until 2022) and extend with WBOD percentage changes (2023-2024).
	@param country_code: Mandatory country code (3-letter) to filter by.
	@param year_start: Starting year for the data
	@param year_end: Ending year for the data (up to 2024)
	@param dataset_path: Path to the WBOD percentage changes CSV file
	@param data_type: Type of transformation to apply (DEFAULT or LN_DIFF)
	@return: A pandas Series indexed by Year with GDP per capita values and the country name.
	"""

	# convert all NOCs at the end, for clarity
	
	# Load Maddison data (1800-2022)
	gdppc_series, country_name = load_gdppc_maddison_series(
		country_code=country_code,
		year_start=year_start,
		year_end=GDP_MADDISON_YEAR_LAST,
		data_type=DsGdpDataType.DEFAULT  # Don't apply transformation yet
	)
	
	# If year_end <= 2022, just return the Maddison data
	if year_end <= GDP_MADDISON_YEAR_LAST:
		if data_type == DsGdpDataType.LN:
			gdppc_series = get_series_log(gdppc_series)
		elif data_type == DsGdpDataType.LN_DIFF:
			gdppc_series = get_series_log_diff(gdppc_series)
		return gdppc_series, country_name
	
	# Load percentage changes from WBOD for years 2023-2024
	df_perc = pd.read_csv(dataset_path)
	
	df_perc = rename_df_values_ioc_to_noc(df_perc, 'Country Code')
	
	# Filter for specific country
	country_df = df_perc[df_perc['Country Code'] == country_code]
	
	if country_df.empty:
		# If no percentage data available, just return Maddison data
		if data_type == DsGdpDataType.LN:
			gdppc_series = get_series_log(gdppc_series)
		elif data_type == DsGdpDataType.LN_DIFF:
			gdppc_series = get_series_log_diff(gdppc_series)
		return gdppc_series, country_name
	
	country_perc_data	= country_df.iloc[0]
	last_gdppc_value	= gdppc_series.iloc[-1]  # Last value from Maddison (2022)
	
	# Extend with percentage changes
	extended_values	= dict(gdppc_series)  # Convert to dict
	current_value	= last_gdppc_value
	
	for year in range(GDP_MADDISON_YEAR_LAST + 1, year_end + 1):
		year_str = str(year)
		if year_str in country_perc_data.index:
			perc_change = country_perc_data[year_str]
			if pd.notna(perc_change):
				try:
					# Percentage change (multiply by 1 + percentage/100)
					perc_change_float		= float(perc_change) / 100.0
					current_value			= current_value * (1 + perc_change_float)
					extended_values[year]	= current_value
				except (ValueError, TypeError):
					pass
	
	# Create extended Series
	gdppc_series = pd.Series(extended_values, name='GDP_per_capita')
	gdppc_series = gdppc_series.sort_index()
	
	if data_type == DsGdpDataType.LN:
		gdppc_series = get_series_log(gdppc_series)
	elif data_type == DsGdpDataType.LN_DIFF:
		gdppc_series = get_series_log_diff(gdppc_series)
	
	return gdppc_series, country_name


def load_gdp_wbod_series(
	country_code	: str,
	year_start		: int			= GDP_WBOD_YEAR_FIRST,
	year_end		: int			= GDP_WBOD_YEAR_LAST,
	dataset_path	: str			= DS_GDP_WBOD_PATH,
	data_type		: DsGdpDataType = DsGdpDataType.DEFAULT
) -> tuple[pd.Series, str]:
	"""@param country_code: Mandatory country code to filter by.
	@return: A pandas Series indexed by Year with GDP values and the country name.
	"""

	# Load the dataset
	df = pd.read_csv(dataset_path)
	
	df = rename_df_values_ioc_to_noc(df, 'Country Code')
	
	# Filter for specific country
	country_df = df[df['Country Code'] == country_code]
	
	if country_df.empty:
		raise ValueError(f"Country code '{country_code}' not found in GDP dataset")
	
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

	if data_type == DsGdpDataType.LN:
		gdp_series = get_series_log(gdp_series)
	elif data_type == DsGdpDataType.LN_DIFF:
		gdp_series = get_series_log_diff(gdp_series)	
	
	# The country filter was already applied using 'Country Code' from the dataset, 
	# which uses IOC codes. The name is just for display.
	return gdp_series, ioc_to_noc(country_data['Country Code'])


def load_gdp_series(
	country_code	: str,
	year_start		: int			= GDP_MADDISON_YEAR_START_DFLT,
	year_end		: int			= GDP_MADDISON_YEAR_END_DFLT,
	dataset_path	: str			= DS_GDPPC_MADDISON_PATH,
	data_type		: DsGdpDataType = DsGdpDataType.DEFAULT
) -> tuple[pd.Series, str]:
	"""
	@param country_code: Mandatory country code to filter by.
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


def _get_all_countries_list(
	year_start	: int	= MEDALS_FULL_YEAR_FIRST,
	year_end	: int	= MEDALS_FULL_YEAR_LAST,
) -> list[str]:
	"""Get a list of all unique country codes (NOCs) from the medals dataset."""
	df = pd.read_csv(DS_MEDALS_FULL_PATH, usecols=['Year', 'NOC'])

	# Convert OAR and ROC to RUS
	df['NOC'] = df['NOC'].replace(NOC_TO_RUS)

	countries = df[(df['Year'] >= year_start) & (df['Year'] <= year_end)]
	countries = countries['NOC'].dropna().unique().tolist()
	return countries


def _get_total_medals_by_year(
	year_start	: int	= MEDALS_FULL_YEAR_FIRST,
	year_end	: int	= MEDALS_FULL_YEAR_LAST,
	medals_season: str	= 'S',
) -> pd.Series:
	"""Get a Series with total medals awarded each year in the specified season."""
	df = pd.read_csv(DS_MEDALS_FULL_PATH, usecols=['Year', 'Season', 'Total_Medals'])
	df = df[(df['Year'] >= year_start) & (df['Year'] <= year_end)]

	if medals_season == 'S':
		df = df[df['Season'] == 'Summer']
	elif medals_season == 'W':
		df = df[df['Season'] == 'Winter']
	elif medals_season == 'B':
		df = df[df['Season'].isin(['Summer', 'Winter'])]

	total_medals_by_year = df.groupby('Year')['Total_Medals'].sum()
	return total_medals_by_year


def get_top_countries_by_medals(
	n				: int	= 40,
	year_start		: int	= MEDALS_FULL_YEAR_FIRST,
	year_end		: int	= MEDALS_FULL_YEAR_LAST,
	medals_season	: str	= 'S',
	dataset_path	: str	= DS_MEDALS_FULL_PATH,
	is_verbose		: bool	= True
):
	"""Calculate the countries' AVERAGE medal share across the years in which they actually competed.
	Don't consider the excluded Countries dataset, since they will be excluded anyway.
	@param n: Number of top countries to return
	@param year_start: Starting year for the data
	@param year_end: Ending year for the data
	@param medals_season: Season of medals to include (S for Summer, W for Winter, B for Both).
	@param dataset_path: Path to the medals dataset CSV file
	@param is_verbose: Whether to print the number of unique countries found in the dataset
	@return: List of top n country codes (NOCs) with the highest average medal share (hosts are ranked before)
	"""
	excluded_countries	= pd.read_csv(DS_EXCLUDED_COUNTRIES_PATH, usecols=['NOC'])
	excluded_countries	= excluded_countries['NOC'].dropna().unique().tolist()

	df			= pd.read_csv(dataset_path, usecols=['Year', 'Season', 'NOC', 'Total_Medals', 'Is_Host'])
	df['NOC']	= df['NOC'].replace(NOC_TO_RUS)
	df			= df[~df['NOC'].isin(excluded_countries)]

	if medals_season == 'S':
		df = df[df['Season'] == 'Summer']
	elif medals_season == 'W':
		df = df[df['Season'] == 'Winter']
	elif medals_season == 'B':
		df = df[df['Season'].isin(['Summer', 'Winter'])]

	# Filter immediately by year range
	df = df[(df['Year'] >= year_start) & (df['Year'] <= year_end)]

	df					= df.set_index('Year').sort_index()
	medals_perc_series	= get_medal_series_percentage(df['Total_Medals'], df)
	df['Total_Medals']	= medals_perc_series.reindex(df.index)

	host_list = df[df['Is_Host'] == True]['NOC'].unique().tolist()
	
	# first try to take n from the hosts
	host_df		= df.copy()
	host_df		= host_df[host_df['NOC'].isin(host_list)]
	host_means	= host_df.groupby('NOC')['Total_Medals'].mean()
	top_list	= host_means.nlargest(n).index.tolist()

	ranking_df	= host_means.copy()

	n_remaining		= n - len(top_list)
	non_host_means	= pd.Series(dtype=float)
	if n_remaining > 0:
		non_host_df		= df[~df['NOC'].isin(host_list)]
		non_host_means	= non_host_df.groupby('NOC')['Total_Medals'].mean()
		top_list		+= non_host_means.nlargest(n_remaining).index.tolist()
		ranking_df		= pd.concat([ranking_df, non_host_means])
	
	if is_verbose:
		print(f"Found {len(host_means)+len(non_host_means)} unique countries in the medals dataset for season '{medals_season}'.")
		
		def print_ranked(series, label):
			# Sort and convert to DataFrame
			df_ranked = series.sort_values(ascending=False).reset_index()
			df_ranked.columns = ['NOC', 'Avg_Share']
			# Add ordinal rank starting from 1
			df_ranked.index = df_ranked.index + 1
			df_ranked.index.name = 'Rank'
			print(f"\n{label}:\n{df_ranked.to_string()}")

		print_ranked(host_means, f"Hosting ({len(host_means)})")
		print_ranked(non_host_means, f"Non-Hosting ({len(non_host_means)})")
		print_ranked(ranking_df, f"All ({len(ranking_df)})")
	return top_list


def load_medals(
	country			: str|None			= None,
	year_start		: int				= MEDALS_FULL_YEAR_FIRST,
	year_end		: int				= MEDALS_FULL_YEAR_LAST,
	medals_season	: str				= 'S',
	dataset_path	: str				= DS_MEDALS_FULL_PATH,
	data_type		: DsMedalsDataType	= DsMedalsDataType.DEFAULT
) -> pd.DataFrame:
	"""Load medals data with Is_Host and Is_Boycott columns.
	@param country: Optional country code (NOC) to filter by.
	@param medals_season: Season of medals to include (S for Summer, W for Winter, B for Both).
	@param data_type: Type of transformation to apply to the medals series (DEFAULT, LN_DIFF, PERCENTAGE)
	@return: DataFrame indexed by Year with Total_Medals, Is_Host, and Is_Boycott columns.
	"""
	
	df = pd.read_csv(dataset_path, usecols=['Year', 'Season', 'NOC', 'Total_Medals', 'Is_Host'])
	
	# Convert OAR and ROC to RUS
	df['NOC'] = df['NOC'].replace(NOC_TO_RUS)

	if medals_season == 'S':
		medals_df = df[df['Season'] == 'Summer']
	elif medals_season == 'W':
		medals_df = df[df['Season'] == 'Winter']
	elif medals_season == 'B':
		medals_df = df[df['Season'].isin(['Summer', 'Winter'])]
	
	if country:
		medals_df = medals_df[medals_df['NOC'] == country]
	
	# Group by year and aggregate
	medals_df = medals_df.groupby('Year').agg({
		'Total_Medals'	: 'sum',
		'Is_Host'		: 'any'  # True if any entry for that year is a host
	}).reset_index()
	
	medals_df[f'Is_Boycott{YEAR_BOYCOTT_URS}'] = medals_df['Year'].isin([YEAR_BOYCOTT_URS])
	medals_df[f'Is_Boycott{YEAR_BOYCOTT_USA}'] = medals_df['Year'].isin([YEAR_BOYCOTT_USA])
	
	# Set index to Year early to ensure transformations align correctly
	medals_df = medals_df.set_index('Year').sort_index()

	medals_series_perc = get_medal_series_percentage(medals_df['Total_Medals'], df).reindex(medals_df.index).fillna(0)

	if data_type == DsMedalsDataType.LN_DIFF:
		# get_series_log_diff returns a series indexed by Year
		# We use .reindex() to keep the original years (filling the first gap with 0 or NaN)
		transformed = get_series_log_diff(medals_df['Total_Medals'])
		medals_df['Total_Medals'] = transformed.reindex(medals_df.index).fillna(0)
	elif data_type == DsMedalsDataType.PERCENTAGE:
		transformed = get_medal_series_percentage(medals_df['Total_Medals'], df)
		medals_df['Total_Medals'] = transformed.reindex(medals_df.index).fillna(0)


	if country:
		# Calculate the Expanding Mean of their Medal Share
		# We use .shift(1) so the current year's medals aren't included in the past average
		medals_df[DF_COL_AM_HISTORY] = medals_series_perc.shift(1).expanding().mean()

		# Fill any NaNs (for a country's very first Olympics) with 0
		medals_df[DF_COL_AM_HISTORY] = medals_df[DF_COL_AM_HISTORY].fillna(0)


	medals_df = medals_df[(medals_df.index >= year_start) & (medals_df.index <= year_end)]
	return medals_df



class DsMedalsAggrType(Enum):
	AVG = "avg"
	SUM = "sum"

def load_medals_homeDiff(
	countries_list			: list[str]|None	= None,
	year_start				: int				= MEDALS_FULL_YEAR_FIRST,
	year_end				: int				= MEDALS_FULL_YEAR_LAST,
	min_events_n			: int				= 0,
	medals_season			: str				= 'S',
	remove_boycott			: bool				= False,
	until_first_host		: bool				= False,
	from_last_host			: bool				= False,
	medals_data_type		: DsMedalsDataType	= DsMedalsDataType.DEFAULT,
	medals_aggr_type		: DsMedalsAggrType	= DsMedalsAggrType.AVG,
	medals_dataset_path		: str				= DS_MEDALS_FULL_PATH,
	is_verbose				: bool				= True
) -> tuple[pd.DataFrame, str]:
	"""Calculate the difference in medals won when hosting vs not hosting.
	@param countries_list: Optional list of country codes to include. If None, includes all countries.
	@param min_events_n: Minimum number of events participated in to be included in the calculation.
	@param medals_season: Season of medals to include (S for Summer, W for Winter, B for Both).
	@param remove_boycott: Whether to exclude years with boycotts from the calculation.
	@param until_first_host: Whether to only consider years up until the country's first time hosting (inclusive).
	@param from_last_host: Whether to only consider years from the country's last time hosting (inclusive) (first host has priority).
	@param medals_data_type: Type of transformation to apply to the medals series (DEFAULT, LN_DIFF, PERCENTAGE)
	@param medals_aggr_type: Whether to calculate the average (AVG) or total (SUM) medals for home and away.
	@param medals_dataset_path: Path to the medals dataset CSV file
	@param is_verbose: Whether to print the number of unique countries found in the dataset
	@return: DataFrame with columns for Home Medal Count, Away Medal Count, and the Difference.
	"""

	if countries_list is None:
		countries_list = _get_all_countries_list(year_start, year_end)
		if is_verbose:
			print(f"Found {len(countries_list)} unique countries in the medals dataset for season '{medals_season}'.")

	total_medals_df = _get_total_medals_by_year(year_start, year_end, medals_season)

	results = []
	
	for country in countries_list:
		medals_df = load_medals(
			country=country,
			year_start=year_start,
			year_end=year_end,
			medals_season=medals_season,
			dataset_path=medals_dataset_path,
			data_type=medals_data_type
		)
		
		if remove_boycott:
			medals_df = medals_df[~medals_df.index.isin([YEAR_BOYCOTT_URS, YEAR_BOYCOTT_USA])]

		if until_first_host:
			first_host_year = medals_df[medals_df[DF_COL_IS_HOST] == True].index.min()
			medals_df = medals_df[medals_df.index <= first_host_year]
		elif from_last_host:
			last_host_year = medals_df[medals_df[DF_COL_IS_HOST] == True].index.max()
			medals_df = medals_df[medals_df.index >= last_host_year]

		events_home_n	= medals_df[medals_df[DF_COL_IS_HOST] == True].shape[0]
		events_n		= medals_df.shape[0]

		host_years = medals_df[medals_df[DF_COL_IS_HOST] == True].index
		# Get total medals available only for years this country participated
		available_medals_series = total_medals_df.loc[medals_df.index]

		if medals_aggr_type == DsMedalsAggrType.AVG:
			home_medals			= medals_df[medals_df[DF_COL_IS_HOST] == True]['Total_Medals'].mean()
			away_medals			= medals_df[medals_df[DF_COL_IS_HOST] == False]['Total_Medals'].mean()
			total_medals_home	= total_medals_df.loc[host_years].mean()
			total_medals		= available_medals_series.mean()
		elif medals_aggr_type == DsMedalsAggrType.SUM:
			home_medals			= medals_df[medals_df[DF_COL_IS_HOST] == True]['Total_Medals'].sum()
			away_medals			= medals_df[medals_df[DF_COL_IS_HOST] == False]['Total_Medals'].sum()
			total_medals_home	= total_medals_df.loc[host_years].sum()
			total_medals	= available_medals_series.sum()
		else:
			raise ValueError(f"Unsupported medals_aggr_type: {medals_aggr_type}")

		diff		= home_medals - away_medals

		results.append({
			DF_COL_NOC:						country,
			DF_COL_MEDALS_HOME:				home_medals,
			DF_COL_MEDALS_AWAY:				away_medals,
			DF_COL_MEDALS_HOME_DIFF:		diff,
			DF_COL_MEDALS_AVAILABLE:		total_medals,
			DF_COL_MEDALS_AVAILABLE_HOME:	total_medals_home,
			DF_COL_EVENTS:					events_n,
			DF_COL_EVENTS_HOME:				events_home_n
		})

	# Filter out countries with fewer than min_events_n events
	results = [r for r in results if r[DF_COL_EVENTS] >= min_events_n]

	return pd.DataFrame(results), '+'.join(countries_list)


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
	@param data_type: Type of transformation to apply to the medals series (DEFAULT, LN_DIFF, PERCENTAGE).
	@return: A pandas Series indexed by Year with total medals as values.
	"""

	medals_df = load_medals(
		country=country,
		year_start=year_start,
		year_end=year_end,
		medals_season=medals_season,
		dataset_path=dataset_path,
		data_type=data_type
	)

	return medals_df['Total_Medals']



#
# Population
#


def load_population_maddison_series(
	country_code	: str,
	year_start		: int			= GDP_MADDISON_YEAR_START_DFLT,
	year_end		: int			= GDP_MADDISON_YEAR_END_DFLT,
	dataset_path	: str			= DS_POPULATION_MADDISON_PATH,
	data_type		: DsPopDataType = DsPopDataType.DEFAULT
) -> tuple[pd.Series, str]:
	"""Load population from Maddison Project Database.
	@param country_code: Mandatory country code (3-letter) to filter by.
	@param year_start: Starting year for the data
	@param year_end: Ending year for the data
	@param dataset_path: Path to the Maddison CSV file
	@param data_type: Type of transformation to apply (DEFAULT or LN_DIFF)
	@return: A pandas Series indexed by Year with population values and the country name.
	"""
	
	# Load the dataset, skipping the first 2 rows (metadata/regions)
	# Row 3 (index 2) contains the actual column names (year, country codes, etc)
	df = pd.read_csv(dataset_path, skiprows=2)
	
	# The first column is 'year' (or similar), and subsequent columns are country codes
	# Rename the first column to 'Year' if it's not already
	if 'year' in df.columns[0].lower():
		df = df.rename(columns={df.columns[0]: 'Year'})
	
	df = rename_df_columns_ioc_to_noc(df)
	
	# Filter for the specific country column
	if country_code not in df.columns:
		raise ValueError(f"Country code '{country_code}' not found in POP dataset.")
	
	# Extract year and country data
	population_data					= df[['Year', country_code]].copy()
	population_data['Year']			= pd.to_numeric(population_data['Year'], errors='coerce')
	population_data[country_code]	= pd.to_numeric(population_data[country_code], errors='coerce')
	
	# Remove rows with NaN values
	population_data = population_data.dropna()
	
	# Filter by year range
	population_data = population_data[(population_data['Year'] >= year_start) & (population_data['Year'] <= year_end)]
	
	# Create Series with Year as index
	population_series = pd.Series(
		population_data[country_code].values,
		index=population_data['Year'].astype(int).values,
		name='Population'
	)
	
	# Get country name from the first row metadata (optional, fallback to country code)
	country_name = country_code
	
	if data_type == DsPopDataType.LN:
		population_series = get_series_log(population_series)
	elif data_type == DsPopDataType.LN_DIFF:
		population_series = get_series_log_diff(population_series)
	
	return population_series, ioc_to_noc(country_name)


def load_population_extended_series(
	country_code	: str,
	year_start		: int			= GDP_MADDISON_YEAR_START_DFLT,
	year_end		: int			= GDPPC_PERC_WBOD_YEAR_LAST,
	dataset_path	: str			= DS_POPULATION_WBOD_PATH,
	data_type		: DsPopDataType = DsPopDataType.DEFAULT
) -> tuple[pd.Series, str]:
	"""Load population from Maddison (until 2022) and extend with WBOD data (2023-2024).
	@param country_code: Mandatory country code (3-letter) to filter by.
	@param year_start: Starting year for the data
	@param year_end: Ending year for the data (up to 2024)
	@param dataset_path: Path to the WBOD population CSV file
	@param data_type: Type of transformation to apply (DEFAULT or LN_DIFF)
	@return: A pandas Series indexed by Year with population values and the country name.
	"""
	
	# Load Maddison data (1800-2022)
	population_series, country_name = load_population_maddison_series(
		country_code=country_code,
		year_start=year_start,
		year_end=POPULATION_MADDISON_YEAR_LAST,
		data_type=DsPopDataType.DEFAULT  # Don't apply transformation yet
	)
	
	# If year_end <= 2022, just return the Maddison data
	if year_end <= POPULATION_MADDISON_YEAR_LAST:
		if data_type == DsPopDataType.LN:
			population_series = get_series_log(population_series)
		elif data_type == DsPopDataType.LN_DIFF:
			population_series = get_series_log_diff(population_series)
		return population_series, country_name
	
	# Load population data from WBOD for years 2023-2024
	df_wbod = pd.read_csv(dataset_path)

	df_wbod = rename_df_values_ioc_to_noc(df_wbod, 'Country Code')
	
	# Filter for specific country
	country_df = df_wbod[df_wbod['Country Code'] == country_code]
	
	if country_df.empty:
		# If no WBOD data available, just return Maddison data
		if data_type == DsPopDataType.LN:
			population_series = get_series_log(population_series)
		elif data_type == DsPopDataType.LN_DIFF:
			population_series = get_series_log_diff(population_series)
		return population_series, country_name
	
	country_data	= country_df.iloc[0]
	#last_pop_value	= population_series.iloc[-1]  # Last value from Maddison (2022)
	
	# Extend with WBOD data for years 2023 onwards
	extended_values	= dict(population_series)  # Convert to dict
	
	for year in range(POPULATION_MADDISON_YEAR_LAST + 1, year_end + 1):
		year_str = str(year)
		if year_str in country_data.index:
			pop_value = country_data[year_str]
			if pd.notna(pop_value):
				try:
					extended_values[year] = float(pop_value) / 1000.0
				except (ValueError, TypeError):
					pass
	
	# Create extended Series
	population_series = pd.Series(extended_values, name='Population')
	population_series = population_series.sort_index()
	
	if data_type == DsPopDataType.LN:
		population_series = get_series_log(population_series)
	elif data_type == DsPopDataType.LN_DIFF:
		population_series = get_series_log_diff(population_series)
	
	return population_series, country_name


def load_population_series(
	country_code	: str,
	year_start		: int			= GDP_MADDISON_YEAR_START_DFLT,
	year_end		: int			= GDP_MADDISON_YEAR_END_DFLT,
	dataset_path	: str			= DS_POPULATION_MADDISON_PATH,
	data_type		: DsPopDataType = DsPopDataType.DEFAULT
) -> tuple[pd.Series, str]:
	"""
	@param country_code: Mandatory country code to filter by.
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


def _get_hosting_schedule(
	medals_season		: str,
	year_start			: int	= MEDALS_FULL_YEAR_FIRST,
	year_end			: int	= MEDALS_FULL_YEAR_LAST,
	medals_dataset_path	: str	= DS_MEDALS_FULL_PATH
) -> pd.DataFrame:
	"""Get a schedule of which country hosted each Olympic year.
	@return: DataFrame indexed by Year with NOC column
	"""
	df = pd.read_csv(medals_dataset_path, usecols=['Year', 'Season', 'NOC', 'Is_Host'])
	
	# Filter by season
	if medals_season == 'S':
		df = df[df['Season'] == 'Summer']
	elif medals_season == 'W':
		df = df[df['Season'] == 'Winter']
	
	# Filter by year range
	df = df[(df['Year'] >= year_start) & (df['Year'] <= year_end)]
	
	# Filter years where Is_Host is True
	df = df[df['Is_Host'] == True]
	
	# Get unique years and their hosts
	hosts = df.groupby('Year')['NOC'].first().reset_index()
	hosts = hosts.set_index('Year')
	
	return hosts


def get_hosts_unique_list(
	medals_season		: str,
	year_start			: int	= MEDALS_FULL_YEAR_FIRST,
	year_end			: int	= MEDALS_FULL_YEAR_LAST,
	remove_boycott		: bool	= False
) -> list[str]:
	"""Get the list of unique host countries in the given season and year range."""
	hosts_df = _get_hosting_schedule(medals_season, year_start, year_end)
	if remove_boycott:
		hosts_df = hosts_df[~hosts_df.index.isin([YEAR_BOYCOTT_URS, YEAR_BOYCOTT_USA])]
	return hosts_df['NOC'].unique().tolist()


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
	country					: str,
	year_start				: int				= MEDALS_FULL_YEAR_FIRST,
	year_end				: int				= MEDALS_FULL_YEAR_LAST,
	medals_season			: str				= 'S',
	gdp_year_shift			: int				= 0,
	population_year_shift	: int				= 0,
	use_gdp_mean			: bool				= False,
	use_population_mean		: bool				= False,
	remove_boycott			: bool				= False,
	use_separate_host_vars	: bool				= False,
	use_separate_close_vars	: bool				= False,
	medals_data_type		: DsMedalsDataType	= DsMedalsDataType.DEFAULT,
	gdp_data_type			: DsGdpDataType		= DsGdpDataType.DEFAULT,
	population_data_type	: DsPopDataType		= DsPopDataType.DEFAULT,
	medals_dataset_path		: str				= DS_MEDALS_FULL_PATH,
	gdp_dataset_path		: str				= DS_GDPPC_MADDISON_PATH,
	population_dataset_path	: str				= DS_POPULATION_MADDISON_PATH
) -> tuple[pd.DataFrame, str]:
	"""Load Olympic medals, GDP per capita, and population data with year alignment/shift.
	@param country: Country code (NOC for medals, 3-letter for GDP and population)
	@param year_start: Starting year for medals data
	@param year_end: Ending year for medals data
	@param medals_season: Season of medals ('S' for Summer, 'W' for Winter, 'B' for Both)
	@param gdp_year_shift: Number of years to shift GDP backwards
	@param population_year_shift: Number of years to shift population backwards
	@param use_gdp_mean: Whether to use 4-year arithmetic mean of GDP
	@param use_population_mean: Whether to use 4-year arithmetic mean of population
	@param use_communist_bloc: Add a variable indicating whether the country is communist/was part of the communist bloc
	@param remove_boycott: Whether to remove years affected by boycotts (1980 and 1984)
	@param use_separate_host_vars: Whether to use separate binary variables for hosting, pre-hosting, and post-hosting instead of a single Is_Host variable
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
		DF_COL_MEDALS			: medals_df['Total_Medals'],
		DF_COL_AM_HISTORY		: medals_df[DF_COL_AM_HISTORY],
		DF_COL_GDP				: gdp_shifted.reindex(medals_df.index),
		DF_COL_POPULATION		: population_shifted.reindex(medals_df.index),
		DF_COL_IS_BOYCOTT_URS	: medals_df[DF_COL_IS_BOYCOTT_URS],
		DF_COL_IS_BOYCOTT_USA	: medals_df[DF_COL_IS_BOYCOTT_USA]
	})

	# Drop rows with NaN values
	merged_df = merged_df.dropna()


	# Load all Olympic years and their hosts
	hosting_schedule		= _get_hosting_schedule(medals_season, medals_dataset_path=medals_dataset_path)
	hosting_schedule_dict	= hosting_schedule['NOC'].to_dict()
	all_olympic_years		= sorted(hosting_schedule.index.tolist())
	col_olympic_years		= [y for y in all_olympic_years if year_start <= y <= year_end]

	# Add many new columns all at once, for performance reasons
	new_cols = {}

	# Handle hosting columns
	if use_separate_host_vars:
		# Add OG<year>, PRE<year>, POST<year> columns
		for olympic_year in col_olympic_years:
			og_col_name		= DF_COL_IS_HOST_OG_YEAR(	olympic_year)
			pre_col_name	= DF_COL_IS_HOST_PRE_YEAR(	olympic_year)
			post_col_name	= DF_COL_IS_HOST_POST_YEAR(	olympic_year)

			# OG: 1 if this country hosted that year
			new_cols[og_col_name] = (country == hosting_schedule.loc[olympic_year, 'NOC'] and (merged_df.index == olympic_year))
			
			# PRE: 1 if this country hosts next Olympics
			next_year_idx	= hosting_schedule.index.get_loc(olympic_year) + 1	# type: ignore
			next_host		= hosting_schedule.iloc[next_year_idx]['NOC'] if next_year_idx < len(hosting_schedule) else None
			new_cols[pre_col_name] = (country == next_host and (merged_df.index == olympic_year))
			
			# POST: 1 if this country hosted previous Olympics
			prev_year_idx	= hosting_schedule.index.get_loc(olympic_year) - 1	# type: ignore
			prev_host		= hosting_schedule.iloc[prev_year_idx]['NOC'] if prev_year_idx >= 0 else None
			#prev_host		= hosting_schedule.iloc[prev_year_idx]['NOC'] if prev_year_idx >= 0 and olympic_year != col_olympic_years[0] else None
			new_cols[post_col_name] = (country == prev_host and (merged_df.index == olympic_year))
	else:
		# Use original Is_Host column
		new_cols[DF_COL_IS_HOST] = medals_df.loc[merged_df.index, DF_COL_IS_HOST]

	# Handle close to host columns
	if use_separate_close_vars:
		for olympic_year in col_olympic_years:
			# IS_HOST_CLOSE: 1 if this country is close to the host country that year, but not the host itself
			host_country = hosting_schedule_dict.get(olympic_year)
			
			def is_host_close_year(group):
				return (country in group) and (host_country in group) and (country != host_country) and (merged_df.index == olympic_year)

			new_cols[DF_COL_IS_HOST_CLOSE_CENTER_YEAR(olympic_year)]	= is_host_close_year(CLOSE_GROUP_EU_CENTRAL)
			new_cols[DF_COL_IS_HOST_CLOSE_GMT1_YEAR(olympic_year)]		= is_host_close_year(CLOSE_GROUP_EU_GMT1)
			new_cols[DF_COL_IS_HOST_CLOSE_MAIN_YEAR(olympic_year)]		= is_host_close_year(CLOSE_GROUP_EU_MAIN)
			new_cols[DF_COL_IS_HOST_CLOSE_WEST_YEAR(olympic_year)]		= is_host_close_year(CLOSE_GROUP_EU_WEST)
			new_cols[DF_COL_IS_HOST_CLOSE_WIDE_YEAR(olympic_year)]		= is_host_close_year(CLOSE_GROUP_EU_WIDE)
	else:
		# IS_HOST_CLOSE: 1 if this country is close to the host country that year, but not the host itself
		# hosts in merged_df
		merged_years_host = merged_df.index.map(hosting_schedule_dict)

		def is_host_close(group):
			# The host for the current year is the one in the group, and current country is not it
			return (country in group) & (merged_years_host.isin(group)) & (~medals_df.loc[merged_df.index, DF_COL_IS_HOST])

		new_cols[DF_COL_IS_HOST_CLOSE_CENTER]	= is_host_close(CLOSE_GROUP_EU_CENTRAL)
		new_cols[DF_COL_IS_HOST_CLOSE_GMT1]		= is_host_close(CLOSE_GROUP_EU_GMT1)
		new_cols[DF_COL_IS_HOST_CLOSE_MAIN]		= is_host_close(CLOSE_GROUP_EU_MAIN)
		new_cols[DF_COL_IS_HOST_CLOSE_WEST]		= is_host_close(CLOSE_GROUP_EU_WEST)
		new_cols[DF_COL_IS_HOST_CLOSE_WIDE]		= is_host_close(CLOSE_GROUP_EU_WIDE)


	# Add Year Dummy Variables
	# Use ALL possible Olympic years to ensure column consistency across countries (and avoid NaN)
	# exclude the last year to avoid dummy variable trap (perfect multicollinearity): const already has its role
	for year in all_olympic_years[:-1]:
		new_cols[DF_COL_YEAR_DUMMY(year)] = (merged_df.index == year)

	#pd.get_dummies(df['Year'], drop_first=True)
	
	new_cols[DF_COL_IS_COMMUNIST] = country in COMMUNIST_BLOC_COUNTRIES

	# Join all new columns at once
	merged_df = pd.concat([merged_df, pd.DataFrame(new_cols, index=merged_df.index)], axis=1)

	# Optionally remove years affected by boycotts
	if remove_boycott:
		merged_df = merged_df[~merged_df.index.isin([YEAR_BOYCOTT_URS, YEAR_BOYCOTT_USA])]

	return merged_df, country_name



def load_stacked_countries(
	countries_list			: list[str]|None	= None,
	year_start				: int				= MEDALS_FULL_YEAR_FIRST,
	year_end				: int				= MEDALS_FULL_YEAR_LAST,
	medals_season			: str				= 'S',
	gdp_year_shift			: int				= 0,
	population_year_shift	: int				= 0,
	use_gdp_mean			: bool				= False,
	use_population_mean		: bool				= False,
	remove_boycott			: bool				= False,
	use_separate_host_vars	: bool				= False,
	use_separate_close_vars	: bool				= False,
	medals_data_type		: DsMedalsDataType	= DsMedalsDataType.DEFAULT,
	gdp_data_type			: DsGdpDataType		= DsGdpDataType.DEFAULT,
	population_data_type	: DsPopDataType		= DsPopDataType.DEFAULT,
	medals_dataset_path		: str				= DS_MEDALS_FULL_PATH,
	gdp_dataset_path		: str				= DS_GDPPC_MADDISON_PATH,
	population_dataset_path	: str				= DS_POPULATION_MADDISON_PATH,
	is_verbose				: bool				= True
) -> tuple[pd.DataFrame, str]:
	"""Load Olympic medals, GDP per capita, and population data with year alignment/shift.
	@param countries_list: List of country codes to filter (None or [] means all countries in the medals dataset)
	@param year_start: Starting year for medals data
	@param year_end: Ending year for medals data
	@param medals_season: Season of medals ('S' for Summer, 'W' for Winter, 'B' for Both)
	@param gdp_year_shift: Number of years to shift GDP backwards
	@param population_year_shift: Number of years to shift population backwards
	@param use_gdp_mean: Whether to use 4-year arithmetic mean of GDP
	@param use_population_mean: Whether to use 4-year arithmetic mean of population
	@param remove_boycott: Whether to remove years affected by boycotts (1980 and 1984)
	@param use_separate_host_vars: Whether to use separate binary variables for hosting, pre-hosting, and post-hosting instead of a single Is_Host variable
	@param medals_data_type: Type of transformation for medals (DEFAULT, LN_DIFF, PERCENTAGE)
	@param gdp_data_type: Type of transformation for GDP (DEFAULT, LN_DIFF)
	@param population_data_type: Type of transformation for population (DEFAULT, LN_DIFF)
	@param medals_dataset_path: Path to medals CSV
	@param gdp_dataset_path: Path to GDP CSV
	@param population_dataset_path: Path to population CSV
	@return: tuple of (DataFrame with aligned 'Medals', 'GDP', and 'Population' columns indexed by Olympics year, country_name)
	"""

	
	# In a panel regression, the DataFrame of each country is stacked on top of each other
	
	if is_verbose:
		print("\n--- Building Global Panel Dataset ---")
	all_countries_data	= []
	all_countries_names = []

	if countries_list is None or len(countries_list) == 0:
		countries_list = _get_all_countries_list(year_start, year_end)
		if is_verbose:
			print(f"Using all countries from medals dataset: {', '.join(countries_list)}")

	skipped_teams = []
	for noc in countries_list:
		try:
			country_df, country_name = load_medals_gdp_and_population_aligned(
				country					= noc,
				year_start				= year_start,
				year_end				= year_end,
				medals_season			= medals_season,
				gdp_year_shift			= gdp_year_shift,
				population_year_shift	= population_year_shift,
				use_gdp_mean			= use_gdp_mean,
				use_population_mean		= use_population_mean,
				remove_boycott			= remove_boycott,
				use_separate_host_vars	= use_separate_host_vars,
				use_separate_close_vars	= use_separate_close_vars,
				medals_data_type		= medals_data_type,
				gdp_data_type			= gdp_data_type,
				population_data_type	= population_data_type,
				medals_dataset_path		= medals_dataset_path,
				gdp_dataset_path		= gdp_dataset_path,
				population_dataset_path	= population_dataset_path
			)
			
			# Add the NOC column so we know who is who when we stack them
			country_df['NOC'] = noc
			
			# Add the DataFrame to our list
			all_countries_data.append(country_df)
			if is_verbose:
				print(f"Added {noc} to panel.")

			all_countries_names.append(country_name)
		except Exception as e:
			# Some small countries might not have GDP data in Maddison, skip them safely
			skipped_teams.append(noc)
			if is_verbose:
				print(f"Skipped {noc}: {e}")
		
	print(f"\nFinished loading data for {len(all_countries_data)} teams. Skipped {len(skipped_teams)} teams with missing data: {', '.join(skipped_teams)}")

	# Stack them all together into one giant "Long Format" DataFrame
	global_df = pd.concat(all_countries_data)

	# Prune empty separate host columns
	if use_separate_host_vars or use_separate_close_vars:
		host_cols = [c for c in global_df.columns if any(c.startswith(pre) for pre in ['OG', 'PRE', 'POST', 'CLOSE'])]
		# Keep only columns that have at least one True/1 value
		cols_to_drop = [c for c in host_cols if not global_df[c].any()]
		if cols_to_drop:
			global_df = global_df.drop(columns=cols_to_drop)
			if is_verbose:
				print(f"Dropped {len(cols_to_drop)} separate host columns with no data: {', '.join(cols_to_drop)}")

	# Reset index to convert Year from index to column (otherwise can't sort rows later)
	global_df = global_df.reset_index()
	if 'index' in global_df.columns:
		global_df = global_df.rename(columns={'index': 'Year'})

	# Sort by Country, then by Year (Crucial for the Pre/Post shift to work correctly)
	global_df = global_df.sort_values(by=['NOC', 'Year'])

	if is_verbose:
		print("\n--- Calculating Pre and Post Host Dummies ---")

	if not use_separate_host_vars:
		# Create Pre and Post using pandas groupby shift
		# shift(-1) looks at the NEXT row. shift(1) looks at the PREVIOUS row.
		global_df[DF_COL_IS_HOST_PRE]	= global_df.groupby('NOC')[DF_COL_IS_HOST].shift(-1).fillna(False).astype(bool)
		global_df[DF_COL_IS_HOST_POST]	= global_df.groupby('NOC')[DF_COL_IS_HOST].shift(1).fillna(False).astype(bool)

	# Clean up any remaining NaNs
	global_df = global_df.dropna()

	return global_df, '+'.join(all_countries_names)



def load_stacked_countries_medals(
	countries_list			: list[str]|None	= None,
	year_start				: int				= MEDALS_FULL_YEAR_FIRST,
	year_end				: int				= MEDALS_FULL_YEAR_LAST,
	medals_season			: str				= 'S',
	remove_boycott			: bool				= False,
	medals_data_type		: DsMedalsDataType	= DsMedalsDataType.DEFAULT,
	medals_dataset_path		: str				= DS_MEDALS_FULL_PATH,
	is_verbose				: bool				= True
) -> pd.DataFrame:
	"""Load Olympic medals, GDP per capita, and population data with year alignment/shift.
	@param countries_list: List of country codes to filter (None or [] means all countries in the medals dataset)
	@param year_start: Starting year for medals data
	@param year_end: Ending year for medals data
	@param medals_season: Season of medals ('S' for Summer, 'W' for Winter, 'B' for Both)
	@param remove_boycott: Whether to remove years affected by boycotts (1980 and 1984)
	@param medals_data_type: Type of transformation for medals (DEFAULT, LN_DIFF, PERCENTAGE)
	@param medals_dataset_path: Path to medals CSV
	@return: DataFrame
	"""

	
	# In a panel regression, the DataFrame of each country is stacked on top of each other
	
	if is_verbose:
		print("\n--- Building Global Panel Dataset ---")
	all_countries_data	= []

	if countries_list is None or len(countries_list) == 0:
		countries_list = _get_all_countries_list(year_start, year_end)
		if is_verbose:
			print(f"Using all countries from medals dataset: {', '.join(countries_list)}")

	skipped_teams = []
	for noc in countries_list:
		try:
			country_df = load_medals(
				country=noc,
				year_start=year_start,
				year_end=year_end,
				medals_season=medals_season,
				dataset_path=medals_dataset_path,
				data_type=medals_data_type
			)
			
			# Add the NOC column so we know who is who when we stack them
			country_df['NOC'] = noc
			
			# Add the DataFrame to our list
			all_countries_data.append(country_df)
			if is_verbose:
				print(f"Added {noc} to panel.")

		except Exception as e:
			# Some small countries might not have GDP data in Maddison, skip them safely
			skipped_teams.append(noc)
			if is_verbose:
				print(f"Skipped {noc}: {e}")
		
	print(f"\nFinished loading data for {len(all_countries_data)} teams. Skipped {len(skipped_teams)} teams with missing data: {', '.join(skipped_teams)}")

	# Stack them all together into one giant "Long Format" DataFrame
	global_df = pd.concat(all_countries_data)

	# Reset index to convert Year from index to column (otherwise can't sort rows later)
	global_df = global_df.reset_index()
	if 'index' in global_df.columns:
		global_df = global_df.rename(columns={'index': 'Year'})

	# Sort by Country, then by Year (Crucial for the Pre/Post shift to work correctly)
	global_df = global_df.sort_values(by=['NOC', 'Year'])

	if is_verbose:
		print("\n--- Calculating Pre and Post Host Dummies ---")

	# Clean up any remaining NaNs
	global_df = global_df.dropna()

	return global_df



def save_stacked_countries_to_csv(
	output_path				: str,
	countries_list			: list[str]|None	= None,
	year_start				: int				= MEDALS_FULL_YEAR_FIRST,
	year_end				: int				= MEDALS_FULL_YEAR_LAST,
	medals_season			: str				= 'S',
	gdp_year_shift			: int				= 0,
	population_year_shift	: int				= 0,
	use_gdp_mean			: bool				= False,
	use_population_mean		: bool				= False,
	remove_boycott			: bool				= False,
	use_separate_host_vars	: bool				= False,
	use_separate_close_vars	: bool				= False,
	medals_data_type		: DsMedalsDataType	= DsMedalsDataType.DEFAULT,
	gdp_data_type			: DsGdpDataType		= DsGdpDataType.DEFAULT,
	population_data_type	: DsPopDataType		= DsPopDataType.DEFAULT,
	is_verbose				: bool				= True
) -> None:
	"""Load stacked country data and save it to a CSV file.
	@param output_path: Path where the CSV file will be saved.
	@param ...: Other parameters are passed directly to load_stacked_countries.
	"""
	global_df, _ = load_stacked_countries(
		countries_list			= countries_list,
		year_start				= year_start,
		year_end				= year_end,
		medals_season			= medals_season,
		gdp_year_shift			= gdp_year_shift,
		population_year_shift	= population_year_shift,
		use_gdp_mean			= use_gdp_mean,
		use_population_mean		= use_population_mean,
		remove_boycott			= remove_boycott,
		use_separate_host_vars	= use_separate_host_vars,
		use_separate_close_vars	= use_separate_close_vars,
		medals_data_type		= medals_data_type,
		gdp_data_type			= gdp_data_type,
		population_data_type	= population_data_type,
		is_verbose				= is_verbose
	)
	
	# Identify columns to remove
	cols_to_remove = [
		DF_COL_IS_BOYCOTT_URS, 
		DF_COL_IS_BOYCOTT_USA, 
		DF_COL_AM_HISTORY
	]
	
	# Also remove all YEAR dummy columns (YEAR1896, YEAR1900, etc.)
	year_dummy_cols = [c for c in global_df.columns if is_dfCol_yearDummy(c)]
	cols_to_remove.extend(year_dummy_cols)
	
	# Drop existing columns safely
	global_df = global_df.drop(columns=[c for c in cols_to_remove if c in global_df.columns])
	
	global_df.to_csv(output_path, index=False)
	
	if is_verbose:
		print(f"Dataset successfully saved to {output_path}")



if __name__ == "__main__":
	
	noc_list = get_top_countries_by_medals(year_start=1900, n=40,
							medals_season='S', is_verbose=True)

	
	save_stacked_countries_to_csv(
		output_path				= 'dataset/generated_olympic-panel-dataset_med-perc.csv',
		is_verbose				= True,
		medals_data_type		= DsMedalsDataType.PERCENTAGE,
	)

