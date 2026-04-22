import os
import re
import sys



def summarize_directory(input_dir):
	summary_lines = []
	
	# Regex to match the starting part and the timestamp, catching the rest of the filename
	# Example: out_regression_20260422-112600_all_1964-2026_ZINB... -> all_1964-2026_ZINB...
	filename_pattern = re.compile(r'^.*?\d{8}-\d{6}_(.*?)\.txt$')
	
	# Regexes for parsing the log content
	lag_pattern	= re.compile(r'Granger causality test \(manual\) with lag (\d+):')
	r2_pattern	= re.compile(r'Pseudo R-squ\.:\s+([-\d\.]+)')
	ll_pattern	= re.compile(r'Log-Likelihood:\s+([-\d\.]+)')
	
	# Walk through the directory to find all .txt files
	for root, _, files in os.walk(input_dir):
		for file in files:
			if not file.endswith('.txt') or file == 'summary.txt':
				continue
				
			filepath = os.path.join(root, file)
			
			# Extract clean filename
			match = filename_pattern.search(file)
			if match:
				clean_name = match.group(1).replace('_', ' ')
			else:
				# Fallback if timestamp pattern wasn't found
				clean_name = file.replace('.txt', '').replace('_', ' ')
			
			try:
				with open(filepath, 'r', encoding='utf-8') as f:
					lines = f.readlines()
			except Exception as e:
				print(f"Error reading {file}: {e}")
				continue
			
			current_lag	= None
			current_r2	= None
			current_ll	= None
			
			for line in lines:
				# Look for the lag starting point
				lag_match = lag_pattern.search(line)
				if lag_match:
					current_lag = lag_match.group(1)
					# Reset metrics for the new lag
					current_r2 = None
					current_ll = None
					continue
				
				# Proceed to look for metrics only if we currently are inside a valid lag block
				if current_lag is not None:
					r2_match = r2_pattern.search(line)
					if r2_match:
						current_r2 = r2_match.group(1)
						
					ll_match = ll_pattern.search(line)
					if ll_match:
						current_ll = ll_match.group(1)
						
					# If we found both metrics for the current lag, save the row
					if current_r2 is not None and current_ll is not None:
						summary_lines.append({
							'name':	clean_name,
							'lag':	current_lag,
							'r2':	current_r2,
							'll':	current_ll
						})
						# Set lag to None to prevent duplicating metrics for the same lag block
						current_lag = None 
						
	if not summary_lines:
		print("No valid regression logs found in the specified directory.")
		return

	# Sort alphabetically by filename, then numerically by lag
	summary_lines.sort(key=lambda x: (x['name'], int(x['lag'])))
	
	# Determine fixed-width columns based on the longest filename for alignment
	max_name_len	= max(len(row['name']) for row in summary_lines)
	name_width		= max_name_len + 4  # Add a little padding buffer
	
	# Output file logic
	output_path = os.path.join(input_dir, 'summary.txt')
	
	with open(output_path, 'w', encoding='utf-8') as out_f:
		# Write column headers
		header = f"{'Filename'.ljust(name_width)} {'Lag'.ljust(8)} {'Pseudo R-squ.'.ljust(16)} {'Log-Likelihood'}\n"
		out_f.write(header)
		out_f.write("-" * (len(header) + 4) + "\n")
		
		# Write rows
		for row in summary_lines:
			# .ljust() handles exactly what you asked for: fixed length - string length spaces
			name_padded = row['name'].ljust(name_width)
			lag_padded  = f"lag-{row['lag']}:".ljust(8)
			r2_padded   = str(row['r2']).ljust(16)
			ll_str      = str(row['ll'])
			
			out_f.write(f"{name_padded} {lag_padded} {r2_padded} {ll_str}\n")
			
	print(f"Summary successfully saved to {output_path}")



if __name__ == '__main__':
	if len(sys.argv) < 2:
		print("Usage: python3 summarize_regression.py <path_to_out_directory>")
		sys.exit(1)
	
	input_directory = sys.argv[1]
	
	if not os.path.isdir(input_directory):
		print(f"Error: Directory '{input_directory}' does not exist.")
		sys.exit(1)
		
	summarize_directory(input_directory)