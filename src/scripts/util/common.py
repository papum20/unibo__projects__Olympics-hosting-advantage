from datetime import datetime
import os
import sys

import pandas as pd



LOG_REGRESSION_OUT_PATH = 'out/scripts/regression/'



class Logger():
	#def __init__(self, filename_tag=""):
	#	timestamp	= datetime.now().strftime("%Y%m%d-%H%M%S")
	#	log_file	= os.path.join(LOG_REGRESSION_OUT_PATH, f"out_regression_{timestamp}_{filename_tag}.txt")
	#	
	#	self.terminal   = sys.stdout
	#	self.log        = open(log_file, "w")

	def __init__(
		self,
		noc				: list[str]|None,
		year_start		: int,
		year_end		: int,
		reg_type		: str,
		cov_type		: str,
		use_gpd_avg		: bool,
		use_pop_avg		: bool,
		sep_host_vars	: bool,
		sep_close_vars	: bool,
		ctrl_vars		: list[str],
		tag=""
	):
		timestamp	= datetime.now().strftime("%Y%m%d-%H%M%S")
		noc_str		= '+'.join(noc) if noc else 'all'
		ctrl_str	= '+'.join(ctrl_vars)
		
		filename = (
			f"out_regression_{timestamp}_{noc_str}_"
			f"{year_start}-{year_end}_{reg_type}_{cov_type}_"
			f"gdp-avg-{use_gpd_avg}_pop-avg-{use_pop_avg}_"
			f"sep-host-{sep_host_vars}_sep-close-{sep_close_vars}_{ctrl_str}_{tag}.txt"
		)
		
		log_path = os.path.join(LOG_REGRESSION_OUT_PATH, filename)
	
		self.terminal   = sys.stdout
		self.log        = open(log_path, "w")

		print(f"Log file: {log_path}\n")

	def write(self, message):
		self.terminal.write(message)
		self.log.write(message)
		self.flush()

	def flush(self):
		# Needed for compatibility with some environments
		self.terminal.flush()
		self.log.flush()
		


#
# Output
#

def print_ds(data, name, verbose, n=5):
	if verbose:
		print(f"Loaded data for {name}:")
		# Ensure all columns and full width are shown even when piped/tee'd
		with pd.option_context('display.max_columns', None, 'display.width', None):
			print(data.to_string())
	else:
		print(f"Loaded data for {name} (tail {n}):")
		with pd.option_context('display.max_columns', None, 'display.width', None):
			print(data.tail(n).to_string())