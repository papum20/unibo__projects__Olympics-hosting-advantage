# Granger

## Prerequisisiti

Stazionarietà:
- **medaglie per paese**:
  - (tot): no
    - e.g. USA/ESP/ITA S/W (in realtà, alcune sì, come ITA S, ma così non basta)
  - **log differenced**: sì
    - tested: USA, ITA
  - **percentuale**: si
    - 
  - nota: a volte no, se consideri vecchie olimpiadi (pre-WW, soprattutto WW1), dove il Paese ospitante vinceva quasi tutte le medaglie, e poi tornava a vincerne pochissime in tutti gli altri anni
- **GDP**:
  - tot: no
    - e.g. USA, ITA
  - **growth rate (log differenced)**: sì
    - tested: USA, ITA
  - taken every 4 years (to do Granger with Olympics): no
  - **GDPpc (Madison)**: same
    - every 4 years: often yes, depends on the taken period
      - e.g. ITA up to 2020 no, but in 2020 there was a significant drop, and apparently ending like this makes it non-stationary


## Results

*Is_Communist* sempre significativo.  

```sh
python src/scripts/granger-causality/granger_medals_gdp.py -s S -n AUS AUT BRA CAN CHN ESP FRA FRG GBR GRC JPN KOR MEX URS USA --start-year 1961 --gdp-avg --pop-avg --sep-host --save
python src/scripts/granger-causality/granger_medals_gdp.py -s S -n AUS BRA CAN CHN ESP FRA FRG GBR GRC JPN KOR MEX URS USA --start-year 1961 --gdp-avg --pop-avg --sep-host --save
```
Risaltano solo OG, PRE e POST per degli anni straordinari (boicattaggi 1980 e 1984; USA 1996).  
GDP quasi 0.05 con lag 7, ma in realtà mai.  

```sh
python src/scripts/granger-causality/granger_medals_gdp.py -s S -n AUS AUT BRA CAN CHN ESP FRA FRG GBR GRC JPN KOR MEX RUS URS USA --start-year 1961 --gdp-avg --pop-avg --save
```
Host e GDP spesso significativi (host di più).  
Solo Host: `<0.05`, R-squared `~0.045`.  
Host + GDP: host `<0.05`, GDP no. R-squared `~0.055`.  
COMM: R-squared `+~0.12` (enorme impatto).  
Aggiungere GDP, e altre var, alla fine, insieme: R-squared `~0.22`, GDP `<0.05`.  
COMM + Host: R-squared `~0.16`.  
COMM + GDP: R-squared `~0.13`, GDP `<0.05`.  
`--gdp-tot` : non migliora (per teoria sotto su COMM), piuttosto peggiora (motivo per cui abbiamo introdotto GDPpc in primo luogo).  

Possibili spiegazioni:
* senza COMM (e POP, anche se influisce poco), GDP può essere mascherato da altre variabili
  * i Paesi COMM hanno alta POP, basso GDPpc, ma investono tanto in sport; alcuni paesi con alto GDPpc (e.g. SWI) non eccellono (anche per bassa POP)
    * quindi, GDPpc da solo non basta
  * chiamata _Suppressor Variable_ (possibilmente, anche _resolving Omitted Variable Bias_)

```sh
python src/scripts/granger-causality/granger_medals_gdp.py -s S -n ESP --start-year 1961 --gdp-avg --pop-avg --save
```
ESP: sia GDP che host.  

```sh
python src/scripts/granger-causality/granger_medals_gdp.py -s S -n FRA --start-year 1961 --gdp-avg --pop-avg --ctrl-vars  HOST  GDP COMM POP BOYCOTT PRE POST  --save
```
A volte, GDP `<0.05` e HOST no!  


### Lag

`2` spesso ottimo.  


## Parameters

Parameter - regression:  
> regression : {"c","ct","ctt","n"}  
> Constant and trend order to include in regression.  
> "c" ⁠:⁠ constant only (default).  
> "ct" ⁠:⁠ constant and trend.  
> "ctt" ⁠:⁠ constant, and linear and quadratic trend.  
> "n" ⁠:⁠ no constant, no trend.  

`ct` può tenere conto di un trend (e.g. GDP che cresce, ma nella sua crescita potrebbe essere costante); tuttavia, anche così è non stazionario (testato per default).  
