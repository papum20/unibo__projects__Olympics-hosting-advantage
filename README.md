# unibo__projects__Olympics-hosting-advantage
Project for the Human Data Science course at University of Bologna, year 2025-2026. A study on the advantage of hosting Olympics, using statistical tools.  
Group 5.  

Paper/report: `docs/report.pdf`  

## Directory structure

* `dataset/`: where datasets are downloaded or generated
* `docs/`: documentation
	* `dataset/`: datasets info
	* `notes/`: notes
	* `references/`: bibliography
* `out/`: 
	* `plots/`: generated plots
	* `scripts/`: test scripts results
* `results/`: findings, in a written format or as outputs
	* `out/`: meaningful results outputs
* `src/`: source code
	* `paper/`: paper Latex
	* `scripts/`: 
		* `bash-utils/`: scripts to run tests, compile paper, etc.
		* `dataset/`: dataset generation or modification scripts
		* `regression-model/`: granger and regression models
		* `stationary_test/`: e.g. ADF
		* `util/`: python utils, e.g. to load datasets or do plots


## Usage

paper:
```bash
# compile
#./src/scripts/bash-util/paper-compile.sh [DIR=src/paper1/ [--save]]
./src/scripts/bash-util/paper-compile.sh src/paper2 --save
# count words
#./src/scripts/bash-util/paper-count-words.sh [DIR=src/paper1/]
./src/scripts/bash-util/paper-count-words.sh src/paper2/
```

chi-squared:
```bash
# help
python src/scripts/chi_squared/chi_squared_daniele.py --help

# one country
python src/scripts/chi_squared/chi_squared_daniele.py -s S -n GBR --start-year 1924 --end-year 2024 -v --show

# all hosts country
python src/scripts/chi_squared/chi_squared_daniele.py -s S --noc-hosts --start-year 1924 --end-year 2024 -v --show
```

regression models - usage:
```bash
python src/scripts/regression-model/regression_model.py --help
```
regression models - examples:
```bash
python src/scripts/regression-model/regression_model.py -s S -n AUS BRA CHN ESP FRA GBR GRC JPN USA --start-year 1991 --gdp-avg --pop-avg --sep-host --save
python src/scripts/regression-model/regression_model.py -s S -n AUS BRA CAN CHN ESP FRA FRG GBR GRC JPN KOR MEX URS USA --start-year 1961 --gdp-avg --pop-avg --sep-host --save
python3 -u src/scripts/regression-model/regression_model.py --start-year 1960 --save --gdp-avg --pop-avg  --sep-host --reg-zinb --reg-hc3 --ctrl-vars GDP POP HOST PRE POST COMM BOYCOTT --log
python src/scripts/regression-model/regression_model.py -s S -n ESP --start-year 1961 --gdp-avg --pop-avg --save
```

stationary tests:
```bash
# Default (USA, Summer, 1896-2026)
python src/scripts/stationary_test/adf_medals.py
# Specific country, Winter Olympics
python src/scripts/stationary_test/adf_medals.py --season W --noc CHN
# Custom year range and save plots
python src/scripts/stationary_test/adf_medals.py --season S --noc GBR --start-year 1960 --end-year 2020 --save
# Skip certain analyses
python src/scripts/stationary_test/adf_medals.py --noc USA --skip-log-diff --skip-percentage
# Both seasons, specific country, save
python src/scripts/stationary_test/adf_medals.py -s B -n FRA --save
# Help
python src/scripts/stationary_test/adf_medals.py --help
# (same as for medals)
python src/scripts/stationary_test/adf_gdp.py USA --help
```

plots:
```bash
python src/scripts/util/plot_medals.py S USA 1 1896 2026
python src/scripts/util/plot_gdp.py USA 1 1896 2026
```

`src/scripts/bash-util/run-regression2.sh`: example of running many tests.   
