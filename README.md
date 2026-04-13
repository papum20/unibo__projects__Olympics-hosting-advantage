# unibo__projects__Olympics-hosting-advantage
Project for the Human Data Science course at University of Bologna, year 2025-2026. A study on the advantage of hosting Olympics, using statistical tools.  

Gruppo 5.  


## Usage

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

python src/scripts/util/plot_medals.py S USA 1 1896 2026
python src/scripts/util/plot_gdp.py USA 1 1896 2026

python src/scripts/granger-causality/granger_medals_gdp.py -s S -n AUS BRA CHN ESP FRA GBR GRC JPN USA --start-year 1991 --gdp-avg --pop-avg --sep-host --save
python src/scripts/granger-causality/granger_medals_gdp.py -s S -n AUS BRA CAN CHN ESP FRA FRG GBR GRC JPN KOR MEX URS USA --start-year 1961 --gdp-avg --pop-avg --sep-host --save
```
