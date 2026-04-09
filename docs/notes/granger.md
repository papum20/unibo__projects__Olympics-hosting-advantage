# Granger Causality

## Prerequisiti

**(assenza di) fattori esterni - confounding variable**  
Una terza variabile che influenzi sia X che Y potrebbe falsare il test.  
Nel paper: discutere possibili confounding variable (presenza/assenza).  

**Serie stazionarie**  
**stazionaria** = media e varianza costanti nel tempo.  

Test di stazionarietà:
- "a occhio": non è rigoroso, dunque esistono metodi che ritornano un numero
- DF (Dickey-Fuller)
- ADF (Augmented Dickey-Fuller)

Misurare **ADF**:
* Calcola una statistica di un test (un numero); se è sotto una certa soglia, rifiuta l'ipotesi nulla (cioè, rifiuta che la serie ha una unit root), quindi è stazionaria (con molta probabilità).  
* Se la statistica è sopra la soglia, non ci sono abbastanza prove per rifiutare l'ipotesi nulla.  
* Dalla statistica, si calcola un p-value, con soglia di 0.05.  

**ADF** può segnare erroneamente come stazionaria una serie, se ci sono pochi punti (e.g. meno di `30`).  

### Fix per **GDP**  

_First Difference of the Natural Logarithm_ : `ln(GDP_t) - ln(GDP_{t-1})`  
idea: you are calculating the percentage growth rate from one period to the next. Economic growth rates are almost always stationary.  

### Fix per **Medals**  

Non si può applicare tale _differenza_, altrimenti si ottengono anche numeri negativi, quindi non si può applicare Zero-Inflated Negative Binomial (ZINB) model (regression) o Poisson model, perché progettati per _Count data_ (0, 1, 2, ...).  
Poi si dovrebbe usare OLS (Linear Regression), che, secondo il paper, non è adatto:
> Since most countries do not win any medals at the Olympics, there are a lot of zero observations in the sample 
> (see Fig. 2), which may bias the estimation using OLS. Previous studies used the Tobit estimator or 
> zero-inflated beta regression to manage the zero-observation problem. However, medal count can only be a 
> positive number, which indicates a Poisson or negative binomial  distribution. To account for both issues, zero-
> inflated Poisson (ZIP) or zero-inflated negative binomial (ZINB) models should be used.


If you look closely at **Equation 2** in the paper:
$$m_{i,j,t} = \alpha + \beta_1 d_{i,t} + \dots + \theta_t + \phi_j + \varepsilon_{i,j,t}$$

$\theta_t$ stands for **Olympic Games (Time) Fixed Effects**.  
In econometrics, if your variables have a common macroeconomic trend (like the fact that global GDP goes up every 4 years, or the fact that the IOC hands out more total medals today than they did in 1996), you can add a "dummy variable" for every single year in your dataset. 
By adding a dummy variable for 2000, 2004, 2008, etc., **the time fixed effects automatically absorb the non-stationarity caused by time trends.** It essentially detrends the data for you directly inside the regression. 

*"the issue of non-stationarity and global time-trends is resolved directly inside the model by the inclusion of Olympic Games (Time) Fixed Effects ($\theta_t$), which absorb macro-level shocks and trends."*


Non si può usare Granger?? `no-granger-on-medals_gemini.md`  

Se proprio lo vuoi usare, fai un'analisi separata, dunque abbandona gli altri modelli per questa sezione (ZINB) e normalizza la serie con qualche metodo.  
Su più olimpiadi possibile (circa 30).  

If you look at the whole history of the Olympics, the number of medals awarded has exploded (43 events in 1896 vs. 329 events in 2024). A country's medal count will naturally trend upward just because there are more medals to win.  
You have two great options to fix this:
*   **Option A: First Difference (The Standard Way):** Calculate the change in medals from the last Olympics. ($Medals_t - Medals_{t-1}$). 
*   **Option B: Medal Share (The Pro Econometric Way):** Instead of raw medals, calculate the **Percentage of Total Medals** the country won that year. (e.g., USA won 10% of all available medals in 1996). Medal share naturally controls for IOC inflation and is usually stationary.

**The "World War Gap" Trap**  
Before writing the code, you must handle a major time-series rule: **Time steps must be equal.**
The Olympics happen every 4 years, but they were cancelled in 1916, 1940, and 1944. If you leave these gaps in a standard time-series index, Granger Causality will calculate incorrectly. 
*The fix:* Treat the "Olympiad number" as the time index (1, 2, 3...) rather than the calendar year, skipping the cancelled years entirely, so the data is just a sequence of continuous games.

### Fix for 0/inf

`0`/`inf`/etc. with logs (error): do `ln(x + 1)` instead of `ln(x)`.  

#### How to Interpret the Output for your Project:

1.  **The ADF Output:** If both p-values are below 0.05, you have successfully proven to your professor that you transformed the data correctly and it is safe to run time-series models.
2.  **The Granger Output:** The test will print out $F$-tests and $\chi^2$ tests for Lag 1 and Lag 2. 
    *   If the p-value for Lag 1 is **< 0.05**, you can formally conclude: *"Historical data for Great Britain shows that an increase in GDP growth in the previous Olympic cycle Granger-causes an increase in medals won in the current Olympic cycle."*
    *   If the p-value is **> 0.05**, you conclude: *"Despite the visual correlation, changes in national GDP do not Granger-cause changes in medal counts over time for Great Britain."*

**Why this is an awesome addition to your paper:**
The original authors say, *"GDP is associated with medals."* But their model only looks at the data cross-sectionally (matching 2012 GDP with 2012 Medals). By adding a Granger Causality test on the historical data, you are answering a much cooler question: *"Does an economic boom today actually predict a sports boom four years from now?"*


## Tecniche

**GDP geometric mean over 4 years (previous 3)**:  
* like the paper

_Why the previous 3 years?_  
The Olympic cycle is called a "quadrennium" (a 4-year period). Government sports budgets, athlete training programs, and facility construction don't happen in a single year; they happen continuously over that 4-year cycle. By taking the average of all 4 years leading up to the Games, you capture the entire funding environment the athletes experienced while training.  
_Why a Geometric Mean instead of an Arithmetic (normal) average?_  
Because GDP compounds over time (like interest in a bank account). If a country has a massive economic crash one year but recovers the next, a standard arithmetic average gets skewed heavily by the extreme outlier. The geometric mean is mathematically designed for growth rates—it smooths out extreme 1-year spikes or crashes, giving you the "true" baseline wealth of the country over that 4-year period.  
(Bonus Math Fact: When you take the Natural Log (ln) of a Geometric Mean, it is mathematically identical to taking the normal average of the logs!)  

**OLS in più variabili (di controllo)**:  
* attraverso derivate parziali, si può capire l'effetto di una variabile (GDP) tenendo costante l'altra (host/boicottaggio)
* previene _Omitted Variable Bias (OVB)_: se ometti una variabile che influenza sia X che Y, potresti erroneamente attribuire a X tutto l'effetto di quella variabile omessa
* quindi, è diverso da fare 3 regressioni separate, perché tiene conto di tutte le variabili contemporaneamente, isolando l'effetto di ciascuna

## Relazione

Spiegare come funzionano le implementazioni usate, parametri usati etc. (eg ADF di libreria python statsmodels).  

Come fa il paper, mostrare 2 regressioni/modelli:
* `Medals ~ Host` o `Medals ~ Host + Boycott` : solo con _Host_ ritorna risultati positivi (basso p-value)
* `Medals ~ Host + Boycott + ln_GDP_4yr_mean` :  ma, aggiungendo le variabili di controllo, l'effetto di _Host_ scompare (alto p-value) e passa a _GDP_

## Ref

ritvikmath ADF:  
https://youtu.be/1opjnegd_hA?si=WVYPi6pPfQUSmg6g  
https://github.com/ritvikmath/Time-Series-Analysis  

Non letto:  
https://real-statistics.com/time-series-analysis/stochastic-processes/dickey-fuller-test/  
