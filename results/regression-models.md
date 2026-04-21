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


## Tests/comparisons

Boycott sempre con 1964, se non YEAR.  

AM+Host: GDP+POP+COMM vs None.  
AM+Host+Year: GDP+POP+COMM vs None.  
AM+Host sep-host: GDP+POP+COMM vs None.  

AM+Host+Pre+Post: GDP+POP+COMM vs None.  
AM+Host+Pre+Post sep-host: GDP+POP+COMM vs None.  

CLOSE:
AM+Host+Pre+Post+Year: GDP+POP+COMM vs None.  
AM+Host+Pre+Post+Year sep-host: GDP+POP+COMM vs None.  
AM+Host+Pre+Post+Year sep-close: GDP+POP+COMM vs None.  
AM+Host+Pre+Post+Year sep-host sep-close: GDP+POP+COMM vs None.  



## Results

*Is_Communist* sempre significativo.  

```sh
python src/scripts/regression-model/regression_model.py -s S -n AUS AUT BRA CAN CHN ESP FRA FRG GBR GRC JPN KOR MEX URS USA --start-year 1961 --gdp-avg --pop-avg --sep-host --save
python src/scripts/regression-model/regression_model.py -s S -n AUS BRA CAN CHN ESP FRA FRG GBR GRC JPN KOR MEX URS USA --start-year 1961 --gdp-avg --pop-avg --sep-host --save
```
Risaltano solo OG, PRE e POST per degli anni straordinari (boicattaggi 1980 e 1984; USA 1996).  
`nonrobust`: GDP quasi 0.05 con lag 7, ma in realtà mai.  
`hc0`: GDP a volte si, a volte no per poco.  

```sh
python src/scripts/regression-model/regression_model.py -s S -n AUS AUT BRA CAN CHN ESP FRA FRG GBR GRC JPN KOR MEX RUS URS USA --start-year 1961 --gdp-avg --pop-avg --save
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
python src/scripts/regression-model/regression_model.py -s S -n ESP --start-year 1961 --gdp-avg --pop-avg --save
```
ESP: sia GDP che host.  

```sh
python src/scripts/regression-model/regression_model.py -s S -n FRA --start-year 1961 --gdp-avg --pop-avg --ctrl-vars  HOST  GDP COMM POP BOYCOTT PRE POST  --save
```
A volte, GDP `<0.05` e HOST no!  


### Lag

`2` spesso ottimo.  

### Cov type

`HC3` troppo aggressivo con OLS, quindi usare `HC0` per robustness. Con ZINB ok.  


### All countries

Panel regression su tutti* (eccetto gli esclusi...).  
ZINB, ovviamente.  
ZINB richiede nessuna colonna vuota:
* rimuovere Boycott, se quegli anni non inclusi
* rimuovere PRE2024 (non esiste) - già rimosso di default

>Why fewer hosts are significant in OLS than ZINB: ZINB evaluates the jump from 0 to 5 medals (a massive mathematical leap for a small country). OLS evaluates the jump from 2% to 3% of the global medal share. ZINB is much more sensitive to "breakout" performances by smaller host nations, which is why more Host dummies light up in that model.  

**LOG-DIFF**: con `Year` dummy, matrice singolare. Bisogna usare `LOG` (per GDP e POP).  
* singolare = probabilmente collinearità perfetta, o quasi. Forse perché i log-diff hanno meno variabilità

**YEAR**: con `sep-host` spesso singolare, quindi non si possono analizzare insieme...  
* tipo, no se aggiungi altre var (`GDP`, etc.)

**AM**: in realtà, è quasi sempre questo il motivo per matrice singolare
* predice troppo le medaglie
  * soprattutto per i tanti Paesi con 0 medaglie (predizione perfetta)
* nel paper forse funziona meglio perché diviso per sport non è esattamente 0
* VIF leggermente più alto (1.3-1.5, contro le altre var con 1-1.1, eccetto quelle tipo GDP POP CLOSE_*)

Host Pre Post sep-host: singolare.  

#### 1996

```sh
python3 -u src/scripts/regression-model/regression_model.py --start-year 1996 --save --gdp-avg --pop-avg  --sep-host --reg-zinb --reg-hc3 --ctrl-vars GDP POP HOST PRE POST COMM --log
```

**POP** sempre molto significativo:
* probabilmente, perché c'è una marea di Paesi piccoli e molto piccoli che sono molto scarsi

**GDP**: significativo solo con lag 1  
**COMM**: sempre significativo  

##### nonrobust

Host, PRE e POST: mai significativi  

##### HC3

Host, PRE e POST:
* sempre significativi
* tranne POST2008 (Grecia, che avuto la crisi)

HC3: cambiamento atteso, data heteroskedasticity  

#### 1964

```sh
python3 -u src/scripts/regression-model/regression_model.py --start-year 1964 --save --gdp-avg --pop-avg  --sep-host --reg-zinb --reg-hc3 --ctrl-vars GDP POP HOST PRE POST COMM --log
```

Comm, POP: sempre  
Host Pre Post:
* sempre
* eccetto post2008, di nuovo, e pre1988 (ESP ha avuto boom solo in 1992)
GDP:
* no
* migliora sempre con lag, e con lag `7` sì
sep-host: no diff.  

##### Boycott

Non cambia alcun risultato.  
Solo Pseudo R-sq passa da ~0.0195 a ~0.0205.  
Probabilmente perché ora ci sono tanti Paesi, e Boycott è significativa solo per pochi.  
>Furthermore, once you add Year Dummies (Time Fixed Effects) to fix the medal inflation issue, those Year Dummies will completely absorb the 1980 and 1984 boycotts anyway! The math will say, "1980 was a weird year for everyone," and the Is_Boycott variable becomes redundant.  

#### 1960

```sh
python3 -u src/scripts/regression-model/regression_model.py --start-year 1960 --save --gdp-avg --pop-avg  --sep-host --reg-zinb --reg-hc3 --ctrl-vars GDP POP HOST PRE POST COMM BOYCOTT --log
```

come 1964  

#### 1952

```sh
python3 -u src/scripts/regression-model/regression_model.py --start-year 1952 --save --gdp-avg --pop-avg  --sep-host --reg-zinb --reg-hc3 --ctrl-vars GDP POP HOST PRE POST COMM BOYCOTT --log
```

risp. a 1964, GDP più significativo, già <0.05 a lag 3.  


## Parameters

Parameter - regression:  
> regression : {"c","ct","ctt","n"}  
> Constant and trend order to include in regression.  
> "c" ⁠:⁠ constant only (default).  
> "ct" ⁠:⁠ constant and trend.  
> "ctt" ⁠:⁠ constant, and linear and quadratic trend.  
> "n" ⁠:⁠ no constant, no trend.  

`ct` può tenere conto di un trend (e.g. GDP che cresce, ma nella sua crescita potrebbe essere costante); tuttavia, anche così è non stazionario (testato per default).  
