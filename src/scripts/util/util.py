
def print_ds(series, series_name, verbose):
	if verbose:
		print(f"Loaded series for {series_name}:")
		print(series)
	else:
		print(f"Loaded series for {series_name} (tail):")
		print(series.tail())
