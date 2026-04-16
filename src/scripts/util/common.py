
def print_ds(data, name, verbose, n=5):
	if verbose:
		print(f"Loaded series for {name}:")
		print(data)
	else:
		print(f"Loaded series for {name} (tail {n}):")
		print(data.tail(n))
