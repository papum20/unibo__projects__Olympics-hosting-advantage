import sys
sys.path.append('src/scripts/')

from statsmodels.tsa.stattools import adfuller

from util.plot_medals import load_medals_series, plot_medals



DS_PATH = 'dataset/country-medals-by-year.csv'
PLOT_OUT_PATH = 'out/plot/'



def print_usage():
	print("""
	   Usage:
		python granger_calculator.py <S|W|B> [NOC] [0|1]
		- S|W|B: flag to indicate the type of medals (Summer, Winter, or Both).
		- NOC: Optional country code (NOC) to filter by. If not provided, defaults to 'USA'.
		- 0|1: Optional flag to indicate whether save the plot to file (default 0)
	""")


def perform_adf_test(series):
	result = adfuller(series)
	print(f'ADF Statistic: {result[0]}')
	print(f'p-value: {result[1]}')
	


if __name__ == "__main__":
	import sys

	if len(sys.argv) <= 1:
		print_usage()
		sys.exit(1)
	
	# Get medals type from command line argument, default to 'S' (Summer)
	medals_type = sys.argv[1] if len(sys.argv) > 1 else 'S'
	if medals_type not in ['S', 'W', 'B']:
		print("Invalid medals type. Use 'S' for Summer, 'W' for Winter, 'B' for Both.")
		sys.exit(1)

	# Get NOC from command line argument, default to 'USA'
	noc = sys.argv[2] if len(sys.argv) > 2 else 'USA'
	
	# Get save_plot flag from command line argument, default to 0
	save_plot_flag = sys.argv[3] if len(sys.argv) > 3 else '0'
	if save_plot_flag not in ['0', '1']:
		print("Invalid save_plot flag. Use '0' for no save, '1' to save the plot.")
		sys.exit(1)


	# Load the medals series
	medals_series = load_medals_series(country=noc, medals_type=medals_type)
	print(f"Loaded medals series for {noc} (printing head):")
	print(medals_series.head())
	
	# Apply the ADF test function
	print(f"\nPerforming ADF test on {noc} medals series:")
	perform_adf_test(medals_series)

	# Plot the medals
	plot_medals(medals_series, noc, medals_type=medals_type, save=(save_plot_flag == '1'))
	