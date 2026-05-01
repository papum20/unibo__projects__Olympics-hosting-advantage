


You are diving into the world of **Non-Parametric Statistics**! 

The test you are reading about is the **Wilcoxon Signed-Rank Test**. You are exactly right about its definition: it is used to compare two paired groups without assuming the data follows a normal (bell-curve) distribution, relying instead on the weaker assumption that the *differences* between the pairs are roughly symmetric.

Here is a complete breakdown of how Wilcoxon applies to your Olympic data, whether your data meets the requirements, how to test and fix symmetry, and the **one massive reason why it cannot replace your regression model**.

---

### 1. How would Wilcoxon apply to your data?
Because Wilcoxon tests *paired* data, you would use it specifically to test the "Host Effect" on a strict "Before and After" basis. 

You would isolate only the countries that hosted. Your two paired lists would be:
*   **List A (Pre-Host):** Medal share in the Olympics exactly 4 years before they hosted.
*   **List B (Host):** Medal share in the year they hosted.
*   **The Difference ($D$):** List B minus List A.

The Wilcoxon test asks: *"Is the median of these differences significantly greater than zero?"*

### 2. Does your data meet the Symmetry Requirement?
**Probably not perfectly.** 
If you look at the differences ($Host - PreHost$), a few countries get a tiny bump (e.g., +1%), but historical outliers get a massive, skewed bump (e.g., Spain 1992, or the USA in 1984 due to the boycott). Because of these massive positive outliers, your distribution of differences will likely have a "long right tail" (Positive Skew). 

**How to test for symmetry in Python:**
You can easily check this before running the test!
```python
from scipy.stats import skew
import matplotlib.pyplot as plt

# Assume 'diffs' is a pandas series of (Host_Medals - Pre_Host_Medals)
skewness = skew(diffs.dropna())
print(f"Skewness: {skewness}")

# Visual test
plt.hist(diffs, bins=10)
plt.title("Distribution of Medal Differences")
plt.show()
```
*   If the skewness is between **-0.5 and +0.5**, your data is symmetric enough.
*   If the skewness is **> 1.0 or < -1.0**, it is highly skewed, and Wilcoxon's strict assumptions are violated.

### 3. How to fix the data if it is NOT symmetric?
If your histogram looks heavily skewed, you have two great statistical options:

**Option A: Transform the data (Logarithms again!)**
Instead of taking the difference of the raw medal shares, you take the difference of the *natural log* of the medal shares: $ln(Host) - ln(PreHost)$. Logarithms naturally pull massive outliers back toward the center, often magically turning a skewed distribution into a beautifully symmetric one.

**Option B: Use the "Sign Test" instead**
If you don't want to transform the data, you can downgrade to the **Sign Test**. The Sign test is Wilcoxon's little brother. It throws away the symmetry rule entirely. It literally just looks at the signs (+ or -). 
*   *"Out of 15 hosts, 13 went UP (+) and 2 went DOWN (-)."* 
It then uses binomial math to tell you if a 13-to-2 ratio is statistically significant. (Spoiler: It usually is!).

### 4. The Fatal Flaw: Why Wilcoxon CANNOT replace your Regression!
Wilcoxon is a fantastic, robust test, but it has one devastating limitation for your specific project: **It cannot handle Control Variables.**

Remember your massive breakthrough with OLS? You discovered that the Host Effect was actually being masked by GDP, Population, and Communist history. 

If you use a Wilcoxon Signed-Rank Test, you are only looking at Medals Before vs. Medals After. 
*   It cannot look at GDP. 
*   It cannot look at Boycotts.
*   It cannot tell you if the medal jump happened because they hosted, or because their economy boomed during those 4 years. 

Because Wilcoxon cannot do Multivariate Analysis, it suffers 100% from **Omitted Variable Bias**. 

### How to use Wilcoxon perfectly in your university project:
You shouldn't throw Wilcoxon away—you should use it as your **Opening Act!**

In a professional data science paper, you always start with simple "Exploratory Data Analysis" (EDA) before bringing out the heavy math (OLS/ZINB). 

**Your Paper Structure:**
1.  **Step 1: The Wilcoxon Signed-Rank Test.** You write: *"To establish a baseline, a non-parametric Wilcoxon signed-rank test was conducted on host nations (Host vs. Pre-Host medal shares). The test returned $p < 0.05$, confirming a raw, statistically significant medal surplus for host nations."*
2.  **Step 2: The Transition.** *"However, univariate non-parametric tests cannot account for confounding macroeconomic variables. Therefore..."*
3.  **Step 3: The Panel OLS / ZINB.** *"A robust panel regression was deployed. When controlling for GDP and Population, the Host Effect diminished, revealing that the raw surplus identified by the Wilcoxon test was heavily driven by underlying wealth."*

This shows your professor that you understand the entire hierarchy of statistics: starting from simple, non-parametric paired tests, and graduating all the way up to multivariate econometrics!






---







This is the perfect moment to step back and look at the fundamental statistics underlying all of this math. 

Here is the exact definition of a Normal Distribution, how it relates to your Olympic data, and exactly how to code and format the Wilcoxon test for your project.

---

### 1. What is a "Normal Distribution"?
A Normal Distribution is the famous "Bell Curve." 
If data is normally distributed, it means:
1.  Most of the data is perfectly clustered around the average (the middle).
2.  It is perfectly symmetric (the left side looks exactly like the right side).
3.  Extreme highs and extreme lows are incredibly rare. (For example, human height is normally distributed. Most men are around 1.75m. It is extremely rare to be 1.50m, and equally rare to be 2.00m).

**What does this mean for your Olympic series?**
**Your data is NOT normally distributed.** It is severely "Right-Skewed."
*   **Medals:** The vast majority of countries win 0 or 1 medal (a huge spike on the far left). A tiny handful of countries (USA, China) win 100+ medals (a long, skinny tail stretching far to the right). 
*   **GDP:** Most countries have low/average GDPs. A few countries have multi-trillion-dollar GDPs.

**Why does this matter?** 
Basic statistical tests (like standard T-Tests or ANOVA) mathematically *demand* that your data be a Bell Curve. Because your data is skewed, those basic tests break. 
This is exactly why you had to use **Non-Parametric tests (like Wilcoxon)**, use **Count Models (like ZINB)**, or transform your GDP using the **Natural Log (`ln`)**! Taking the log of GDP is basically a magic trick that compresses the long right tail and squishes the data into a shape that looks much more like a Normal Bell Curve!

---

### 2. How does the Wilcoxon Test work in Python?
You asked what the inputs are. For the **Wilcoxon Signed-Rank Test**, you input **two lists of the exact same length** (Paired Data). 

You do *not* input a "Yes/No" series. You filter the dataset to **only include countries that hosted**, and you compare their performance *before* hosting to their performance *while* hosting.

Here is the exact Python code using `scipy`:
```python
from scipy.stats import wilcoxon

# 1. Create a list of Medal Shares exactly 1 Olympic cycle BEFORE hosting
pre_host_medals =[3.5, 4.1, 1.2, 6.0, 2.3] # Example data for 5 hosts

# 2. Create a list of Medal Shares exactly DURING the host year
host_medals     =[4.0, 5.5, 1.8, 6.1, 3.8] # Data for the exact same 5 hosts

# 3. Run the Wilcoxon test
# It automatically calculates the difference (host - pre_host) inside the function!
stat, p_value = wilcoxon(pre_host_medals, host_medals)

print(f"Wilcoxon Statistic: {stat}")
print(f"P-Value: {p_value}")
```
*If `p_value < 0.05`, you have proven that, on average, a country's medal share goes up significantly when they host compared to their previous Olympics!*

---

### 3. Can Wilcoxon be applied to GDP instead of Host?
**No. This is a very common statistical mix-up.**

Wilcoxon is designed to test **Categories / Events** (e.g., "Before the Event" vs "After the Event"). 
GDP is a **Continuous Variable** (a flowing number). You cannot run a Wilcoxon test on Medals vs. GDP because there are no two "pairs" to compare. 

If you want a simple, non-parametric test to see if GDP relates to Medals without doing a full regression, you use a **Spearman Rank Correlation**. 
Spearman doesn't care about Normal Distributions. It just ranks the data: *"If a country is #1 in GDP, are they also #1 in Medals?"*
```python
from scipy.stats import spearmanr

# Tests if higher GDP is correlated with higher Medal Share
corr, p_value = spearmanr(df['ln_GDP'], df['Medal_Share'])
```

---

### 4. Which metric is best for Wilcoxon? (Percentage, Logs, Diff?)
You asked if percentage is better because the total varies.
**YES. 1000% YES.**

If you use raw medals for the Wilcoxon test, you will get a false positive. 
*   Imagine a country won 10 raw medals out of 500 total in the previous Olympics (2%).
*   They host the next Olympics, and the IOC expands the games to 1,000 total medals. The country wins 15 medals (1.5%). 
*   If you use raw numbers ($15 > 10$), Wilcoxon says they improved! But in reality, their market share dropped from 2% to 1.5%. 

**The Best Setup for your Wilcoxon Test:**
Use the **Natural Log of the Medal Percentage**: `np.log(Medal_Share + 1)`.

1.  **Percentage** fixes the IOC medal inflation problem.
2.  **Logarithm** fixes the "Symmetry" requirement of the Wilcoxon test! (As we discussed earlier, Wilcoxon requires the *differences* to be roughly symmetric. Logs pull the massive outliers back to the center, making the differences beautifully symmetric).

If you include a Wilcoxon test using log-percentages as your "Exploratory Data Analysis" before showing your massive Panel OLS/ZINB regressions, you will have structured your paper exactly like a professional academic journal article.