from datetime import datetime
from enum import Enum
import os
import sys

import pandas as pd



LOG_REGRESSION_OUT_PATH = 'out/scripts/regression/'
LOG_CHI_OUT_PATH		= 'out/scripts/chi_squared/'

class LoggerType(Enum):
	REGRESSION	= "regression",
	CHI_SQUARED	= "chi_squared"





class Logger():
	#def __init__(self, filename_tag=""):
	#	timestamp	= datetime.now().strftime("%Y%m%d-%H%M%S")
	#	log_file	= os.path.join(LOG_REGRESSION_OUT_PATH, f"out_regression_{timestamp}_{filename_tag}.txt")
	#	
	#	self.terminal   = sys.stdout
	#	self.log        = open(log_file, "w")

	ctrl_vars_str = {
		"HOST"			: "H",
		"AM"			: "M",
		"YEAR"			: "Y",
		"PRE"			: "Pr",
		"POST"			: "Po",
		"GDP"			: "G",
		"POP"			: "P",
		"COMM"			: "C",
		"BOYCOTT_URS"	: "B",
		"BOYCOTT_USA"	: "",
		"CLOSE_GMT1"	: "CG1",
		"CLOSE_WIDE"	: "Cwd",
		"CLOSE_MAIN"	: "CM",
		"CLOSE_WEST"	: "CW",
		"CLOSE_CENTER"	: "CC"
	}

	def __init__(
		self,
		logger_type		: LoggerType,
		noc				: list[str]|int|None,
		year_start		: int,
		year_end		: int,
		lag_min			: int	= 0,
		lag_max			: int	= 0,
		reg_type		: str	= "",
		cov_type		: str	= "",
		use_gpd_avg		: bool	= False,
		use_pop_avg		: bool	= False,
		gdp_type		: str	= "",
		pop_type		: str	= "",
		sep_host_vars	: bool	= False,
		sep_close_vars	: bool	= False,
		ctrl_vars		: list[str]|None = None,
		tag=""
	):
		timestamp	= datetime.now().strftime("%Y%m%d-%H%M%S")
		noc_str		= '+'.join(noc) if isinstance(noc, list) else f"top{noc}" if noc else 'all'
		ctrl_str	= '+'.join([self.ctrl_vars_str.get(var, var) for var in ctrl_vars]) if ctrl_vars else 'none'
		
		
		if logger_type == LoggerType.REGRESSION:
			filename = (
				f"out_{logger_type.value}_{timestamp}_{noc_str}_"
				f"{year_start}-{year_end}_l{lag_min}-{lag_max}_{reg_type}-{cov_type}_"
				f"gdp-{gdp_type}-avg{int(use_gpd_avg)}_pop{pop_type}-avg{int(use_pop_avg)}_"
				f"sep-host{int(sep_host_vars)}_sep-close{int(sep_close_vars)}_{ctrl_str}_{tag}.txt"
			)
			log_path = os.path.join(LOG_REGRESSION_OUT_PATH, filename)
		elif logger_type == LoggerType.CHI_SQUARED:
			filename = (
				f"out_{logger_type.value}_{timestamp}_{noc_str}_"
				f"{year_start}-{year_end}_"
				f"gdp-{gdp_type}-avg{int(use_gpd_avg)}_pop{pop_type}-avg{int(use_pop_avg)}_"
				f"{tag}.txt"
			)
			log_path = os.path.join(LOG_CHI_OUT_PATH, filename)
		else:
			raise ValueError(f"Unknown logger type: {logger_type}")

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