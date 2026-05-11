import pandas as pd
import numpy as np
from scipy.stats import chisquare

# Caricamento dati
df = pd.read_csv('generated_olympic-panel-dataset.csv')

# Filtra anni rilevanti e pulisci dati mancanti
df_filtered = df[(df['Year'] >= 1924) & (df['Year'] <= 2024)].copy()
df_filtered['Medals'] = df_filtered['Medals'].fillna(0)

# Identifica anni olimpici validi (dove sono state assegnate medaglie)
olympic_years = df_filtered.groupby('Year')['Medals'].sum()
olympic_years_actual = olympic_years[olympic_years > 0].index.tolist()

# Estrai i paesi che hanno ospitato almeno una volta
host_nocs = df_filtered[df_filtered['Is_Host'] == True]['NOC'].unique()

results = []

# Analizza ogni paese che ha ospitato
for noc in host_nocs:
    # Filtra dati del paese negli anni olimpici
    subset = df_filtered[(df_filtered['NOC'] == noc) &
                         (df_filtered['Year'].isin(olympic_years_actual))]

    # Separa partecipazioni e medaglie per ospitalità
    n_h = len(subset[subset['Is_Host'] == True])        # N partecipazioni quando ospita
    n_nh = len(subset[subset['Is_Host'] == False])      # N partecipazioni quando non ospita
    m_h = subset[subset['Is_Host'] == True]['Medals'].sum()      # Medaglie totali quando ospita
    m_nh = subset[subset['Is_Host'] == False]['Medals'].sum()    # Medaglie totali quando non ospita

    m_total = m_h + m_nh      # Medaglie totali
    n_total = n_h + n_nh      # Partecipazioni totali

    # Calcola frequenze ATTESE (ipotesi nulla: ospitalità non influisce)
    # Se ospitalità non conta, le medaglie dovrebbero distribuirsi proporzionalmente alle partecipazioni
    e_h = m_total * (n_h / n_total)
    e_nh = m_total * (n_nh / n_total)

    # VERIFICA VALIDITÀ CHI-QUADRATO
    # Il test è affidabile solo se frequenze attese >= 5
    chi_valid = (e_h >= 5) and (e_nh >= 5)
    warning = None
    # Cochran's rule (of thumb):
    # For tables with more than a single degree of freedom,
    # a minimum expected frequency of 5 can be regarded as adequate,
    # although when there is only a single degree of freedom
    # a minimum expected frequency of 10 is much safer

    if not chi_valid:
        warning = "⚠️ Frequenze attese < 5: risultati non affidabili (poche medaglie o partecipazioni sbilanciate)"

    # Esegui test chi-quadrato comunque (come richiesto)
    if n_total > 0 and m_total > 0 and n_h > 0 and n_nh > 0:
        chi_stat, chi_p = chisquare([m_h, m_nh], f_exp=[e_h, e_nh])
    else:
        chi_p = None

    # Salva risultati
    results.append({
        'Paese': noc,
        'Nr. host': n_h,
        'Nr. non host': n_nh,
        'tot medaglie': m_total,
        'Med host': round(m_h, 2),
        'Med attese host': round(e_h, 2),
        'Med non host': round(m_nh, 2),
        'Med attese non host': round(e_nh, 2),
        'P Value': round(chi_p, 4) if chi_p else None,
        'Risultati': chi_p < 0.05 if chi_p else None,
        'Avviso': warning
    })

# Crea dataframe e ordina per p-value
results_df = pd.DataFrame(results).sort_values(by='P Value', na_position='last')
print(results_df.to_string())
