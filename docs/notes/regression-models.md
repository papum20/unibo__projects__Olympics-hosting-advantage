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


## Leggere risultati

OLS:  
https://www.geeksforgeeks.org/machine-learning/interpreting-the-results-of-linear-regression-using-ols-summary/  

Costanti in OLS: se p-value < 0.05, il dato non è significativo (quindi non leggere gli altri valori, come _coef_).  

## How to Interpret the Output for your Project:

1.  **The ADF Output:** If both p-values are below 0.05, you have successfully proven to your professor that you transformed the data correctly and it is safe to run time-series models.
2.  **The Granger Output:** The test will print out $F$-tests and $\chi^2$ tests for Lag 1 and Lag 2. 
    *   If the p-value for Lag 1 is **< 0.05**, you can formally conclude: *"Historical data for Great Britain shows that an increase in GDP growth in the previous Olympic cycle Granger-causes an increase in medals won in the current Olympic cycle."*
    *   If the p-value is **> 0.05**, you conclude: *"Despite the visual correlation, changes in national GDP do not Granger-cause changes in medal counts over time for Great Britain."*

**Why this is an awesome addition to your paper:**
The original authors say, *"GDP is associated with medals."* But their model only looks at the data cross-sectionally (matching 2012 GDP with 2012 Medals). By adding a Granger Causality test on the historical data, you are answering a much cooler question: *"Does an economic boom today actually predict a sports boom four years from now?"*

**Which statistic p-value to look at:**  
Look at the F-tests (ssr based F test & parameter F test).
Why? Chi-square (chi2) and Likelihood Ratio tests rely on "asymptotic theory," which means they only work correctly when you have a massive dataset (hundreds of rows). Because your df_denom (degrees of freedom) is only 2 (a tiny dataset), the Chi2 test breaks and gives you a False Positive (p=0.000)
The F-test is designed specifically for small samples.  



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

**Chi boicotta**:
* paper: 
  >Some countries have only participated in one Olympic competition, so using zero observations from all Olympic competitions would bias the analysis.
* quindi, lascia riga vuota, altrimenti influenzerebbe male (la regressione vedrebbe una correlazione con 0 medaglie, che non sono vere)


### Panel regression

Paper: per Paese per anno per sport.  
N_COUNTRIES x N_SPORTS x N_YEARS righe - ~12,000 observations.  

By zooming in on the sport level, they can control for the fact that a country might be historically amazing at Fencing but terrible at Judo. It also allowed them (in the text of the paper) to check if the "Host Advantage" is stronger in *subjectively judged* sports (like Gymnastics) compared to *objective* sports (like the 100m sprint), where a referee might be influenced by a cheering home crowd.  


### Dummy variable separate per ogni edizione

To analyze each specific Olympic Games individually, you literally create a separate column for **every single hosting event**. 

**Will you have tens of variables?**   
**Yes!** If you analyze 7 recent Summer Olympics (1996 to 2020), you will create:
*   7 `OG` (Host) variables
*   7 `Pre` variables
*   7 `Post` variables
This means you will add **21 new dummy variables** to your regression.

**Won't they interfere with each other?**  
**No, they won't, because of a concept called "Degrees of Freedom."**
In OLS regression, as long as your number of rows (observations) is much larger than your number of columns (variables), the math works perfectly. 
*   If you analyze 18 countries over 15 Olympics (1964 to 2024), you have **~270 rows**. 
*   Your model will have **~25 variables** (21 dummies + GDP, Pop, etc.).
Because 270 is much bigger than 25, the model has plenty of "degrees of freedom" to calculate everything without the variables tripping over each other. 

Furthermore, because `OG96` is only a `1` for the USA in 1996, and `OG12` is only a `1` for Great Britain in 2012, they are mathematically separate. They never overlap, so they cannot interfere with each other!

*(Econometric Note: When you create a dummy variable that is `1` for only a single row in the entire dataset, it is called an "Observation-Specific Dummy". It calculates the exact abnormal surplus of medals for that specific country in that specific year, adjusting for their GDP and Population!)*


### Dummy var per sport - Sport FE

**What do "OG FE" and "Sport FE" mean?**  
"FE" stands for **Fixed Effects**. This is one of the most powerful tools in panel data econometrics. 

A "Fixed Effect" is simply a **Dummy Variable** used to absorb structural, unchangeable differences between groups so they don't mess up your math. The "Yes" in the table just means: *"We added these dummy variables to the regression."*

Here is exactly what each one does:

**A. Sport FE (Sport Fixed Effects) = YES**
Imagine comparing Swimming to Soccer. 
*   In Swimming, Michael Phelps alone can win 8 medals. A country can easily win 30 swimming medals. 
*   In Soccer, a country can only win **1 medal** (the team medal). 
If the researchers didn't use Sport FE, the ZINB model would look at the data and say: *"Wow, the USA won 30 medals in Swimming and only 1 in Soccer. The USA must be 30 times better at Swimming than Soccer!"* 

By putting `Sport FE = Yes`, they added a dummy variable for every single sport (`Is_Swimming`, `Is_Soccer`, `Is_Judo`). The math then completely absorbs the size difference, essentially saying: *"We will judge a country's swimming performance ONLY against other swimming performances, not against soccer."*

### Dummy var per anno - OG FE

**B. OG FE (Olympic Games Fixed Effects) = YES**
This is the **Time Fixed Effect** we discussed a few messages ago! 
The IOC adds new sports and hands out more total medals every single Olympic cycle (e.g., 841 medals in 1996 vs. 1,080 medals in 2020). If a country's raw medal count goes up between 1996 and 2020, the model might accidentally think it's because their GDP went up. In reality, it's just because there are more medals available to win!

By putting `OG FE = Yes`, they added a dummy variable for every single year (`Is_1996`, `Is_2000`, `Is_2004`). These year dummies automatically absorb the "global inflation" of medals and any global economic recessions that affected every country at the exact same time.

#### How this relates to your project:
*   **Do you need Sport FE?** No! Because you grouped all your medals together into a single total per country (`N_COUNTRIES × N_YEARS`), the sports are already combined. You don't need Sport Fixed Effects.
*   **Do you need OG FE?** Because you smartly converted your dependent variable into **Medal Share (%)** rather than raw counts, you naturally defeated the medal inflation problem (10% of the medals in 1996 is mathematically equal to 10% in 2020). Therefore, adding Olympic Games Fixed Effects isn't strictly necessary for you, though adding year dummies is always a safe econometric practice to absorb global shocks! 

You have done an incredible job deconstructing this paper. You are reading the notation, the tables, and the methodology exactly how a PhD reviewer would.


### Year dummy

To add a "Year Dummy" (Time Fixed Effect), you create a new column for each year. If the row is from 1996, the `Year_1996` column gets a `1`, and all other year columns get a `0`. 

#### The "Dummy Variable Trap" (Perfect Multicollinearity)
If you have 15 Olympic Games in your dataset, you **cannot** add 15 Year columns. You must only add **14 columns**. You have to leave one year out.

**Why?**
Because you already have a `const` (Intercept) in your model! The Intercept acts as your baseline. 
If you include all 15 years, the computer's matrix algebra completely breaks (it literally divides by zero) because the sum of the year columns perfectly equals the Intercept column. 

**The Solution:** You drop the very first year (e.g., 1964). 
*   1964 becomes the hidden "Baseline" built into the Intercept.
*   The coefficient for the `Year_1968` column will tell you: *"Compared to 1964, how much did the global average change in 1968?"*

#### A beautiful nuance about your specific model:
The authors of the paper **desperately** needed Year Dummies because they used *Raw Medal Counts*. In 1960 there were ~400 medals. Today there are over 1,000. They needed the Year Dummies to absorb that massive global inflation.

But **you** are using **Medal Share (%)**. The total percentage of medals awarded in 1960 was exactly 100%. The total percentage of medals awarded in 2024 was exactly 100%. The pie never gets bigger! 
Because of this, Year Dummies won't change your model very much. However, adding them is still considered a "best practice" because it absorbs the fact that there are *more countries* competing today than in 1960, which slightly lowers the average share everyone gets.

#### How to code this automatically in Python
You do not need to write a massive `for` loop to create these. Pandas has a built-in function called `pd.get_dummies()` that does it instantly, and it even has a built-in parameter to avoid the Dummy Variable Trap!

You can just add these three lines of code right before you run your OLS:

```python
    # 1. Let Pandas generate all the Year columns automatically
    # drop_first=True automatically deletes the first year to avoid the Dummy Variable Trap!
    year_dummies = pd.get_dummies(global_df['Year'], prefix='Year', drop_first=True)
    
    # 2. Convert them from True/False to 1/0
    year_dummies = year_dummies.astype(int)
    
    # 3. Add them to your X predictors matrix
    X = pd.concat([X, year_dummies], axis=1)
    
    # Run your model as usual!
    model = sm.OLS(Y, X).fit()
    print(model.summary())
```


### Fix for 0/inf

`0`/`inf`/etc. with logs (error): do `ln(x + 1)` instead of `ln(x)`.  


### Sport-level non Participating countries

>We used data for countries with qualified athletes in the sport concerned. Some countries have only participated in one 
>Olympic competition, so using zero observations from all Olympic competitions would bias the analysis. 

Facendo un'analisi a livello di sport per sport (con la sua dummy var), vengono esclusi i Paesi che non hanno partecipato a quello sport in quell'anno (nessuna riga piuttosto che uno 0). Altrimenti, ci sarebbe un bias.  


### Confronto con risultati del paper

* confronto con risultati del paper  
* robust standard error (heteroskedasticity-consistent)
  * risolve il problema di quando i dati hanno diverse misure, per cui errori e varianze sarebbero diversi per i vari dati altrimenti
  * a occhio, non vedo differenze nei risultati
  
#### What are the numbers in the paper's tables?
Look at Table 1 in the paper. For the Baseline Total (Column 1), you see:
**Host**
**$0.467^{***}$**
**(0.0820)**

Here is exactly what this means:
*   **The Top Number ($0.467$):** This is the **Coefficient ($\beta$)**. Because the authors used a Zero-Inflated Negative Binomial (ZINB) model, this number represents a logarithmic multiplier. Mathematically, $e^{0.467} = 1.59$. This means hosting gives a country roughly a **59% boost** to their raw medal count compared to a normal year.
*   **The Stars ($^{***}$):** This is the **p-value**. Instead of writing out $p = 0.0002$, academics use stars as a shortcut.
    *   $^{***}$ means $p < 0.01$ (99% confident)
    *   $^{**}$ means $p < 0.05$ (95% confident)
    *   $^*$ means $p < 0.10$ (90% confident)
*   **The Number in Parentheses $(0.0820)$:** This is the **Standard Error (SE)**. It is the measure of uncertainty around the coefficient. (If you divide the coefficient by the standard error: $0.467 / 0.0820 = 5.69$, this gives you the $t$-statistic/ $z$-statistic, which is what generates the p-value!).

#### What does "Robust" Standard Errors mean?
In statistics, there is a strict rule called *Homoskedasticity*, which assumes the "error" or "noise" in your predictions is the same for every row in your dataset.

But think about the Olympics: 
*   If your model tries to predict medals for Malta, it might be wrong by 1 or 2 medals. 
*   If your model tries to predict medals for the USA, it might be wrong by 15 or 20 medals. 
Because the error size changes depending on the country, your data has **Heteroskedasticity**.

If you run a normal OLS, heteroskedasticity tricks the math into making the Standard Errors too small, which makes the p-values artificially low (giving you false positives). **"Robust" standard errors** use a mathematical correction (often called the Huber-White sandwich estimator) to widen the standard errors back to their true, honest size, fixing the false positives.

**How to do this in Python:**
You can easily make your OLS robust just like the paper by changing one line of code!
```python
# Instead of: model = sm.OLS(Y, X).fit()
# Do this:
model = sm.OLS(Y, X).fit(cov_type='HC3')  # HC3 is standard for robust errors
```

#### Are your numbers comparable to the paper's numbers?
**Direct numerical comparison? NO.**
You cannot compare your `Is_Host` coefficient of (for example) `0.678` to their `0.467`. 

**Why? Because your scales are completely different.**
*   **The Paper:** Predicts **Raw Medal Counts** (0, 1, 50, 100). Their ZINB model uses a logarithmic scale, so their coefficient means "+46.7% more medals."
*   **Your Model:** Predicts **Medal Share %** (0.0 to 100.0). Since you used OLS, your scale is linear. If your coefficient for `Is_Host` is `2.5`, it literally means: *"Hosting gives this country an extra 2.5% of the total medals available worldwide."*

**So, what CAN you compare?**
You compare the **Direction** and the **Significance (Stars)**! 

*   **Agreement:** If the paper says `Host` is positive and significant ($^{***}$) in the baseline model, and your `Is_Host` has a positive coefficient and $p < 0.01$, **you successfully replicated their baseline finding.**
*   **The Big Reveal:** If the paper says `Host` loses its stars (becomes insignificant) when GDP is added, and your `Is_Host` p-value suddenly jumps to $p = 0.448$ when you add your `ln_GDP` variable... **you have successfully proven the exact same econometric phenomenon using a completely different mathematical approach.**

If you write in your report: *"While the coefficients are on different scales (log-counts vs. linear percentages), the direction and statistical significance of the variables perfectly mirror the ZINB findings of the original paper,"* your professor will know you truly understand how econometrics works.


## Relazione

Spiegare come funzionano le implementazioni usate, parametri usati etc. (eg ADF di libreria python statsmodels).  

Come fa il paper, mostrare 2 regressioni/modelli:
* `Medals ~ Host` o `Medals ~ Host + Boycott` : solo con _Host_ ritorna risultati positivi (basso p-value)
* `Medals ~ Host + Boycott + ln_GDP_4yr_mean` :  ma, aggiungendo le variabili di controllo, l'effetto di _Host_ scompare (alto p-value) e passa a _GDP_


### Why does GDP causality appear and disappear (with more vars)
You noticed that GDP is significant from 1961, but not from 1991, and sometimes disappears when you add all the separated Host dummies. Here are the two econometric reasons why:

*   **Reason A: The "Variance Sponge" Effect:** When you run a model with the generic `Is_Host` variable, GDP has plenty of room to explain why medals go up. But when you add 20+ specific event variables (`OG92`, `Pre96`, `Post00`), you are saturating the model. Those specific dummies act like a sponge, soaking up all the variance in the data. With so many variables, the model starts to "overfit," leaving GDP with nothing left to explain, causing its p-value to spike.
*   **Reason B: The Post-1990 Economic Plateau:** Between 1961 and 1990, the global economy radically transformed. Countries went from poor to rich, and their medal shares followed. But from 1991 to 2024, the wealthy countries (USA, UK, France) mostly had stable, low GDP growth (~2% a year). Because their GDP stopped fluctuating wildly, it stopped being a dynamic predictor of medal spikes in the modern era.

### Should you merge URS->RUS and FRG->GER?
**NO. Do not merge them.** 

This is a classic time-series trap. Let’s look at the Soviet Union (URS):
*   In 1988, URS had a population of ~286 million (it included Ukraine, Belarus, Kazakhstan, etc.) and won 132 medals.
*   In 1996, Russia (RUS) had a population of ~148 million and won 63 medals.

If you merge them into a single "RUS" code, your dataset will show a catastrophic 50% drop in Population, GDP, and Medals overnight in 1992. Your OLS regression will completely freak out trying to calculate a slope for that crash.

**The Solution:** The beauty of Panel Data is that it is **Unbalanced**. You don't need to force a continuous history. 
*   Let `URS` be its own country that simply "dies" (disappears from the dataset) after 1988. 
*   Let `RUS` be a brand new country that is "born" in 1996. 
*   Because you have `Is_Communist = 1` for both of them, the model will inherently understand that they share the same state-sponsored sports culture, without ruining the GDP/Population math!

### How to structure your final project (Which results to present)

You have run so many amazing models. You do not need to show all of them. A perfect university paper tells a "story" by showing 3 specific models, side-by-side. 

I strongly recommend you present your results exactly in this order:

#### Step 1: The Global Baseline (The "Naive" Model)
*   **Setup:** Panel regression from 1964 to 2024.
*   **Variables:** `Is_Host` (the generic one), `Is_Communist`, and `Is_Boycott`. 
*   **What to say:** *"First, I ran a baseline model simulating public perception. The results show that the generic 'Host' variable is highly significant, leading to the common assumption that simply hosting the games guarantees a medal surplus. Additionally, the Communist Bloc dummy is highly significant, confirming the literature on state-sponsored sports dominance."*

#### Step 2: The Macroeconomic Control Model
*   **Setup:** Same as Step 1, but you add `ln_GDP` (Lagged or 4-year mean) and `ln_Population`.
*   **What to say:** *"However, when controlling for national wealth (GDP) and talent pool (Population), the strength of the generic 'Host' effect diminishes. This proves the core thesis: a large portion of the 'Host Advantage' is actually a 'Wealth Advantage'. Host nations are generally wealthy, and their underlying GDP drives the medals, not the event itself."*

#### Step 3: The Disaggregated "Specific Games" Model
*   **Setup:** Panel regression, but you remove the generic `Is_Host` and replace it with the specific `OG92`, `OG96`, `Pre12`, etc., variables.
*   **What to say:** *"Finally, to replicate the original paper's deeper findings, I disaggregated the host variable. The results reveal that the 'Host Effect' is not a universal rule. While countries like Spain (1992) or Great Britain (2012) show highly significant positive coefficients (meaning they truly overperformed their GDP), others do not. This confirms that the Host Effect is highly heterogeneous, dependent on specific national sports policies (like Spain's ADO program) rather than a guaranteed outcome."*



## Ref

ritvikmath ADF:  
https://youtu.be/1opjnegd_hA?si=WVYPi6pPfQUSmg6g  
https://github.com/ritvikmath/Time-Series-Analysis  

Non letto:  
https://real-statistics.com/time-series-analysis/stochastic-processes/dickey-fuller-test/  
