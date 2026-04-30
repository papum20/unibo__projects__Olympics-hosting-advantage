import re

d1 = """
const                 -7.9340      1.292     -6.142      0.000     -10.466      -5.402
Avg_Medals_History     0.4625      0.029     16.061      0.000       0.406       0.519
GDP                    0.2497      0.068      3.664      0.000       0.116       0.383
Population             0.6241      0.076      8.185      0.000       0.475       0.773
Is_Communist           0.6953      0.202      3.446      0.001       0.300       1.091
YEAR1996               0.3839      0.294      1.305      0.192      -0.192       0.960
YEAR2000               0.2220      0.297      0.748      0.455      -0.360       0.804
YEAR2004               0.0904      0.282      0.320      0.749      -0.463       0.643
YEAR2008               0.0242      0.256      0.095      0.925      -0.477       0.526
YEAR2012              -0.0457      0.253     -0.181      0.856      -0.541       0.449
YEAR2016              -0.0236      0.241     -0.098      0.922      -0.495       0.448
YEAR2020              -0.0480      0.260     -0.185      0.854      -0.557       0.461
OG1996                 0.3544      0.464      0.764      0.445      -0.554       1.263
OG2000                 4.2012      0.222     18.890      0.000       3.765       4.637
OG2004                 0.1602      0.195      0.822      0.411      -0.222       0.542
OG2008                 5.1860      0.408     12.716      0.000       4.387       5.985
OG2012                 2.2818      0.195     11.711      0.000       1.900       2.664
OG2016                -0.4034      0.215     -1.881      0.060      -0.824       0.017
OG2020                 2.1087      0.224      9.428      0.000       1.670       2.547
OG2024                 1.9130      0.218      8.764      0.000       1.485       2.341
PRE1996                2.7649      0.225     12.303      0.000       2.324       3.205
PRE2000               -0.2550      0.210     -1.214      0.225      -0.667       0.157
PRE2004                1.7441      0.459      3.799      0.000       0.844       2.644
PRE2008                0.4562      0.201      2.270      0.023       0.062       0.850
PRE2012               -0.5113      0.241     -2.120      0.034      -0.984      -0.039
PRE2016                0.9625      0.192      5.026      0.000       0.587       1.338
PRE2020               -1.1370      0.199     -5.723      0.000      -1.526      -0.748
POST1996               0.3025      0.245      1.236      0.217      -0.177       0.782
POST2000              -1.5731      0.429     -3.663      0.000      -2.415      -0.731
POST2004               3.3176      0.206     16.121      0.000       2.914       3.721
POST2008              -1.1174      0.183     -6.108      0.000      -1.476      -0.759
POST2012               3.5654      0.417      8.559      0.000       2.749       4.382
POST2016               2.3512      0.185     12.677      0.000       1.988       2.715
POST2020              -0.4222      0.247     -1.707      0.088      -0.907       0.063
POST2024               0.9517      0.235      4.056      0.000       0.492       1.412
"""

d2 = """
const                  0.7003      0.216      3.241      0.001       0.277       1.124
Avg_Medals_History     0.6132      0.023     26.261      0.000       0.567       0.659
YEAR1996               0.2518      0.356      0.706      0.480      -0.447       0.950
YEAR2000               0.1218      0.355      0.343      0.732      -0.574       0.818
YEAR2004              -0.0615      0.331     -0.186      0.853      -0.710       0.587
YEAR2008              -0.0860      0.293     -0.293      0.769      -0.660       0.488
YEAR2012              -0.1720      0.295     -0.584      0.559      -0.749       0.405
YEAR2016              -0.0751      0.280     -0.268      0.789      -0.624       0.474
YEAR2020              -0.0772      0.309     -0.250      0.803      -0.682       0.528
OG1996                -0.5754      0.516     -1.115      0.265      -1.587       0.436
OG2000                 4.0760      0.278     14.652      0.000       3.531       4.621
OG2004                -0.3718      0.244     -1.521      0.128      -0.851       0.107
OG2008                 7.8972      0.195     40.451      0.000       7.515       8.280
OG2012                 2.3247      0.232     10.016      0.000       1.870       2.780
OG2016                 0.9562      0.167      5.721      0.000       0.629       1.284
OG2020                 3.0483      0.216     14.110      0.000       2.625       3.472
OG2024                 2.0312      0.253      8.039      0.000       1.536       2.526
PRE1996                2.6279      0.280      9.371      0.000       2.078       3.178
PRE2000               -0.9005      0.279     -3.231      0.001      -1.447      -0.354
PRE2004                4.4672      0.246     18.157      0.000       3.985       4.949
PRE2008                0.4658      0.227      2.051      0.040       0.021       0.911
PRE2012                0.9015      0.189      4.772      0.000       0.531       1.272
PRE2016                1.9318      0.172     11.239      0.000       1.595       2.269
PRE2020               -1.0189      0.244     -4.184      0.000      -1.496      -0.542
POST1996               0.8383      0.277      3.023      0.003       0.295       1.382
POST2000              -2.4315      0.497     -4.892      0.000      -3.406      -1.457
POST2004               3.2752      0.245     13.389      0.000       2.796       3.755
POST2008              -1.6399      0.191     -8.575      0.000      -2.015      -1.265
POST2012               6.2751      0.203     30.848      0.000       5.876       6.674
POST2016               2.3484      0.210     11.204      0.000       1.938       2.759
POST2020               0.9141      0.207      4.405      0.000       0.507       1.321
POST2024               1.8418      0.227      8.121      0.000       1.397       2.286
"""

def parse(data):
    lines = data.strip().split('\n')
    m = {}
    for l in lines:
        parts = l.split()
        if len(parts) >= 5:
            var = parts[0]
            val = float(parts[1])
            pval = float(parts[4])
            stars = "***" if pval < 0.01 else "**" if pval < 0.05 else "*" if pval < 0.1 else ""
            m[var] = f"{val:.3f}{stars}"
    return m

d1_p = parse(d1)
d2_p = parse(d2)

# Generate tex output
# I will read existing tex and rewrite it.
tex_file = "src/paper/results_regression.tex"
with open(tex_file, "r") as f:
    lines = f.readlines()

new_lines = []
for idx, line in enumerate(lines):
    if "\\begin{tabular}" in line:
        line = line.replace("*{5}", "*{6}")
    if "\\multicolumn{2}{c}{\\textbf{OLS}}" in line:
        line = line.replace("\\multicolumn{2}{c}{\\textbf{OLS}}", "\\multicolumn{3}{c}{\\textbf{OLS}}")
    if "\\textbf{Top 40} & \\textbf{Top 40 + AM} \\\\" in line:
        line = line.replace("\\textbf{Top 40 + AM} \\\\", "\\textbf{Top 40 + AM} & \\textbf{New OLS Model} \\\\")
        
    # Match data row with ampersands
    if "&" in line and "\\\\" in line and not "\\multicolumn" in line and not "textbf" in line and not "bottomrule" in line and not "cmidrule" in line:
        parts = line.split('&')
        var_name = parts[0].strip()
        # Find if it exists in d1_p
        if var_name in d1_p:
            parts[-1] = parts[-1].replace("\\\\", f"& {d1_p[var_name]} \\\\")
            line = "&".join(parts)
        elif var_name == "ln_GDP":
            parts[-1] = parts[-1].replace("\\\\", f"& {d1_p['GDP']} \\\\")
            line = "&".join(parts)
        elif var_name == "ln_Population":
            parts[-1] = parts[-1].replace("\\\\", f"& {d1_p['Population']} \\\\")
            line = "&".join(parts)
        elif var_name == "Is_Communist":
            parts[-1] = parts[-1].replace("\\\\", f"& {d1_p['Is_Communist']} \\\\")
            line = "&".join(parts)
        elif var_name == "AM (History)":
            parts[-1] = parts[-1].replace("\\\\", f"& {d1_p['Avg_Medals_History']} \\\\")
            line = "&".join(parts)
        elif var_name == "Constant":
            parts[-1] = parts[-1].replace("\\\\", f"& {d1_p['const']} \\\\")
            line = "&".join(parts)
        
        # Now handle the parenthesis row
        elif var_name == "" and len(parts) > 1 and "(" in parts[-1]:
            # Guess the variable from the previous line?
            prev_line = new_lines[-1]
            prev_var = prev_line.split('&')[0].strip()
            
            if prev_var in d2_p:
                val = f"({d2_p[prev_var]})"
                parts[-1] = parts[-1].replace("\\\\", f"& {val} \\\\")
                line = "&".join(parts)
            elif prev_var == "AM (History)":
                val = f"({d2_p['Avg_Medals_History']})"
                parts[-1] = parts[-1].replace("\\\\", f"& {val} \\\\")
                line = "&".join(parts)
            elif prev_var == "Constant":
                 parts[-1] = parts[-1].replace("\\\\", f"& ({d2_p['const']}) \\\\")
                 line = "&".join(parts)
            else:
                 # Add empty cell
                 parts[-1] = parts[-1].replace("\\\\", "& --- \\\\")
                 line = "&".join(parts)
        elif var_name == "":
            pass # Keep it but append --- if it's the second row of a var
            
    new_lines.append(line)

with open(tex_file, "w") as f:
    f.writelines(new_lines)
print("done")
