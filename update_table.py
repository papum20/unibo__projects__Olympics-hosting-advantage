import re

stats_data = """
OG1932                12.6129      0.665     18.972      0.000      11.310      13.916
PRE1932                0.8963      0.448      2.001      0.045       0.018       1.774
POST1932               0.3689      0.412      0.895      0.371      -0.439       1.177
"""

def get_stars(p):
    if p < 0.01: return "***"
    if p < 0.05: return "**"
    if p < 0.1: return "*"
    return ""

def parse_stats(data):
    results = {}
    for line in data.strip().split('\n'):
        parts = line.split()
        if len(parts) < 5: continue
        var = parts[0]
        coef = float(parts[1])
        p_val = float(parts[4])
        stars = get_stars(p_val)
        results[var] = f"{coef:.3f}{stars}"
    return results

mapping = parse_stats(stats_data)
file_path = "src/paper/results_regression.tex"

with open(file_path, 'r') as f:
    lines = f.readlines()

new_lines = []
for line in lines:
    row_updated = False
    for var, value in mapping.items():
        if line.strip().startswith(var) and "&" in line:
            parts = line.split("&")
            # The structure is currently: Var & Csurilla & ZINB All & ZINB Top 40 & OLS Base & OLS w/ AM & OLS w/ AM w/o YEAR
            # We want to fill the 5th and 6th columns (indices 4 and 5) which are currently often empty or hold other values.
            # Looking at the file, OG1932 usually doesn't exist.
            pass
            
    new_lines.append(line)

# Let's actually find where to insert the 1932 rows if they are missing.
# Or if they exist but are empty.
# I will check if they are in the file first.
