# DATA

## Our own

### country-medals-by-year.csv
Generato con `convert_athletes_to_countries.py`.  

### country-medals-by-year_missing_2018-2026.csv
Creato manualmente, per gli anni mancanti nel dataset (2018-2026).  
https://en.wikipedia.org/wiki/2018_Winter_Olympics_medal_table#Medal_table  
https://en.wikipedia.org/wiki/2020_Summer_Olympics_medal_table#Medal_table  
https://en.wikipedia.org/wiki/2022_Winter_Olympics_medal_table#Medal_table  
https://en.wikipedia.org/wiki/2024_Summer_Olympics_medal_table#Medal_table  
https://en.wikipedia.org/wiki/2026_Winter_Olympics_medal_table#Medal_table  

### hosts.csv

Creato manualmente (https://en.wikipedia.org/wiki/List_of_Olympic_Games_host_cities).  

## External

# maddison

Maddison Project Database provides information on comparative economic growth and income levels over the very long run.  
https://www.rug.nl/ggdc/historicaldevelopment/maddison/releases/maddison-project-database-2023  
Citation: MPD version 2023: Bolt, Jutta and Jan Luiten van Zanden (2024), "Maddison style estimates of the evolution of the world economy: A new 2023 update", Journal of Economic Surveys, 1–41. DOI: 10.1111/joes.12618”  

### rgiffin_athletes.csv

https://www.kaggle.com/datasets/heesoo37/120-years-of-olympic-history-athletes-and-results  
Dataset principale Olimpiadi, per ogni atleta.  

#### Content

The file athlete_events.csv contains 271116 rows and 15 columns. Each row corresponds to an individual athlete competing in an individual Olympic event (athlete-events). The columns are:
* ID - Unique number for each athlete
* Name - Athlete's name
* Sex - M or F
* Age - Integer
* Height - In centimeters
* Weight - In kilograms
* Team - Team name
* NOC - National Olympic Committee 3-letter code
* Games - Year and season
* Year - Integer
* Season - Summer or Winter
* City - Host city
* Sport - Sport
* Event - Event
* Medal - Gold, Silver, Bronze, or NA

#### Limitations

- 1896-2016
- for team sports, a country will appear with multiple athletes

### Exploratory Data Analysis

https://www.kaggle.com/code/joshuaswords/does-hosting-the-olympics-improve-performance  
Per exploratory data analysis.  

### worldBankOpenData_GDP_USD 
https://data.worldbank.org/  
World Bank Open Data  
GDP 1960-2025  
Columns: "Country Name","Country Code","Indicator Name","Indicator Code", years "1960"-"2025"  
"Data Source","World Development Indicators",  
"Last Updated Date","2026-02-24",  

