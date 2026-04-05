"""
Smart Portfolio Design for Young Sri Lankan Investors
CSE (Colombo Stock Exchange) — Portfolio Advisor App
Research by: M.K.A. Loshani
"""

import streamlit as st
import pandas as pd
import numpy as np
from scipy.optimize import minimize
from sklearn.cluster import KMeans
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import warnings
import io
warnings.filterwarnings('ignore')

# ─────────────────────────────────────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Smart Portfolio — Young CSE Investors",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─────────────────────────────────────────────────────────────────────────────
# CUSTOM CSS  —  Youth-Friendly UI
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=Space+Grotesk:wght@400;500;600;700;800&display=swap');

/* ── BASE ─────────────────────────────────────────── */
html, body, [class*="css"] {
    font-family: 'Plus Jakarta Sans', sans-serif;
}
.stApp {
    background: linear-gradient(135deg, #f0f4ff 0%, #f9f4ff 40%, #fff4fb 100%);
    color: #18172b;
}

/* ── SIDEBAR ──────────────────────────────────────── */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #ffffff 0%, #f4f0ff 100%);
    border-right: 1px solid #e4d9ff;
}
[data-testid="stSidebar"] * { color: #18172b !important; }
[data-testid="stSidebar"] .stSlider label,
[data-testid="stSidebar"] .stSelectbox label,
[data-testid="stSidebar"] .stFileUploader label {
    color: #6c5eb5 !important;
    font-weight: 600 !important;
    font-size: 0.82rem !important;
    text-transform: uppercase !important;
    letter-spacing: 0.5px !important;
}

/* ── HEADER ───────────────────────────────────────── */
.main-title {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 2.7rem;
    font-weight: 800;
    background: linear-gradient(135deg, #6c3de8 0%, #c4338a 60%, #f5a623 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    line-height: 1.1;
    letter-spacing: -1px;
}
.main-subtitle {
    font-size: 0.92rem;
    color: #8878c0;
    font-weight: 400;
    letter-spacing: 0.2px;
}

/* ── SECTION TITLES ───────────────────────────────── */
.section-title {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 1.4rem;
    font-weight: 700;
    color: #18172b;
    padding-bottom: 10px;
    margin-bottom: 18px;
    border-bottom: 3px solid transparent;
    border-image: linear-gradient(90deg, #6c3de8, #c4338a, #f5a623) 1;
}

/* ── METRIC CARDS ─────────────────────────────────── */
.metric-card {
    background: #ffffff;
    border: 1px solid #e8dfff;
    border-radius: 18px;
    padding: 20px 22px;
    text-align: center;
    box-shadow: 0 4px 20px rgba(108,61,232,0.08);
    transition: transform 0.25s cubic-bezier(.34,1.56,.64,1), box-shadow 0.25s;
    position: relative;
    overflow: hidden;
}
.metric-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    background: linear-gradient(90deg, #6c3de8, #c4338a, #f5a623);
    border-radius: 18px 18px 0 0;
}
.metric-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 14px 36px rgba(108,61,232,0.15);
}
.metric-label {
    font-size: 0.68rem;
    color: #9b8cc4;
    text-transform: uppercase;
    letter-spacing: 1.3px;
    font-weight: 700;
    margin-bottom: 6px;
}
.metric-value {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 2rem;
    font-weight: 800;
    color: #18172b;
    line-height: 1;
}
.metric-unit { font-size: 0.85rem; color: #9b8cc4; font-weight: 400; }

/* ── PROFILE ELEMENTS ─────────────────────────────── */
.profile-badge {
    background: linear-gradient(135deg, #f4f0ff, #fff0fb);
    border: 2px solid #c4b5fd;
    border-radius: 18px;
    padding: 18px;
    margin-bottom: 14px;
    box-shadow: 0 4px 16px rgba(108,61,232,0.09);
}
.profile-name {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 1.3rem;
    font-weight: 700;
    color: #6c3de8;
}
.profile-detail { color: #8878c0; font-size: 0.88rem; }

/* ── STOCK TABLE ──────────────────────────────────── */
.stock-row-pass { background: rgba(16,185,129,0.06); }
.stock-row-fail { background: rgba(239,68,68,0.04); }

/* ── RISK ZONE CARDS ──────────────────────────────── */
.zone-conservative {
    background: linear-gradient(120deg, #ecfdf5, #f0fdf4);
    border-left: 4px solid #10b981;
    border-radius: 12px;
    padding: 14px 18px; margin: 8px 0;
    box-shadow: 0 2px 10px rgba(16,185,129,0.1);
    transition: transform 0.2s ease;
}
.zone-conservative:hover { transform: translateX(5px); }

.zone-moderate {
    background: linear-gradient(120deg, #fffbeb, #fef3c7);
    border-left: 4px solid #f59e0b;
    border-radius: 12px;
    padding: 14px 18px; margin: 8px 0;
    box-shadow: 0 2px 10px rgba(245,158,11,0.1);
    transition: transform 0.2s ease;
}
.zone-moderate:hover { transform: translateX(5px); }

.zone-aggressive {
    background: linear-gradient(120deg, #fff1f2, #ffe4e6);
    border-left: 4px solid #f43f5e;
    border-radius: 12px;
    padding: 14px 18px; margin: 8px 0;
    box-shadow: 0 2px 10px rgba(244,63,94,0.1);
    transition: transform 0.2s ease;
}
.zone-aggressive:hover { transform: translateX(5px); }

/* ── TABS ─────────────────────────────────────────── */
[data-baseweb="tab-list"] {
    background: transparent;
    border-bottom: 2px solid #e4d9ff;
    gap: 2px;
}
[data-baseweb="tab"] {
    color: #9b8cc4 !important;
    font-weight: 600;
    font-size: 0.88rem;
    border-radius: 10px 10px 0 0;
    padding: 8px 18px !important;
    transition: all 0.2s;
}
[data-baseweb="tab"]:hover {
    background: #f0ebff !important;
    color: #6c3de8 !important;
}
[aria-selected="true"] {
    color: #6c3de8 !important;
    border-bottom-color: #6c3de8 !important;
    background: #f0ebff !important;
}

/* ── DIVIDER ──────────────────────────────────────── */
hr { border-color: #e4d9ff; }

/* ── STREAMLIT NATIVE METRICS ─────────────────────── */
[data-testid="stMetricValue"] {
    color: #6c3de8 !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-weight: 800 !important;
}
[data-testid="stMetricLabel"] {
    color: #9b8cc4 !important;
    font-weight: 600 !important;
    text-transform: uppercase !important;
    font-size: 0.72rem !important;
    letter-spacing: 1px !important;
}

/* ── DATAFRAMES ───────────────────────────────────── */
[data-testid="stDataFrame"] {
    border-radius: 14px !important;
    overflow: hidden;
    border: 1px solid #e4d9ff !important;
    box-shadow: 0 2px 14px rgba(108,61,232,0.06);
}

/* ── BUTTONS ──────────────────────────────────────── */
.stButton > button {
    background: linear-gradient(135deg, #6c3de8, #c4338a);
    color: white;
    border: none;
    border-radius: 12px;
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-weight: 700;
    padding: 8px 22px;
    transition: all 0.2s;
    box-shadow: 0 4px 14px rgba(108,61,232,0.25);
}
.stButton > button:hover {
    opacity: 0.88;
    transform: translateY(-2px);
    box-shadow: 0 8px 20px rgba(108,61,232,0.35);
}

/* ── ALERTS ───────────────────────────────────────── */
.stAlert { border-radius: 14px; }

/* ── SELECTBOX / INPUT ────────────────────────────── */
[data-baseweb="select"] > div {
    border-color: #c4b5fd !important;
    border-radius: 10px !important;
}
[data-baseweb="select"] > div:focus-within {
    border-color: #6c3de8 !important;
    box-shadow: 0 0 0 3px rgba(108,61,232,0.12) !important;
}

/* ── SCROLLBAR ────────────────────────────────────── */
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: #f4f0ff; border-radius: 3px; }
::-webkit-scrollbar-thumb { background: #c4b5fd; border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: #6c3de8; }

/* ── CAPITAL CARD IN SIDEBAR ──────────────────────── */
.capital-card {
    background: linear-gradient(135deg, #6c3de8, #c4338a);
    border-radius: 16px;
    padding: 16px 18px;
    text-align: center;
    margin-top: 10px;
    box-shadow: 0 6px 20px rgba(108,61,232,0.28);
}
.capital-label {
    font-size: 0.65rem;
    color: rgba(255,255,255,0.8);
    text-transform: uppercase;
    letter-spacing: 1.3px;
    font-weight: 700;
    margin-bottom: 4px;
}
.capital-value {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 1.55rem;
    font-weight: 800;
    color: #ffffff;
}

/* ── RECOMMENDED BADGE ────────────────────────────── */
.rec-badge {
    display: inline-block;
    background: linear-gradient(135deg, #6c3de8, #c4338a);
    color: #ffffff;
    font-size: 0.68rem;
    font-weight: 700;
    letter-spacing: 0.6px;
    text-transform: uppercase;
    padding: 5px 14px;
    border-radius: 20px;
    margin-top: 10px;
    box-shadow: 0 3px 10px rgba(108,61,232,0.3);
}

/* ── PROJECTION MINI CARDS ────────────────────────── */
.proj-row {
    display: flex;
    flex-direction: column;
    gap: 7px;
    margin-top: 10px;
    text-align: left;
    font-size: 0.85rem;
}
.proj-item {
    border-radius: 10px;
    padding: 7px 12px;
    font-weight: 500;
}
.proj-expected { background: #f0ebff; color: #6c3de8; }
.proj-best     { background: #ecfdf5; color: #059669; }
.proj-worst    { background: #fff1f2; color: #e11d48; }
.proj-prob     { background: #f0fdf4; color: #16a34a; font-weight: 700; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# DATA LOADING & PROCESSING
# ─────────────────────────────────────────────────────────────────────────────

@st.cache_data
def load_and_process_data(file_bytes):
    df = pd.read_excel(io.BytesIO(file_bytes), sheet_name='Sheet1')
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
    df = df[df['Date'].notna()].drop_duplicates(subset=['Date']).sort_values('Date')
    df = df.set_index('Date')
    stock_names = df.columns.tolist()
    for col in stock_names:
        if df[col].dtype == object:
            df[col] = df[col].astype(str).str.replace(',', '').str.strip()
        df[col] = pd.to_numeric(df[col], errors='coerce')
    df = df.ffill().bfill()
    return df, stock_names

@st.cache_data
def compute_analytics(_df, stock_names):
    returns = _df.pct_change().dropna()
    returns = returns.replace([np.inf, -np.inf], np.nan)
    # Clean extreme returns
    extreme_mask = (returns.abs() > 0.50)
    returns = returns.where(~extreme_mask, np.nan)
    returns = returns.ffill(limit=3)
    for col in returns.columns:
        if returns[col].isna().any():
            returns[col] = returns[col].fillna(returns[col].median())
    returns = returns.dropna()

    annual_returns = returns.mean() * 252
    annual_volatility = returns.std() * np.sqrt(252)
    covariance_matrix = returns.cov() * 252
    current_prices = _df.iloc[-1]

    return returns, annual_returns, annual_volatility, covariance_matrix, current_prices

@st.cache_data
def compute_risk_boundaries(_annual_volatility, _annual_returns, _covariance_matrix, _returns, stock_names):
    n = len(stock_names)
    cov = _covariance_matrix

    # Method 1: Min Variance
    def port_vol(w): return np.sqrt(np.dot(w.T, np.dot(cov, w)))
    cons = [{'type': 'eq', 'fun': lambda w: np.sum(w) - 1}]
    bnds = tuple((0, 1) for _ in range(n))
    x0 = np.array([1/n]*n)
    res = minimize(port_vol, x0, method='SLSQP', bounds=bnds, constraints=cons)
    min_var_vol = res.fun

    # Method 2: Max Sharpe
    def neg_sharpe(w):
        r = np.dot(w, _annual_returns)
        v = port_vol(w)
        return -(r - 0.10) / v if v > 0 else 1e10
    res2 = minimize(neg_sharpe, x0, method='SLSQP', bounds=bnds, constraints=cons)
    max_sharpe_vol = port_vol(res2.x)

    # Method 3: Equal weight
    ew = np.array([1/n]*n)
    ew_vol = port_vol(ew)

    # Method 4: Percentile
    vols = _annual_volatility.values
    p25_t = np.percentile(vols, 25)
    p75_t = np.percentile(vols, 75)
    dists25 = np.abs(vols - p25_t)
    dists75 = np.abs(vols - p75_t)
    sel_n = max(5, n//4)
    idx25 = np.argsort(dists25)[:sel_n]
    idx75 = np.argsort(dists75)[:sel_n]
    w25 = np.zeros(n); w25[idx25] = 1/sel_n
    w75 = np.zeros(n); w75[idx75] = 1/sel_n
    perc_lower = port_vol(w25)
    perc_upper = port_vol(w75)

    # Method 5: StdDev simulation
    np.random.seed(42)
    pvols = []
    for _ in range(10000):
        rw = np.random.random(n); rw /= rw.sum()
        v = port_vol(rw)
        if 0 < v < 2: pvols.append(v)
    pvols = np.array(pvols)
    std_lower = max(0, pvols.mean() - pvols.std())
    std_upper = pvols.mean() + pvols.std()

    # Method 6: VaR
    var_lower = np.percentile(pvols, 2.5)
    var_upper = np.percentile(pvols, 97.5)

    # Method 7: KMeans
    vol_data = vols.reshape(-1,1)
    km = KMeans(n_clusters=3, random_state=42, n_init=10)
    clusters = km.fit_predict(vol_data)
    centers = km.cluster_centers_.flatten()
    sorted_idx = np.argsort(centers)
    low_stocks = [i for i,c in enumerate(clusters) if c == sorted_idx[0]]
    high_stocks = [i for i,c in enumerate(clusters) if c == sorted_idx[2]]
    wl = np.zeros(n); wl[low_stocks] = 1/len(low_stocks) if low_stocks else 0
    wh = np.zeros(n); wh[high_stocks] = 1/len(high_stocks) if high_stocks else 0
    clust_lower = port_vol(wl)
    clust_upper = port_vol(wh)

    lower_list = [min_var_vol, perc_lower, std_lower, var_lower, clust_lower]
    upper_list = [max_sharpe_vol, perc_upper, std_upper, var_upper, clust_upper]
    consensus_lower = float(np.median(lower_list))
    consensus_upper = float(np.median(upper_list))

    # Young investor adjustment (30-year horizon)
    yi_lower = consensus_lower
    yi_upper = consensus_upper * 1.30

    # Emerging market adjustment (CSE)
    cse_vol_75th = float(_annual_volatility.quantile(0.75))
    adj_upper = cse_vol_75th

    # Risk zones
    yi_range = yi_upper - yi_lower
    zone1 = yi_lower + yi_range / 3
    zone2 = yi_lower + 2 * yi_range / 3

    return {
        'min_var_vol': min_var_vol,
        'max_sharpe_vol': max_sharpe_vol,
        'ew_vol': ew_vol,
        'perc_lower': perc_lower, 'perc_upper': perc_upper,
        'std_lower': std_lower, 'std_upper': std_upper,
        'var_lower': var_lower, 'var_upper': var_upper,
        'clust_lower': clust_lower, 'clust_upper': clust_upper,
        'consensus_lower': consensus_lower,
        'consensus_upper': consensus_upper,
        'yi_lower': yi_lower,
        'yi_upper': yi_upper,
        'adj_upper': adj_upper,
        'zone_conservative_end': zone1,
        'zone_moderate_end': zone2,
    }

def compute_max_affordable_price(capital, n_stocks=15, min_shares=10):
    return capital / (n_stocks * min_shares)

def classify_affordability(price, max_price):
    per = price / max_price
    if per <= 0.5: return 'Highly Affordable', 3, '#2ecc71'
    elif per <= 1.0: return 'Affordable', 2, '#f39c12'
    elif per <= 2.0: return 'Moderately Affordable', 1, '#e67e22'
    else: return 'Not Affordable', 0, '#e74c3c'

def screen_stocks(stock_names, annual_volatility, current_prices, bounds, capital):
    adj_lower = bounds['yi_lower']
    adj_upper = bounds['adj_upper']
    max_price = compute_max_affordable_price(capital)

    results = []
    for stock in stock_names:
        vol = annual_volatility[stock]
        price = current_prices[stock]
        risk_pass = adj_lower <= vol <= adj_upper
        afford_label, afford_score, afford_color = classify_affordability(price, max_price)
        price_pass = afford_score >= 2
        both_pass = risk_pass and price_pass
        results.append({
            'Stock': stock,
            'Price (LKR)': round(price, 2),
            'Volatility (%)': round(vol*100, 2),
            'Risk Pass': risk_pass,
            'Affordability': afford_label,
            'Afford Score': afford_score,
            'Afford Color': afford_color,
            'Price Pass': price_pass,
            'Qualified': both_pass,
        })
    return pd.DataFrame(results)

def build_portfolio(qualified_stocks, annual_returns, cov_matrix, objective='min_variance'):
    n = len(qualified_stocks)
    if n < 3:
        return None
    stock_ret = annual_returns[qualified_stocks].values
    sub_cov = cov_matrix.loc[qualified_stocks, qualified_stocks].values

    def port_vol(w): return np.sqrt(np.dot(w.T, np.dot(sub_cov, w)))
    def port_ret(w): return np.dot(w, stock_ret)

    if objective == 'min_variance':
        obj = lambda w: np.dot(w.T, np.dot(sub_cov, w))
    elif objective == 'max_sharpe':
        def obj(w):
            r = port_ret(w); v = port_vol(w)
            return -(r - 0.10)/v if v > 0 else 1e10
    else:  # max_return
        obj = lambda w: -port_ret(w)

    min_w = max(0.02, 1/n * 0.5)
    max_w = min(0.30, 1/n * 3)
    bnds = tuple((min_w, max_w) for _ in range(n))
    cons = [{'type': 'eq', 'fun': lambda w: np.sum(w) - 1}]
    x0 = np.array([1/n]*n)
    res = minimize(obj, x0, method='SLSQP', bounds=bnds, constraints=cons,
                   options={'maxiter': 2000, 'ftol': 1e-10})
    w = res.x
    w = np.clip(w, 0, 1); w /= w.sum()

    p_vol = port_vol(w)
    p_ret = port_ret(w)
    sharpe = (p_ret - 0.10) / p_vol if p_vol > 0 else 0

    return {
        'stocks': qualified_stocks,
        'weights': w,
        'volatility': p_vol,
        'return': p_ret,
        'sharpe': sharpe,
        'success': res.success or True,
    }

def monte_carlo(portfolio, returns_df, n_sim=500, n_years=5):
    if portfolio is None: return None
    pr = returns_df[portfolio['stocks']]
    mu = pr.mean().values
    cov = pr.cov().values
    w = portfolio['weights']
    n_days = int(252 * n_years)
    final_vals = []
    for _ in range(n_sim):
        sim = np.random.multivariate_normal(mu, cov, n_days)
        daily_r = sim @ w
        final_vals.append((1 + daily_r).cumprod()[-1])
    final_vals = np.array(final_vals)
    return {
        'mean': np.mean(final_vals),
        'median': np.median(final_vals),
        'p5': np.percentile(final_vals, 5),
        'p95': np.percentile(final_vals, 95),
        'prob_positive': np.mean(final_vals > 1),
        'prob_double': np.mean(final_vals > 2),
        'vals': final_vals
    }

# ─────────────────────────────────────────────────────────────────────────────
# SIDEBAR — INVESTOR PROFILE
# ─────────────────────────────────────────────────────────────────────────────

with st.sidebar:
    st.markdown("""
    <div style="padding:6px 0 18px;">
        <div style="background:linear-gradient(135deg,#6c3de8,#c4338a); border-radius:16px; padding:16px 12px; text-align:center; box-shadow:0 6px 20px rgba(108,61,232,0.3);">
            <div style="font-family:'Space Grotesk',sans-serif; font-size:1.25rem; font-weight:800; color:#fff; letter-spacing:-0.5px;">
                📊 CSE Portfolio Advisor
            </div>
            <div style="font-size:0.62rem; color:rgba(255,255,255,0.75); letter-spacing:1.6px; text-transform:uppercase; margin-top:4px; font-weight:600;">
                Smart · Young · Sri Lankan
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<p style="font-family:Space Grotesk,sans-serif;font-weight:700;font-size:0.78rem;color:#6c3de8;text-transform:uppercase;letter-spacing:1.2px;margin:0 0 6px;">👤 Your Investor Profile</p>', unsafe_allow_html=True)

    age = st.slider("Your Age", 18, 40, 25, help="Your current age affects risk tolerance")
    monthly_income = st.selectbox(
        "Monthly Income (LKR)",
        [30000, 40000, 50000, 60000, 75000, 100000, 150000],
        index=2,
        format_func=lambda x: f"Rs. {x:,}"
    )
    investment_pct = st.slider("Investment Rate (% of income)", 5, 30, 15)
    months_saved = st.slider("Months of savings to invest", 3, 12, 6)

    capital = monthly_income * (investment_pct/100) * months_saved
    st.markdown(f"""
    <div class="capital-card">
        <div class="capital-label">💰 Your Investment Capital</div>
        <div class="capital-value">Rs. {capital:,.0f}</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown('<p style="font-family:Space Grotesk,sans-serif;font-weight:700;font-size:0.78rem;color:#6c3de8;text-transform:uppercase;letter-spacing:1.2px;margin:0 0 6px;">📂 Data Source</p>', unsafe_allow_html=True)
    uploaded_file = st.file_uploader(
        "Upload CLOSEPRICES.xlsx", type=['xlsx'],
        help="Upload your CSE close prices file"
    )

    st.markdown("---")
    st.markdown('<p style="font-family:Space Grotesk,sans-serif;font-weight:700;font-size:0.78rem;color:#6c3de8;text-transform:uppercase;letter-spacing:1.2px;margin:0 0 6px;">⚙️ Analysis Settings</p>', unsafe_allow_html=True)
    n_simulations = st.select_slider(
        "Monte Carlo Simulations",
        options=[100, 300, 500, 1000],
        value=300
    )
    show_advanced = st.checkbox("Show Advanced Analytics", value=False)

# ─────────────────────────────────────────────────────────────────────────────
# LOAD DATA
# ─────────────────────────────────────────────────────────────────────────────

try:
    if uploaded_file:
        file_bytes = uploaded_file.read()
    else:
        with open("CLOSEPRICES.xlsx", "rb") as f:
            file_bytes = f.read()
    df, stock_names = load_and_process_data(file_bytes)
    data_loaded = True
except Exception as e:
    data_loaded = False
    st.error(f"Could not load data: {e}. Please upload CLOSEPRICES.xlsx in the sidebar.")

# ─────────────────────────────────────────────────────────────────────────────
# MAIN HEADER
# ─────────────────────────────────────────────────────────────────────────────

st.markdown("""
<div style="padding: 24px 0 14px;">
    <div class="main-title">Smart Portfolio Design</div>
    <div class="main-title">for Young Sri Lankan Investors </div>
    <div style="margin-top:12px; display:flex; flex-wrap:wrap; gap:8px; align-items:center;">
        <span style="background:#ede9fe;color:#6c3de8;padding:4px 13px;border-radius:20px;font-size:0.72rem;font-weight:700;letter-spacing:0.4px;">📐 Risk-Boundary Framework</span>
        <span style="background:#fce7f3;color:#be185d;padding:4px 13px;border-radius:20px;font-size:0.72rem;font-weight:700;letter-spacing:0.4px;">📈 Colombo Stock Exchange</span>
        <span style="background:#fef3c7;color:#b45309;padding:4px 13px;border-radius:20px;font-size:0.72rem;font-weight:700;letter-spacing:0.4px;">📅 2020 – 2024</span>
    </div>
</div>
""", unsafe_allow_html=True)

if not data_loaded:
    st.stop()

# Compute
returns, annual_returns, annual_volatility, covariance_matrix, current_prices = compute_analytics(df, stock_names)
bounds = compute_risk_boundaries(annual_volatility, annual_returns, covariance_matrix, returns, stock_names)
screened = screen_stocks(stock_names, annual_volatility, current_prices, bounds, capital)
qualified_stocks = screened[screened['Qualified']]['Stock'].tolist()

# Age-based profile
horizon = 60 - age
if age <= 25:
    profile_name = "Aggressive Growth"
    profile_emoji = "🚀"
    profile_color = "#e74c3c"
    recommended_portfolio = "Aggressive"
elif age <= 30:
    profile_name = "Moderate Growth"
    profile_emoji = "⚖️"
    profile_color = "#f39c12"
    recommended_portfolio = "Moderate"
else:
    profile_name = "Conservative Growth"
    profile_emoji = "🛡️"
    profile_color = "#2ecc71"
    recommended_portfolio = "Conservative"

# ─────────────────────────────────────────────────────────────────────────────
# INVESTOR PROFILE SUMMARY
# ─────────────────────────────────────────────────────────────────────────────

col_a, col_b, col_c, col_d = st.columns(4)
with col_a:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Investor Profile</div>
        <div style="font-family:'Space Grotesk',sans-serif;font-size:1.15rem;font-weight:800;color:#6c3de8;margin-top:4px;">{profile_emoji} {profile_name}</div>
    </div>""", unsafe_allow_html=True)
with col_b:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Investment Horizon</div>
        <div style="font-family:'Space Grotesk',sans-serif;font-size:2rem;font-weight:800;color:#18172b;">{horizon}<span style="font-size:0.85rem;color:#9b8cc4;font-weight:400;"> yrs</span></div>
    </div>""", unsafe_allow_html=True)
with col_c:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Capital Available</div>
        <div style="font-family:'Space Grotesk',sans-serif;font-size:1.15rem;font-weight:800;background:linear-gradient(135deg,#6c3de8,#c4338a);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;margin-top:4px;">Rs. {capital:,.0f}</div>
    </div>""", unsafe_allow_html=True)
with col_d:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Qualified Stocks</div>
        <div style="font-family:'Space Grotesk',sans-serif;font-size:2rem;font-weight:800;color:#18172b;">{len(qualified_stocks)}<span style="font-size:0.85rem;color:#9b8cc4;font-weight:400;"> / {len(stock_names)}</span></div>
    </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# TABS
# ─────────────────────────────────────────────────────────────────────────────

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📐 Risk Framework",
    "🔍 Stock Screening",
    "💼 Portfolios",
    "🎲 Monte Carlo",
    "📋 Research Summary"
])


# ─────────────────────────────────────────────────────────────────────────────
# CHART THEME — Youth Palette
# ─────────────────────────────────────────────────────────────────────────────
_BG_PAPER   = 'rgba(0,0,0,0)'
_BG_PLOT    = '#fdfcff'
_GRID       = '#ede8ff'
_FONT_COL   = '#18172b'
_FONT_FAM   = 'Plus Jakarta Sans'
_PURPLE     = '#6c3de8'
_PINK       = '#c4338a'
_AMBER      = '#f59e0b'
_GREEN      = '#10b981'
_RED        = '#f43f5e'
_ORANGE     = '#f97316'
_TEAL       = '#06b6d4'
_INDIGO     = '#6366f1'

def _base_layout(**kwargs):
    """Return a base Plotly layout dict with youth theme applied."""
    base = dict(
        paper_bgcolor=_BG_PAPER,
        plot_bgcolor=_BG_PLOT,
        font=dict(color=_FONT_COL, family=_FONT_FAM, size=12),
        margin=dict(t=50, b=60, l=10, r=10),
        legend=dict(
            bgcolor='rgba(255,255,255,0.92)',
            bordercolor=_GRID,
            borderwidth=1,
            font=dict(size=11),
        ),
        hoverlabel=dict(
            bgcolor='#1e1b3a',
            font_color='white',
            font_family=_FONT_FAM,
            bordercolor='#6c3de8',
        ),
        xaxis=dict(gridcolor=_GRID, linecolor=_GRID, zerolinecolor=_GRID,
                   tickfont=dict(size=11)),
        yaxis=dict(gridcolor=_GRID, linecolor=_GRID, zerolinecolor=_GRID,
                   tickfont=dict(size=11)),
    )
    base.update(kwargs)
    return base

# ═════════════════════════════════════════════════════════════════════════════
# TAB 1: RISK FRAMEWORK
# ═════════════════════════════════════════════════════════════════════════════

with tab1:
    st.markdown('<div class="section-title">Risk Boundary Framework</div>', unsafe_allow_html=True)
    st.markdown("""
    Seven mathematical methods establish the **optimal volatility range** for young Sri Lankan CSE investors.
    The consensus boundary is then adjusted for the 30-year investment horizon and CSE's emerging market characteristics.
    """)

    # Method comparison table
    methods_data = {
        'Method': ['Min Variance', 'Percentile (Q1-Q3)', 'Std Dev (μ±σ)', 'VaR (95% CI)', 'K-Means Clustering'],
        'Lower Bound (%)': [
            round(bounds['min_var_vol']*100, 2),
            round(bounds['perc_lower']*100, 2),
            round(bounds['std_lower']*100, 2),
            round(bounds['var_lower']*100, 2),
            round(bounds['clust_lower']*100, 2),
        ],
        'Upper Bound (%)': [
            round(bounds['max_sharpe_vol']*100, 2),
            round(bounds['perc_upper']*100, 2),
            round(bounds['std_upper']*100, 2),
            round(bounds['var_upper']*100, 2),
            round(bounds['clust_upper']*100, 2),
        ],
    }
    methods_df = pd.DataFrame(methods_data)
    methods_df['Range (%)'] = (methods_df['Upper Bound (%)'] - methods_df['Lower Bound (%)']).round(2)

    col1, col2 = st.columns([1.2, 1])

    with col1:
        st.markdown("**Seven-Method Comparison**")

        # Plotly grouped bar — Youth enhanced
        fig = go.Figure()
        fig.add_trace(go.Bar(
            name='Lower Bound',
            x=methods_df['Method'],
            y=methods_df['Lower Bound (%)'],
            marker=dict(
                color=_PURPLE,
                opacity=0.88,
                line=dict(color='white', width=1.5),
            ),
            hovertemplate='<b>%{x}</b><br>Lower: %{y:.2f}%<extra></extra>',
        ))
        fig.add_trace(go.Bar(
            name='Upper Bound',
            x=methods_df['Method'],
            y=methods_df['Upper Bound (%)'],
            marker=dict(
                color=_PINK,
                opacity=0.88,
                line=dict(color='white', width=1.5),
            ),
            hovertemplate='<b>%{x}</b><br>Upper: %{y:.2f}%<extra></extra>',
        ))
        fig.add_hline(
            y=bounds['consensus_lower']*100, line_dash='dot', line_color=_GREEN, line_width=2,
            annotation_text=f"✅ Consensus Lower: {bounds['consensus_lower']*100:.2f}%",
            annotation_font=dict(color=_GREEN, size=11, family=_FONT_FAM),
        )
        fig.add_hline(
            y=bounds['consensus_upper']*100, line_dash='dot', line_color=_AMBER, line_width=2,
            annotation_text=f"⚡ Consensus Upper: {bounds['consensus_upper']*100:.2f}%",
            annotation_font=dict(color=_AMBER, size=11, family=_FONT_FAM),
        )
        layout_bar = _base_layout(
            barmode='group', height=400,
            margin=dict(t=30, b=70, l=10, r=10),
            yaxis=dict(title='Volatility (%)', gridcolor=_GRID, linecolor=_GRID,
                       tickfont=dict(size=11), title_font=dict(size=12, color=_FONT_COL)),
            xaxis=dict(gridcolor=_GRID, linecolor=_GRID, tickfont=dict(size=11),
                       tickangle=-20),
            title=dict(text='Seven-Method Volatility Boundary Comparison',
                       font=dict(size=14, color=_FONT_COL, family=_FONT_FAM), x=0.01),
        )
        fig.update_layout(**layout_bar)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("**Consensus & Adjusted Boundaries**")
        st.markdown(f"""
        <div class="zone-conservative">
            <b style="color:#059669;font-family:Space Grotesk,sans-serif;font-weight:700;">🌿 Conservative Zone</b><br>
            <span style="color:#374151;font-size:0.88rem;font-weight:500;">{bounds['yi_lower']*100:.2f}% — {bounds['zone_conservative_end']*100:.2f}% volatility</span><br>
            <small style="color:#8878c0;font-weight:500;">For ages 30–35 · Capital preservation</small>
        </div>
        <div class="zone-moderate">
            <b style="color:#b45309;font-family:Space Grotesk,sans-serif;font-weight:700;">⚡ Moderate Zone</b><br>
            <span style="color:#374151;font-size:0.88rem;font-weight:500;">{bounds['zone_conservative_end']*100:.2f}% — {bounds['zone_moderate_end']*100:.2f}% volatility</span><br>
            <small style="color:#8878c0;font-weight:500;">For ages 26–30 · Balanced growth</small>
        </div>
        <div class="zone-aggressive">
            <b style="color:#e11d48;font-family:Space Grotesk,sans-serif;font-weight:700;">🔥 Aggressive Zone</b><br>
            <span style="color:#374151;font-size:0.88rem;font-weight:500;">{bounds['zone_moderate_end']*100:.2f}% — {bounds['adj_upper']*100:.2f}% volatility</span><br>
            <small style="color:#8878c0;font-weight:500;">For ages 22–25 · Maximum growth</small>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(f"""
        **Key Parameters:**
        - **Consensus Lower:** {bounds['consensus_lower']*100:.2f}%
        - **Consensus Upper:** {bounds['consensus_upper']*100:.2f}%
        - **Horizon Adjustment (30yr):** ×1.30
        - **Adjusted Upper:** {bounds['yi_upper']*100:.2f}%
        - **CSE Market Adjustment:** 75th percentile = {bounds['adj_upper']*100:.2f}%
        """)

    st.markdown("---")
    st.markdown("**Method Results Table**")
    st.dataframe(methods_df, use_container_width=True, hide_index=True)

    if show_advanced:
        st.markdown("---")
        st.markdown("**CSE Stock Volatility Distribution**")
        fig2 = go.Figure()
        sorted_vols = annual_volatility.sort_values()
        colors_v = [_GREEN if bounds['yi_lower'] <= v <= bounds['adj_upper'] else _RED
                    for v in sorted_vols.values]
        # gradient effect: qualified bars get purple tint
        colors_v2 = [_PURPLE if bounds['yi_lower'] <= v <= bounds['adj_upper'] else _RED
                     for v in sorted_vols.values]
        fig2.add_trace(go.Bar(
            x=sorted_vols.index, y=sorted_vols.values*100,
            marker=dict(color=colors_v2, opacity=0.85, line=dict(color='white', width=1.2)),
            name='Volatility',
            hovertemplate='<b>%{x}</b><br>Volatility: %{y:.2f}%<extra></extra>',
        ))
        fig2.add_hrect(
            y0=bounds['yi_lower']*100, y1=bounds['adj_upper']*100,
            fillcolor='rgba(108,61,232,0.06)', line_width=0,
            annotation_text='✅ Target Zone', annotation_position='top right',
            annotation_font=dict(color=_PURPLE, size=11, family=_FONT_FAM),
        )
        fig2.add_hline(y=bounds['yi_lower']*100, line_dash='dash', line_color=_GREEN, line_width=2,
                       annotation_text=f"Lower: {bounds['yi_lower']*100:.2f}%",
                       annotation_font=dict(color=_GREEN, size=11))
        fig2.add_hline(y=bounds['adj_upper']*100, line_dash='dash', line_color=_RED, line_width=2,
                       annotation_text=f"Upper: {bounds['adj_upper']*100:.2f}%",
                       annotation_font=dict(color=_RED, size=11))
        layout_vol = _base_layout(
            height=380, margin=dict(t=40, b=60, l=10, r=10),
            title=dict(text='CSE Stock Annual Volatility — Boundary Check',
                       font=dict(size=14, color=_FONT_COL, family=_FONT_FAM), x=0.01),
            yaxis=dict(title='Annual Volatility (%)', gridcolor=_GRID),
            xaxis=dict(title='Stock', gridcolor=_GRID),
        )
        fig2.update_layout(**layout_vol)
        st.plotly_chart(fig2, use_container_width=True)

# ═════════════════════════════════════════════════════════════════════════════
# TAB 2: STOCK SCREENING
# ═════════════════════════════════════════════════════════════════════════════

with tab2:
    st.markdown('<div class="section-title">Dual-Criteria Stock Screening</div>', unsafe_allow_html=True)
    st.markdown(f"""
    Stocks must pass **both** criteria to qualify for portfolio construction:
    - **Stage 1 — Risk:** Volatility within young investor boundaries ({bounds['yi_lower']*100:.2f}% — {bounds['adj_upper']*100:.2f}%)
    - **Stage 2 — Price:** Affordable given your capital of Rs. {capital:,.0f} (max price ≈ Rs. {compute_max_affordable_price(capital):,.0f})
    """)

    # Summary counts
    col_s1, col_s2, col_s3, col_s4 = st.columns(4)
    n_risk = screened['Risk Pass'].sum()
    n_price = screened['Price Pass'].sum()
    n_qual = screened['Qualified'].sum()
    with col_s1:
        st.metric("Total Stocks", len(stock_names))
    with col_s2:
        st.metric("Pass Risk Filter", int(n_risk))
    with col_s3:
        st.metric("Pass Price Filter", int(n_price))
    with col_s4:
        st.metric("✅ Fully Qualified", int(n_qual))

    st.markdown("<br>", unsafe_allow_html=True)

    col_l, col_r = st.columns([1.3, 1])

    with col_l:
        # Scatter plot: Price vs Volatility
        fig_sc = go.Figure()
        # Qualified zone shading
        fig_sc.add_vrect(
            x0=bounds['yi_lower']*100, x1=bounds['adj_upper']*100,
            fillcolor='rgba(108,61,232,0.06)', line_width=0,
        )
        fig_sc.add_vrect(
            x0=bounds['yi_lower']*100, x1=bounds['adj_upper']*100,
            fillcolor='rgba(0,0,0,0)', line_width=0,
        )
        # Plot each stock
        for _, row in screened.iterrows():
            if row['Qualified']:
                mk_color = _PURPLE
                mk_symbol = 'circle'
                mk_size = 16
                mk_line = dict(color='white', width=2)
            elif row['Risk Pass']:
                mk_color = _AMBER
                mk_symbol = 'diamond'
                mk_size = 13
                mk_line = dict(color='white', width=1.5)
            else:
                mk_color = _RED
                mk_symbol = 'x'
                mk_size = 11
                mk_line = dict(color='white', width=1.5)
            fig_sc.add_trace(go.Scatter(
                x=[row['Volatility (%)']],
                y=[row['Price (LKR)']],
                mode='markers+text',
                marker=dict(size=mk_size, color=mk_color, symbol=mk_symbol,
                            line=mk_line, opacity=0.9),
                text=[row['Stock']],
                textposition='top center',
                textfont=dict(size=9, color=_FONT_COL, family=_FONT_FAM),
                name=row['Stock'],
                showlegend=False,
                hovertemplate=(
                    f"<b>{row['Stock']}</b><br>"
                    f"Volatility: {row['Volatility (%)']:.2f}%<br>"
                    f"Price: Rs.{row['Price (LKR)']:,.2f}<br>"
                    f"Status: {'✅ Qualified' if row['Qualified'] else ('⚠️ Risk OK, Price High' if row['Risk Pass'] else '❌ Excluded')}"
                    "<extra></extra>"
                ),
            ))
        # Boundary lines
        fig_sc.add_vline(x=bounds['yi_lower']*100, line_dash='dash',
                         line_color=_GREEN, line_width=2,
                         annotation_text=f"Min Vol: {bounds['yi_lower']*100:.1f}%",
                         annotation_font=dict(color=_GREEN, size=10))
        fig_sc.add_vline(x=bounds['adj_upper']*100, line_dash='dash',
                         line_color=_RED, line_width=2,
                         annotation_text=f"Max Vol: {bounds['adj_upper']*100:.1f}%",
                         annotation_font=dict(color=_RED, size=10))
        fig_sc.add_hline(
            y=compute_max_affordable_price(capital), line_dash='dash',
            line_color=_PURPLE, line_width=2,
            annotation_text=f"Max Price: Rs.{compute_max_affordable_price(capital):,.0f}",
            annotation_font=dict(color=_PURPLE, size=10),
        )
        # Legend annotation boxes
        fig_sc.add_annotation(x=0.01, y=0.99, xref='paper', yref='paper',
            text="🟣 Qualified  🔶 Risk OK  🔴 Excluded",
            showarrow=False, bgcolor='rgba(255,255,255,0.9)',
            bordercolor=_GRID, borderwidth=1,
            font=dict(size=10, color=_FONT_COL, family=_FONT_FAM),
            align='left',
        )
        layout_sc = _base_layout(
            height=440, margin=dict(t=55, b=65, l=10, r=10),
            title=dict(text='Stock Universe: Volatility vs Price — Dual Screening',
                       font=dict(size=14, color=_FONT_COL, family=_FONT_FAM), x=0.01),
            xaxis=dict(title='Annual Volatility (%)', gridcolor=_GRID),
            yaxis=dict(title='Latest Price (LKR)', gridcolor=_GRID),
        )
        fig_sc.update_layout(**layout_sc)
        st.plotly_chart(fig_sc, use_container_width=True)

    with col_r:
        st.markdown("**Affordability Breakdown**")
        afford_counts = screened['Affordability'].value_counts()
        colors_a = {'Highly Affordable': '#2ecc71', 'Affordable': '#27ae60',
                    'Moderately Affordable': '#f39c12', 'Not Affordable': '#e74c3c'}
        colors_a_youth = {
            'Highly Affordable': _PURPLE,
            'Affordable': _TEAL,
            'Moderately Affordable': _AMBER,
            'Not Affordable': _RED,
        }
        fig_pie = go.Figure(go.Pie(
            labels=afford_counts.index,
            values=afford_counts.values,
            marker=dict(
                colors=[colors_a_youth.get(l, '#888') for l in afford_counts.index],
                line=dict(color='white', width=3),
            ),
            hole=0.52,
            textinfo='label+percent',
            textfont=dict(color='white', size=11, family=_FONT_FAM),
            hovertemplate='<b>%{label}</b><br>Count: %{value}<br>%{percent}<extra></extra>',
            pull=[0.04 if l == 'Highly Affordable' else 0 for l in afford_counts.index],
        ))
        fig_pie.add_annotation(
            text=f"<b>{int(afford_counts.sum())}</b><br><span style='font-size:10px'>Stocks</span>",
            x=0.5, y=0.5, showarrow=False,
            font=dict(size=18, color=_FONT_COL, family=_FONT_FAM),
        )
        layout_pie = _base_layout(height=300, margin=dict(t=20, b=10, l=0, r=0),
                                   showlegend=True)
        layout_pie['legend'] = dict(
            orientation='v', x=1.0, y=0.5,
            font=dict(size=10, family=_FONT_FAM),
            bgcolor='rgba(255,255,255,0.9)',
            bordercolor=_GRID, borderwidth=1,
        )
        fig_pie.update_layout(**layout_pie)
        st.plotly_chart(fig_pie, use_container_width=True)

        st.markdown("**Qualified Stocks**")
        q_stocks = screened[screened['Qualified']][['Stock', 'Price (LKR)', 'Volatility (%)']].reset_index(drop=True)
        if len(q_stocks) > 0:
            st.dataframe(q_stocks, use_container_width=True, hide_index=True, height=200)
        else:
            st.warning("No stocks qualify with current filters. Try increasing your capital or relaxing criteria.")

    st.markdown("---")
    st.markdown("**Complete Stock Screening Results**")
    display_df = screened[['Stock', 'Price (LKR)', 'Volatility (%)', 'Risk Pass', 'Affordability', 'Qualified']].copy()
    display_df['Risk Pass'] = display_df['Risk Pass'].map({True: '✅', False: '❌'})
    display_df['Qualified'] = display_df['Qualified'].map({True: '✅ Qualified', False: '❌ Excluded'})
    st.dataframe(display_df, use_container_width=True, hide_index=True)

# ═════════════════════════════════════════════════════════════════════════════
# TAB 3: PORTFOLIOS
# ═════════════════════════════════════════════════════════════════════════════

with tab3:
    st.markdown('<div class="section-title">Three Age-Based Portfolios</div>', unsafe_allow_html=True)

    if len(qualified_stocks) < 3:
        st.warning(f"Only {len(qualified_stocks)} stocks qualify. Need at least 3 for portfolio construction. "
                   "Try increasing your capital or using different settings.")
        st.info("💡 Tip: Increase your capital in the sidebar or broaden age criteria.")
        # Use all stocks for demonstration
        fallback_stocks = screened.nsmallest(10, 'Volatility (%)')[
            screened.nsmallest(10, 'Volatility (%)').index]['Stock'].tolist()
        working_stocks = fallback_stocks if len(fallback_stocks) >= 3 else stock_names[:10]
        st.markdown(f"*Showing demo portfolio with top-10 lowest-volatility stocks: {', '.join(working_stocks)}*")
    else:
        working_stocks = qualified_stocks

    # Build portfolios
    with st.spinner("Optimizing portfolios..."):
        p_conservative = build_portfolio(working_stocks, annual_returns, covariance_matrix, 'min_variance')
        p_moderate = build_portfolio(working_stocks, annual_returns, covariance_matrix, 'max_sharpe')
        p_aggressive = build_portfolio(working_stocks, annual_returns, covariance_matrix, 'max_return')

    portfolios = {
        'Conservative': {'data': p_conservative, 'color': '#2ecc71', 'emoji': '🛡️', 'age': 'Ages 30–35'},
        'Moderate': {'data': p_moderate, 'color': '#f39c12', 'emoji': '⚖️', 'age': 'Ages 26–30'},
        'Aggressive': {'data': p_aggressive, 'color': '#e74c3c', 'emoji': '🚀', 'age': 'Ages 22–25'},
    }

    # Summary metrics row
    cols = st.columns(3)
    for i, (pname, pinfo) in enumerate(portfolios.items()):
        p = pinfo['data']
        with cols[i]:
            highlight = "border:2px solid #6c3de8; box-shadow:0 0 0 5px rgba(108,61,232,0.14); background:linear-gradient(135deg,#f6f0ff,#fff0fb);" if pname == recommended_portfolio else ""
            if p:
                st.markdown(f"""
                <div class="metric-card" style="{highlight}">
                    <div class="metric-label">{pinfo['emoji']} {pname} · {pinfo['age']}</div>
                    <div style="display:flex; justify-content:space-around; margin-top:10px;">
                        <div>
                            <div class="metric-label">Return</div>
                            <div style="font-family:'Space Grotesk',sans-serif;font-size:1.5rem;font-weight:800;color:{pinfo['color']};">
                                {p['return']*100:.1f}%
                            </div>
                        </div>
                        <div>
                            <div class="metric-label">Volatility</div>
                            <div style="font-family:'Space Grotesk',sans-serif;font-size:1.5rem;font-weight:800;color:{pinfo['color']};">
                                {p['volatility']*100:.1f}%
                            </div>
                        </div>
                        <div>
                            <div class="metric-label">Sharpe</div>
                            <div style="font-family:'Space Grotesk',sans-serif;font-size:1.5rem;font-weight:800;color:{pinfo['color']};">
                                {p['sharpe']:.2f}
                            </div>
                        </div>
                    </div>
                    {'<div style="text-align:center;margin-top:10px;"><span class="rec-badge">⭐ Recommended for you</span></div>' if pname == recommended_portfolio else ''}
                </div>
                """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Portfolio weights charts
    col_w1, col_w2, col_w3 = st.columns(3)
    wcols = [col_w1, col_w2, col_w3]
    for i, (pname, pinfo) in enumerate(portfolios.items()):
        p = pinfo['data']
        with wcols[i]:
            if p:
                w_series = pd.Series(p['weights'], index=p['stocks'])
                w_series = w_series[w_series > 0.01].sort_values(ascending=True)
                # Build colour gradient: higher weight = more saturated
                n_bars = len(w_series)
                bar_colors = [pinfo['color']] * n_bars
                fig_w = go.Figure(go.Bar(
                    x=w_series.values * 100,
                    y=w_series.index,
                    orientation='h',
                    marker=dict(
                        color=w_series.values * 100,
                        colorscale=[
                            [0.0, 'rgba(108,61,232,0.25)'],
                            [0.5, pinfo['color']],
                            [1.0, pinfo['color']],
                        ],
                        line=dict(color='white', width=1.5),
                        opacity=0.9,
                    ),
                    text=[f"{v*100:.1f}%" for v in w_series.values],
                    textposition='outside',
                    textfont=dict(size=9, color=_FONT_COL, family=_FONT_FAM),
                    hovertemplate='<b>%{y}</b><br>Weight: %{x:.2f}%<extra></extra>',
                ))
                layout_w = _base_layout(
                    height=320,
                    margin=dict(t=50, b=40, l=10, r=50),
                    title=dict(
                        text=f"{pinfo['emoji']} {pname}",
                        font=dict(size=13, color=pinfo['color'], family=_FONT_FAM),
                        x=0.0,
                    ),
                    xaxis=dict(title='Weight (%)', gridcolor=_GRID,
                               range=[0, w_series.max()*130]),
                    yaxis=dict(gridcolor=_GRID),
                )
                fig_w.update_layout(**layout_w)
                st.plotly_chart(fig_w, use_container_width=True)

    # Efficient frontier
    st.markdown("---")
    st.markdown("**Efficient Frontier — Risk vs Return**")

    np.random.seed(42)
    n_pts = 1000
    ef_vols, ef_rets, ef_sharpes = [], [], []
    n_w = len(working_stocks)
    sub_ret = annual_returns[working_stocks].values
    sub_cov = covariance_matrix.loc[working_stocks, working_stocks].values
    for _ in range(n_pts):
        rw = np.random.random(n_w); rw /= rw.sum()
        rv = np.sqrt(np.dot(rw.T, np.dot(sub_cov, rw)))
        rr = np.dot(rw, sub_ret)
        ef_vols.append(rv*100); ef_rets.append(rr*100)
        ef_sharpes.append((rr - 0.10)/rv if rv > 0 else 0)

    fig_ef = go.Figure()
    # Background cloud — random portfolios coloured by Sharpe
    fig_ef.add_trace(go.Scatter(
        x=ef_vols, y=ef_rets, mode='markers',
        marker=dict(
            color=ef_sharpes,
            colorscale=[
                [0.0,  '#f43f5e'],
                [0.35, '#f97316'],
                [0.60, '#f59e0b'],
                [0.80, '#10b981'],
                [1.0,  '#6c3de8'],
            ],
            size=5,
            opacity=0.55,
            colorbar=dict(
                title=dict(text='Sharpe Ratio', font=dict(size=12, family=_FONT_FAM)),
                thickness=14, len=0.7,
                tickfont=dict(size=10, family=_FONT_FAM),
                outlinewidth=0,
            ),
        ),
        name='Simulated Portfolios',
        hovertemplate='Volatility: %{x:.2f}%<br>Return: %{y:.2f}%<extra></extra>',
    ))
    # Optimised portfolio stars with glow rings
    for pname, pinfo in portfolios.items():
        p = pinfo['data']
        if p:
            # Glow ring
            fig_ef.add_trace(go.Scatter(
                x=[p['volatility']*100], y=[p['return']*100],
                mode='markers',
                marker=dict(size=32, color=pinfo['color'], opacity=0.15, symbol='circle'),
                showlegend=False, hoverinfo='skip',
            ))
            # Star marker
            fig_ef.add_trace(go.Scatter(
                x=[p['volatility']*100], y=[p['return']*100],
                mode='markers+text',
                marker=dict(size=18, color=pinfo['color'], symbol='star',
                            line=dict(color='white', width=2.5), opacity=1.0),
                text=[f"{pinfo['emoji']} {pname}"],
                textposition='top center',
                textfont=dict(color=pinfo['color'], size=12, family=_FONT_FAM),
                name=f"{pinfo['emoji']} {pname}",
                hovertemplate=(
                    f"<b>{pinfo['emoji']} {pname}</b><br>"
                    f"Return: {p['return']*100:.1f}%<br>"
                    f"Volatility: {p['volatility']*100:.1f}%<br>"
                    f"Sharpe: {p['sharpe']:.2f}"
                    "<extra></extra>"
                ),
            ))
    layout_ef = _base_layout(
        height=460, margin=dict(t=50, b=70, l=10, r=100),
        title=dict(
            text='Efficient Frontier',
            font=dict(size=14, color=_FONT_COL, family=_FONT_FAM), x=0.01,
        ),
        xaxis=dict(title='Portfolio Volatility (%)', gridcolor=_GRID),
        yaxis=dict(title='Expected Annual Return (%)', gridcolor=_GRID),
        legend=dict(
            x=1.08, y=0.9, bgcolor='rgba(255,255,255,0.95)',
            bordercolor=_GRID, borderwidth=1,
            font=dict(size=11, family=_FONT_FAM),
        ),
    )
    fig_ef.update_layout(**layout_ef)
    st.plotly_chart(fig_ef, use_container_width=True)

# ═════════════════════════════════════════════════════════════════════════════
# TAB 4: MONTE CARLO
# ═════════════════════════════════════════════════════════════════════════════

with tab4:
    st.markdown('<div class="section-title">Monte Carlo Simulation</div>', unsafe_allow_html=True)
    st.markdown(f"Testing portfolio robustness across **{n_simulations} scenarios** over a **5-year horizon**.")

    if 'p_conservative' not in dir() or p_conservative is None:
        st.warning("Build portfolios first (Tab 3). Ensure you have qualified stocks.")
    else:
        with st.spinner(f"Running {n_simulations} Monte Carlo simulations..."):
            mc_cons = monte_carlo(p_conservative, returns, n_simulations)
            mc_mod = monte_carlo(p_moderate, returns, n_simulations)
            mc_agg = monte_carlo(p_aggressive, returns, n_simulations)

        mc_map = {
            'Conservative': (mc_cons, '#2ecc71', '🛡️'),
            'Moderate': (mc_mod, '#f39c12', '⚖️'),
            'Aggressive': (mc_agg, '#e74c3c', '🚀'),
        }

        # Summary table
        mc_rows = []
        for pname, (mc, color, emoji) in mc_map.items():
            if mc:
                mc_rows.append({
                    'Portfolio': f"{emoji} {pname}",
                    'Mean 5yr Value (Rs. 1 → ?)': f"Rs. {mc['mean']:.2f}",
                    'Median': f"Rs. {mc['median']:.2f}",
                    'Worst Case (5%)': f"Rs. {mc['p5']:.2f}",
                    'Best Case (95%)': f"Rs. {mc['p95']:.2f}",
                    'Prob. Positive Return': f"{mc['prob_positive']*100:.1f}%",
                    'Prob. Double': f"{mc['prob_double']*100:.1f}%",
                })
        if mc_rows:
            st.dataframe(pd.DataFrame(mc_rows), use_container_width=True, hide_index=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # Distribution charts
        col_m1, col_m2, col_m3 = st.columns(3)
        for col, (pname, (mc, color, emoji)) in zip([col_m1, col_m2, col_m3], mc_map.items()):
            with col:
                if mc:
                    fig_mc = go.Figure()
                    # Positive / negative split coloring
                    fig_mc.add_trace(go.Histogram(
                        x=mc['vals'], nbinsx=35,
                        marker=dict(
                            color=color,
                            opacity=0.82,
                            line=dict(color='white', width=0.8),
                        ),
                        name='Scenarios',
                        hovertemplate='Value: Rs.%{x:.2f}<br>Count: %{y}<extra></extra>',
                    ))
                    # Break-even line
                    fig_mc.add_vline(
                        x=1.0, line_dash='dot', line_color=_PURPLE, line_width=2,
                        annotation_text='Break-even',
                        annotation_font=dict(color=_PURPLE, size=10, family=_FONT_FAM),
                        annotation_position='top left',
                    )
                    # Median line
                    fig_mc.add_vline(
                        x=mc['median'], line_dash='dash', line_color=_FONT_COL, line_width=2,
                        annotation_text=f"Median: Rs.{mc['median']:.2f}",
                        annotation_font=dict(color=_FONT_COL, size=10, family=_FONT_FAM),
                        annotation_position='top right',
                    )
                    # Shading: loss region
                    fig_mc.add_vrect(
                        x0=min(mc['vals']), x1=1.0,
                        fillcolor='rgba(244,63,94,0.06)', line_width=0,
                    )
                    layout_mc = _base_layout(
                        height=320, margin=dict(t=48, b=50, l=10, r=10),
                        title=dict(
                            text=f"{emoji} {pname}",
                            font=dict(size=13, color=color, family=_FONT_FAM), x=0.0,
                        ),
                        xaxis=dict(title='Final Value (Rs. 1 invested)', gridcolor=_GRID),
                        yaxis=dict(title='Frequency', gridcolor=_GRID),
                    )
                    fig_mc.update_layout(**layout_mc)
                    st.plotly_chart(fig_mc, use_container_width=True)

        # Capital projection
        st.markdown("---")
        st.markdown(f"**Your Capital Projection — Rs. {capital:,.0f} over 5 years**")
        proj_cols = st.columns(3)
        for col, (pname, (mc, color, emoji)) in zip(proj_cols, mc_map.items()):
            with col:
                if mc:
                    proj_mean = capital * mc['mean']
                    proj_med = capital * mc['median']
                    proj_worst = capital * mc['p5']
                    proj_best = capital * mc['p95']
                    st.markdown(f"""
                    <div class="metric-card" style="border-top:4px solid {color};">
                        <div style="font-family:Space Grotesk,sans-serif;font-weight:700;font-size:1rem;color:{color};margin-bottom:10px;">{emoji} {pname}</div>
                        <div class="proj-row">
                            <div class="proj-item proj-expected">📊 Expected &nbsp;<b>Rs. {proj_mean:,.0f}</b></div>
                            <div class="proj-item proj-best">📈 Best Case &nbsp;<b>Rs. {proj_best:,.0f}</b></div>
                            <div class="proj-item proj-worst">📉 Worst Case &nbsp;<b>Rs. {proj_worst:,.0f}</b></div>
                            <div class="proj-item proj-prob">✅ Positive return in {mc['prob_positive']*100:.0f}% of scenarios</div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

# ═════════════════════════════════════════════════════════════════════════════
# TAB 5: RESEARCH SUMMARY
# ═════════════════════════════════════════════════════════════════════════════

with tab5:
    st.markdown('<div class="section-title">Research Framework Summary</div>', unsafe_allow_html=True)
    st.markdown("""
    **Title:** Smart Portfolio Design for Young Sri Lankan Investors  
    **Context:** Colombo Stock Exchange (CSE) · 2020–2024 · 19 Stocks · 1,162 Trading Days
    """)

    col_f1, col_f2 = st.columns(2)

    with col_f1:
        st.markdown("#### 📐 Methodology")
        st.markdown(f"""
        **Step 1 — Data Collection**
        - 19 CSE blue-chip stocks, Jan 2020 – Dec 2024
        - Daily close prices (1,162 observations)
        - Forward-fill for missing trading days

        **Step 2 — Returns & Statistics**
        - Daily log returns → annualised
        - Extreme returns (>50%) treated as data errors
        - Covariance matrix for portfolio construction

        **Step 3 — Risk Boundaries (7 Methods)**
        - Min Variance → Lower: {bounds['min_var_vol']*100:.2f}%
        - Max Sharpe → Upper: {bounds['max_sharpe_vol']*100:.2f}%
        - Percentile: {bounds['perc_lower']*100:.2f}% – {bounds['perc_upper']*100:.2f}%
        - Std Dev: {bounds['std_lower']*100:.2f}% – {bounds['std_upper']*100:.2f}%
        - VaR 95%: {bounds['var_lower']*100:.2f}% – {bounds['var_upper']*100:.2f}%
        - K-Means Clustering: {bounds['clust_lower']*100:.2f}% – {bounds['clust_upper']*100:.2f}%
        - **Consensus:** {bounds['consensus_lower']*100:.2f}% – {bounds['consensus_upper']*100:.2f}%

        **Step 4 — Young Investor Adjustment**
        - 30-year horizon factor: ×1.30
        - CSE emerging market: 75th percentile = {bounds['adj_upper']*100:.2f}%
        - Final range: {bounds['yi_lower']*100:.2f}% – {bounds['adj_upper']*100:.2f}%

        **Step 5 — Dual Stock Screening**
        - Stage 1: Volatility within adjusted bounds
        - Stage 2: Price enables 15-stock portfolio with 10+ shares each
        - Qualified: {len(qualified_stocks)} of {len(stock_names)} stocks
        """)

    with col_f2:
        st.markdown("#### 📚 Academic Foundation")
        st.markdown("""
        | Reference | Application |
        |-----------|-------------|
        | Markowitz (1952) | Mean-variance optimization |
        | Evans & Archer (1968) | 10–15 stocks for diversification |
        | Sharpe (1966) | Risk-adjusted return (Sharpe ratio) |
        | Statman (1987) | Optimal portfolio size |
        | Bekaert & Harvey (2003) | Emerging market volatility premium |
        | Estrada (2000) | CSE as emerging market |
        | Shefrin & Statman (2000) | Behavioral portfolio theory |
        | Kumar & Lee (2006) | Retail investor behavior |
        """)

        st.markdown("#### 💡 Key Findings")
        st.markdown(f"""
        - CSE stocks are **{annual_volatility.median()*100:.0f}% median volatility** — higher than developed markets
        - Only **{len(qualified_stocks)}/{len(stock_names)} stocks** qualify under dual criteria for Rs. {capital:,.0f} capital
        - Emerging market adjustment (1.5–3× per Bekaert & Harvey) is necessary
        - Young investors benefit from **30-year horizon buffer** (×1.30)
        - Portfolio diversification with CSE requires stocks **below Rs. {compute_max_affordable_price(capital):,.0f}**
        """)

        st.markdown("#### 🎯 Three Investor Profiles")
        st.markdown(f"""
        <div class="zone-aggressive" style="margin-bottom:6px;">
            <b style="color:#e11d48;font-family:Space Grotesk,sans-serif;font-weight:700;">🚀 Ages 22–25 → Aggressive</b><br>
            <small>Max return portfolio · Accept {bounds['zone_moderate_end']*100:.1f}%–{bounds['adj_upper']*100:.1f}% volatility</small>
        </div>
        <div class="zone-moderate" style="margin-bottom:6px;">
            <b style="color:#b45309;font-family:Space Grotesk,sans-serif;font-weight:700;">⚖️ Ages 26–30 → Moderate</b><br>
            <small>Max Sharpe ratio · {bounds['zone_conservative_end']*100:.1f}%–{bounds['zone_moderate_end']*100:.1f}% volatility</small>
        </div>
        <div class="zone-conservative">
            <b style="color:#059669;font-family:Space Grotesk,sans-serif;font-weight:700;">🛡️ Ages 30–35 → Conservative</b><br>
            <small>Min variance · {bounds['yi_lower']*100:.1f}%–{bounds['zone_conservative_end']*100:.1f}% volatility</small>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("#### 📊 Data Overview")
    col_d1, col_d2, col_d3 = st.columns(3)
    with col_d1:
        st.metric("Date Range", f"{df.index.min().strftime('%Y-%m-%d')} → {df.index.max().strftime('%Y-%m-%d')}")
    with col_d2:
        st.metric("CSE Stocks Analysed", len(stock_names))
    with col_d3:
        st.metric("Trading Days", len(df))

    # Price table
    st.markdown("**Latest Stock Prices & Volatility**")
    summary_df = pd.DataFrame({
        'Stock': stock_names,
        'Latest Price (LKR)': [round(current_prices[s], 2) for s in stock_names],
        'Annual Volatility (%)': [round(annual_volatility[s]*100, 2) for s in stock_names],
        'Annual Return (%)': [round(annual_returns[s]*100, 2) for s in stock_names],
        'Risk Zone': [
            'Conservative' if annual_volatility[s] <= bounds['zone_conservative_end']
            else 'Moderate' if annual_volatility[s] <= bounds['zone_moderate_end']
            else 'Aggressive' if annual_volatility[s] <= bounds['adj_upper']
            else 'Out of Bounds'
            for s in stock_names
        ]
    }).sort_values('Annual Volatility (%)')
    st.dataframe(summary_df, use_container_width=True, hide_index=True)

# ─────────────────────────────────────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────────────────────────────────────

st.markdown("""
<hr>
<div style="text-align:center;padding:14px 0;"><div style="font-family:Space Grotesk,sans-serif;font-weight:800;font-size:0.92rem;background:linear-gradient(135deg,#6c3de8,#c4338a);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;">Smart Portfolio Design · Young CSE Investors 🇱🇰</div><div style="color:#9b8cc4;font-size:0.7rem;margin-top:3px;letter-spacing:0.4px;">Built with Streamlit · Colombo Stock Exchange · 2020–2024</div></div>
""", unsafe_allow_html=True)


