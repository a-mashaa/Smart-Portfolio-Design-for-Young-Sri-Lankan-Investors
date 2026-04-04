# Smart Portfolio Design — Young Sri Lankan CSE Investors
## Streamlit App Setup Guide

---

## 📁 Files Required
```
project/
├── app.py                 ← Main Streamlit app
├── requirements.txt       ← Python dependencies
└── CLOSEPRICES.xlsx       ← CSE stock price data
```

---

## ⚙️ Setup Instructions

### Step 1 — Install Python
Make sure Python 3.8+ is installed:
```bash
python --version
```

### Step 2 — Create a Virtual Environment (recommended)
```bash
python -m venv venv

# Activate on Windows:
venv\Scripts\activate

# Activate on Mac/Linux:
source venv/bin/activate
```

### Step 3 — Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4 — Place Data File
Put `CLOSEPRICES.xlsx` in the **same folder** as `app.py`.

### Step 5 — Run the App
```bash
streamlit run app.py
```

The app will open automatically at: **http://localhost:8501**

---

## 🚀 Deploy Online (Free) — Streamlit Community Cloud

1. Push your project to a **GitHub repository**
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Click **"New app"** → Select your repo
4. Set **Main file path** to `app.py`
5. Click **Deploy**

> Upload `CLOSEPRICES.xlsx` to your repo too, OR use the sidebar uploader in the app.

---

## 📱 App Features

### Tab 1 — Risk Framework
- 7-method risk boundary calculation
- Conservative / Moderate / Aggressive zones
- CSE emerging market adjustment

### Tab 2 — Stock Screening
- Dual-criteria filter (Risk + Affordability)
- Interactive scatter plot
- Full screening table

### Tab 3 — Portfolios
- 3 age-based optimized portfolios
- Weight allocation charts
- Efficient frontier visualization

### Tab 4 — Monte Carlo
- 100–1,000 scenario simulations
- Capital projection over 5 years
- Probability of positive return / doubling

### Tab 5 — Research Summary
- Full methodology documentation
- Academic references
- Stock data overview table

---

## 👤 Investor Profile (Sidebar)

| Setting | Options |
|---------|---------|
| Age | 18–40 |
| Monthly Income | Rs. 30,000 – Rs. 150,000 |
| Investment Rate | 5–30% of income |
| Months Saved | 3–12 months |

The app automatically recommends the right portfolio based on your age:
- **Ages 22–25** → 🚀 Aggressive
- **Ages 26–30** → ⚖️ Moderate
- **Ages 30–35** → 🛡️ Conservative

---

## 📚 Research Methodology

### Risk Boundary Methods
1. **Minimum Variance Portfolio** — Lower bound
2. **Maximum Sharpe Portfolio** — Upper bound
3. **Equal Weight** — Baseline reference
4. **Percentile (25th–75th)** — Distribution-based
5. **Std Deviation (μ ± σ)** — Statistical range
6. **Value at Risk (95% CI)** — Tail risk
7. **K-Means Clustering** — Low/Medium/High groups

### Adjustments for CSE
- **30-year horizon:** ×1.30 upper bound
- **Emerging market:** Use 75th percentile of actual CSE volatility
- Justified by Bekaert & Harvey (2003): emerging markets = 1.5–3× developed

### Stock Screening
- **Stage 1:** Volatility within adjusted bounds
- **Stage 2:** Price ≤ Capital ÷ (15 stocks × 10 shares)
- Both criteria required for qualification

### Portfolio Optimization
- Conservative: Minimize variance (Markowitz 1952)
- Moderate: Maximize Sharpe ratio (Sharpe 1966)
- Aggressive: Maximize expected return
- Weights: 2–30% per stock (no concentration)

---

## 🔧 Troubleshooting

**App won't start?**
```bash
pip install --upgrade streamlit
streamlit run app.py
```

**Data not loading?**
- Ensure `CLOSEPRICES.xlsx` is in the same folder as `app.py`
- OR use the sidebar file uploader

**Port already in use?**
```bash
streamlit run app.py --server.port 8502
```

**Browser doesn't open automatically?**
Manually open: `http://localhost:8501`

---

*Research: Smart Portfolio Design for Young Sri Lankan Investors · CSE · 2020–2024*
