# Granger Causality

## Prerequisiti

Serie stazionarie.  
**stazionaria** = media e varianza costanti nel tempo.  

Test di stazionarietà:
- DF (Dickey-Fuller)
- ADF (Augmented Dickey-Fuller)

Misurare ADF:
Calcola una statistica di un test (un numero); se è sotto una certa soglia, rifiuta l'ipotesi nulla (cioè, rifiuta che la serie ha una unit root), quindi è stazionaria (con molta probabilità).  
Se la statistica è sopra la soglia, non ci sono abbastanza prove per rifiutare l'ipotesi nulla.  
Dalla statistica, si calcola un p-value, con soglia di 0.05.  

## Relazione

Spiegare come funzionano le implementazioni usate, parametri usati etc. (eg ADF di libreria python statsmodels).  

## Ref

ritvikmath ADF:  
https://youtu.be/1opjnegd_hA?si=WVYPi6pPfQUSmg6g  
https://github.com/ritvikmath/Time-Series-Analysis  

Non letto:  
https://real-statistics.com/time-series-analysis/stochastic-processes/dickey-fuller-test/  
