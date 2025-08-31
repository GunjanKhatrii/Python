# 📊 Stock Price Analysis (Apple, Amazon, Google, Microsoft)

This project performs **exploratory data analysis (EDA)** and **visualization** on stock prices of major tech companies (Apple, Amazon, Google, and Microsoft) using Python.  
It explores stock trends, moving averages, returns, resampling, and correlation between companies.

---

## 📌 Features & Analysis Steps

### 1. **Data Collection**
- Used `glob` to fetch stock CSV files from a dataset folder.
- Merged data using `pandas.DataFrame.append()`.
- Selected companies:
  - **Apple (AAPL)**
  - **Amazon (AMZN)**
  - **Google (GOOG)**
  - **Microsoft (MSFT)**

---

### 2. **Stock Price Trends**
- Converted `date` column into proper `datetime`.
- Visualized stock price changes over time using **Matplotlib**.

---

### 3. **Moving Averages**
- Calculated rolling means for **10, 20, and 50 days**.
- Visualized moving averages to observe trends and smooth price fluctuations.

---

### 4. **Daily Stock Returns**
- Calculated **daily percentage returns**:
  \[
  \text{Daily Return} = \frac{(P_t - P_{t-1})}{P_{t-1}} \times 100
  \]
- Visualized Apple’s daily returns using **Plotly Express** for interactive plots.

---

### 5. **Resampling Analysis**
Resampled stock closing prices into different time periods:
- Monthly (`M`)
- Quarterly (`Q`)
- Yearly (`Y`)
- Weekly (`W`)
- Custom intervals (`30S`, `17min` etc.)

---

### 6. **Correlation of Closing Prices**
- Combined closing prices of all companies into a single DataFrame.
- Visualized **pair plots** (`sns.pairplot`) and **heatmaps** (`sns.heatmap`).
- **Findings**:
  - Google & Microsoft are highly correlated.
  - Amazon & Microsoft also show strong correlation (~0.96).

---

### 7. **Correlation of Daily Returns**
- Computed **daily return percentage changes** for all companies.
- Used **PairGrid**:
  - Histograms on diagonals
  - Scatterplots on lower triangle
  - KDE (contour density) plots on upper triangle
- **Findings**:
  - Apple & Amazon daily returns show partial linear correlation.

---

## 📂 Project Structure


