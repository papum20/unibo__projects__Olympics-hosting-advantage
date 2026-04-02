# Granger

## Prerequisisiti

Stazionarietà:
- medaglie per paese (tot): no
  - e.g. USA/ESP/ITA S/W (in realtà, alcune sì, come ITA S, ma così non basta)
- GDP: no
  - e.g. USA, ITA
- GDP growth rate (log differenced): sì
  - tested: USA, ITA


Parameter - regression:  
> regression : {"c","ct","ctt","n"}  
> Constant and trend order to include in regression.  
> "c" ⁠:⁠ constant only (default).  
> "ct" ⁠:⁠ constant and trend.  
> "ctt" ⁠:⁠ constant, and linear and quadratic trend.  
> "n" ⁠:⁠ no constant, no trend.  

`ct` può tenere conto di un trend (e.g. GDP che cresce, ma nella sua crescita potrebbe essere costante); tuttavia, anche così è non stazionario.  
