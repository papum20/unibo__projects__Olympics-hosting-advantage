# Chi Squared

1. test con tutti i Paesi, per dimostrare risultato generale
2. singoli Paese, per vedere chi beneficia, di preciso 

## Requisiti

Nessuna distribuzione assunta.  

Countable data: mai medie, percentuali, etc.  
Per non usare percentuali, in una colonna usi le vinte totali, nell'altra le perse totali.  

Cochran's rule (of thumb): For tables with more than a single degree of freedom, a minimum expected frequency of 5 can be regarded as adequate, although when there is only a single degree of freedom a minimum expected frequency of 10 is much safer.  

https://www.tandfonline.com/doi/full/10.1080/00031305.2017.1286260#d1e862:  
>Cochran's Rule is often quoted in a washed-down version, such as “For tables with more than a single degree of freedom, a minimum expected frequency of 5 can be regarded as adequate, although when there is only a single degree of freedom a minimum expected frequency of 10 is much safer” (Hays, Citation1973, p. 736).

## Metodo

Crea tabella:
|               | Won Medal | Did Not Win Medal |
|---------------|-----------|-------------------|
| Host          |     a     |         b         |
| Non-Host      |     c     |         d         |

not win = non vinte (per più precisione, solo per eventi in cui il Paese ha partecipato).  
Tutti sommati su tutti gli anni.  

Per più Paesi, somme di ognuno (sempre 2 righe in totale).  

### Risultati

Boost after hosting:  
Is this a problem?  
In academia, this is actually considered a good thing! It makes your test conservative. If your Chi-Squared test STILL finds a statistically significant Home Advantage despite the Away average being inflated by the legacy effect, your finding is incredibly strong and bulletproof.

### Punti aggiuntivi

* TODO: remove boycott - from both load and get hosts