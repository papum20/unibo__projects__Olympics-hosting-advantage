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


Parameter - regression:  
> regression : {"c","ct","ctt","n"}  
> Constant and trend order to include in regression.  
> "c" ⁠:⁠ constant only (default).  
> "ct" ⁠:⁠ constant and trend.  
> "ctt" ⁠:⁠ constant, and linear and quadratic trend.  
> "n" ⁠:⁠ no constant, no trend.  

`ct` può tenere conto di un trend (e.g. GDP che cresce, ma nella sua crescita potrebbe essere costante); tuttavia, anche così è non stazionario (testato per default).  
