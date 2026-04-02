

im following human data science course but didnt attend and i need to do a project, on any topic of my choice, using the same scientific methods the prof used. this is the course material, what are the instruments, statistical ones, regressions, causality, etc. everything which is present in these studies and materials which i can use for my research?



-------------------





Based on the course materials provided from the "Human Data Science" course (taught by professors like Marco Roccetti, Luca Casini, Giovanni Delnevo, and Silvia Mirri), the curriculum heavily focuses on applying a mix of **traditional statistics, machine learning, and deep learning** to solve complex, real-world problems (e.g., COVID-19 spread, archaeological site detection, and predictive maintenance for water meters). 

A major overarching theme of your professors' work is the **"Human-in-the-loop" philosophy**: they care deeply about data quality, context, and semantics rather than just feeding massive amounts of raw data into a "black box."

Here is a comprehensive breakdown of all the scientific methods, statistical instruments, and algorithms present in the course materials that you can use for your project:

### 1. Exploratory Data Analysis (EDA) & Classical Statistics
Before jumping into complex AI, the course emphasizes rigorous statistical foundations:
*   **Hypothesis Testing:** Z-tests, T-tests (independent, paired, one-sample), ANOVA (F-tests), and Chi-Square tests.
*   **Distribution Testing:** Kolmogorov-Smirnov (KS) test to check if two samples come from the same distribution.
*   **Correlation Analysis:** 
    *   *Pearson’s $r$ coefficient* (used in their COVID-19 vs. pollution studies).
    *   *Cramér’s V* and *Theil’s U index* (used to find correlations between categorical variables and labels).
*   **Resampling Techniques:** Bootstrapping, Permutation tests, and Cross-Validation (specifically $k$-fold cross-validation).
*   **A/B Testing:** Designing experiments and calculating Power and Sample Size to detect significant effects.

### 2. Time Series & Causal Inference
Your professors did extensive work modeling the spread of COVID-19 using time-series data. If you want to do a forecasting or temporal project, you can use:
*   **Granger Causality:** A statistical hypothesis test to determine whether one time series is useful in forecasting another (e.g., testing if pollution levels "Granger-cause" COVID-19 infections after a time lag).
*   **Augmented Dickey-Fuller Test:** Used to verify if a time series is stationary (a prerequisite for Granger causality).
*   **Bayesian Changepoint Detection:** Using Markov Chain Monte Carlo (MCMC) methods to find structural breaks in a time series (e.g., finding the exact date when COVID-19 infections switched from a decreasing to an increasing trend).
*   **Piecewise Linear Regression:** Fitting distinct linear regression lines to different segments of time-series data separated by a changepoint.

### 3. Traditional Machine Learning Models
If you are working with tabular data (regression or classification), the materials cover a wide array of classic algorithms:
*   **Regressions:** Linear Regression, and **Generalized Linear Models (GLM)**—specifically *Negative Binomial Regression* and *Poisson Regression* (highly recommended by the professors for counting/epidemiological data).
*   **Classifiers:** Logistic Regression, Support Vector Machines (SVM/SVC), K-Nearest Neighbors (KNN).
*   **Tree-based & Ensemble Methods:** Classification and Regression Trees (CART), Random Forest (RF), Extra Trees (ET), Adaptive Boosting (AdaBoost), Gradient Boosting (GB), and Bagging.

### 4. Deep Learning (DL)
For unstructured data (images, sequences), the course covers several neural network architectures:
*   **For Sequential/Time-Series Data:** Recurrent Neural Networks (RNNs), LSTMs (Long Short-Term Memory), and GRUs (Gated Recurrent Units). They used these to predict water meter failures based on historical readings.
*   **For Image/Computer Vision Data:** Convolutional Neural Networks (CNNs). Specifically, architectures like ResNet, EfficientNet, U-Net, and MAnet.
*   **Semantic Segmentation:** Used in their archaeological studies to detect sites from satellite imagery.
*   **Advanced Architectures:** The course also touches on Autoencoders, Generative Adversarial Networks (GANs), and Transformers (with attention mechanisms).

### 5. Data Pre-Processing & "Human-in-the-Loop" Techniques
Your professors strongly penalize models trained on "dirty" data. You should strongly consider implementing these techniques in your project:
*   **Handling Imbalanced Data:** Using **SMOTE-NC** (Synthetic Minority Over-sampling Technique for Nominal and Continuous) to oversample minority classes.
*   **Dimensionality Reduction:** Principal Component Analysis (PCA) and Binning.
*   **Pareto Analysis / Data Semantics Filtering:** Instead of feeding all data into a model, they used the 80/20 Pareto rule to isolate only the most statistically coherent and meaningful features, discarding "noisy" data manually (the human-in-the-loop approach).
*   **Data Augmentation:** For images (random cropping, flipping, rotation, GaussNoise, blurring) to prevent overfitting.
*   **Transfer Learning:** Taking a pre-trained model (like Google's InceptionV3 or models trained on ImageNet) and fine-tuning it on a smaller, specific dataset. 

### 6. Evaluation Metrics
To prove your model works, use the exact metrics the professors use:
*   **For Classification:** AUC-ROC (Area Under the Curve), Confusion Matrices, Precision, Recall, F1-score, Positive Predictive Value (PPV), Negative Predictive Value (NPV).
*   **For Regression:** MAE (Mean Absolute Error), RMSE (Root Mean Squared Error), MAPE (Mean Absolute Percentage Error).
*   **For Image Segmentation:** IoU (Intersection over Union), Dice Loss, Focal Loss, and MCC (Matthews Correlation Coefficient).

### 💡 Tips for Your Project:
To impress your professors, **don't just throw a complex Deep Learning model at a random dataset.** Choose a problem, apply an exploratory statistical analysis first to "clean" and understand the semantics of the data, and compare a simple model against a complex one. 

**Project Idea Examples based on the Syllabus:**
1.  **Epidemiological/Economic Time Series:** Take a dataset (e.g., flu cases, stock market trends, or transport data), use *Granger Causality* to find leading indicators, and then predict future trends using a *Generalized Linear Model (Negative Binomial)* or *Bayesian Changepoint Detection*.
2.  **Predictive Maintenance / Imbalanced Classification:** Find an industrial dataset (e.g., machine failures). Use *SMOTE* to balance the data, apply *Pareto Analysis* to select features, and compare a *Random Forest* or *Gradient Boosting* model against an *LSTM*.
3.  **Satellite/Medical Imagery:** Take a dataset of satellite images (e.g., deforestation, urban growth) or medical scans. Use *Semantic Segmentation (U-Net)* with *Transfer Learning* and *Data Augmentation* to detect anomalies, using *IoU* as your metric.





-------------------


User 4:41 PM
sorry but i dont know any of these tools can u give me more information. i want to study olympics and correlation between medals and hosting; specifically i found an interesting paper saying theres no causality here but rather its mostly related to GDP (https://www.nature.com/articles/s41598-022-27259-8) so i want to exapnd that. can u xplain better the tools i can use?
ill need no DL ML etc models but mostly statistical tools and analysis
i want to expand it maybe with more countries, winter olympics, and find a correlation with medals and not hosting but playing in a close country, especially for a state in the EU: this should highlight something either positive or negative regarding the correlation with jetlag, travelling for athlets etc.
and maybe ill use more up to date GDP data since it evolved

-------------------


This is a fantastic project idea. It perfectly aligns with the core philosophy of the "Human Data Science" course: **challenging assumptions, focusing on data semantics, and understanding the *why* behind the numbers** rather than just throwing a machine learning model at a dataset. 

Since you want to focus strictly on classical statistics and causality (no Deep Learning or complex ML), we can look directly at the statistical instruments your professors used in their own research (like their COVID-19 studies) and adapt them to the Olympics.

Here is a detailed, easy-to-understand explanation of the specific statistical tools from your course materials that you can use for this project, and exactly *how* to apply them to your Olympics/GDP/Distance idea:

---

### 1. Generalized Linear Models (GLMs): Poisson & Negative Binomial Regression
**What it is:** You probably know standard Linear Regression (drawing a straight line through data points). However, standard linear regression is meant for *continuous* data (like predicting a house price: $250,500.50). **Olympic medals are "Count Data"**—you can win 0, 1, 2, or 50 medals, but you cannot win -5 or 3.14 medals. 
When your professors predicted COVID-19 infections (which are also counts), they specifically used **Poisson Regression** and **Negative Binomial Regression**.
**How to use it for your project:** 
You can build a Negative Binomial Regression model where:
*   **Target Variable (Y):** Number of medals won by a country.
*   **Predictor 1 (X1):** GDP of the country.
*   **Predictor 2 (X2):** Population.
*   **Predictor 3 (X3):** Distance from the host country (e.g., in kilometers, or time zone difference to measure jetlag).
*   **Why it impresses the professors:** By using this, you can mathematically isolate the effect of *distance* while controlling for *GDP*. The model will tell you: *"Assuming two countries have the exact same GDP and population, does the one closer to the host country win more medals?"*

### 2. Hypothesis Testing: T-Tests and ANOVA
**What it is:** These are tests to determine if the difference between groups is mathematically significant or just due to random luck.
*   **T-Test:** Compares the averages of **two** groups.
*   **ANOVA (Analysis of Variance):** Compares the averages of **three or more** groups.
**How to use it for your project:**
*   **The T-Test:** Group an EU country’s historical performances into two buckets: "Olympics held in Europe/Same Timezone" vs. "Olympics held far away (Asia/Americas)". Use a T-test to see if their average medal count is significantly higher when playing close to home.
*   **ANOVA:** Divide all participating countries into categories based on travel strain: *Group A (0-3 hours time difference)*, *Group B (4-7 hours)*, and *Group C (8+ hours)*. Run an ANOVA to see if travel strain creates a statistically significant drop in performance across the board.

### 3. Correlation Analysis (Pearson & Partial Correlation)
**What it is:** Pearson’s $r$ measures how closely two variables move together on a scale of -1 to 1. A score of 1 means perfect positive correlation (GDP goes up, medals go up); -1 means perfect negative correlation (Distance goes up, medals go down).
**How to use it for your project:**
*   Calculate the **Pearson correlation** between flight hours (or physical distance) and the percentage of total medals won. 
*   **Partial Correlation (Crucial Step):** Because rich countries might just happen to be closer to certain host cities, you can run a *Partial Correlation*. This calculates the correlation between Distance and Medals *while mathematically subtracting the influence of GDP*. This directly expands on the *Nature* paper you cited!

### 4. Granger Causality (Time-Series Analysis)
**What it is:** Your professors used this extensively to prove that pollution *causes* COVID spread, not just correlates with it. "Granger Causality" is a statistical test used on time-series data to see if past values of Variable X can predict future values of Variable Y better than just looking at past values of Y alone.
**How to use it for your project:**
You can test the *Nature* paper's hypothesis directly over time. Does a spike in a country's GDP *Granger-cause* a spike in their Olympic medals in the subsequent Winter/Summer games? Or is it the other way around? (Maybe hosting/winning medals boosts the GDP?). Applying this time-series test adds a massive layer of academic rigor to your project.

### 5. Bayesian Changepoint Detection
**What it is:** This is a method your professors used to find the exact date when COVID-19 infection rates suddenly changed slopes (from decreasing to increasing). It finds "structural breaks" in a timeline.
**How to use it for your project:**
Look at the timeline of specific EU countries' Olympic performances from 1960 to 2024. Feed the medal counts into a Changepoint algorithm. Does the algorithm detect a sudden permanent shift in performance? You can then investigate *why* that happened. Did the changepoint align with a massive economic boom (GDP change)? Did it align with the fall of the Soviet Union? Did it align with a national policy change regarding sports funding?

---

### Step-by-Step Blueprint for your Project

If you want to structure this into a high-grade paper for the exam, follow the "Data Semantics" workflow your professors love:

**Phase 1: Data Semantics & Pre-processing (The "Human-in-the-Loop" phase)**
*   *The Professors' rule:* "Data is dirty. Define the semantics." 
*   Total medals available change every Olympic year (e.g., there are way more sports now than in 1980). Therefore, raw medal counts are bad data. **Convert medals to "Percentage of Total Medals Available"** to normalize the data across decades.
*   Update the GDP data using World Bank or IMF datasets up to 2024.
*   Create a "Jetlag Index" (e.g., difference in hours between the capital of the competing country and the host city).

**Phase 2: Exploratory Data Analysis (EDA)**
*   Plot scatterplots of GDP vs. Medal Share.
*   Plot scatterplots of Jetlag Index vs. Medal Share.
*   Look for outliers (e.g., countries with low GDP but high medals—like Kenya in marathon running or Norway in Winter Olympics).

**Phase 3: Statistical Testing**
*   Run the **T-Tests / ANOVA** on the Jetlag Index groups. 
*   Report the *p-values* (if p < 0.05, you can confidently state that jetlag/distance negatively impacts athletic performance).

**Phase 4: Generalized Linear Modeling**
*   Run the **Negative Binomial Regression**. Show the coefficients. If the coefficient for "Distance from Host" is negative and statistically significant even when GDP is included, you have successfully proven your hypothesis and expanded the *Nature* paper!

This approach requires zero Deep Learning or Black Box AI. It relies entirely on interpretable, robust mathematics—exactly what the "Human Data Science" course advocates for.