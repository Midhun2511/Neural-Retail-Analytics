import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_absolute_error, r2_score, mean_squared_error
from streamlit_option_menu import option_menu
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# ============================================================
# PAGE CONFIGURATION
# ============================================================
st.set_page_config(
    page_title="Neural Retail Analytics Intelligence Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# ADVANCED CUSTOM CSS STYLING
# ============================================================
st.markdown("""
<style>
    /* Main Background */
    .stApp {
        background: #0F172A;
    }
    
    /* Hide Streamlit Branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Text Colors */
    h1, h2, h3, h4, h5, p, label, div, span {
        color: #FFFFFF !important;
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0F172A 0%, #1E293B 100%);
        border-right: 1px solid rgba(59, 130, 246, 0.2);
        padding-top: 20px;
    }
    
    [data-testid="stSidebar"] .stSelectbox label,
    [data-testid="stSidebar"] .stSlider label,
    [data-testid="stSidebar"] .stMultiSelect label,
    [data-testid="stSidebar"] .stDateInput label {
        color: #94A3B8 !important;
        font-weight: 500 !important;
        font-size: 14px !important;
    }
    
    /* Metric Cards */
    .metric-card {
        padding: 20px 15px;
        border-radius: 16px;
        text-align: center;
        box-shadow: 0 4px 20px rgba(0,0,0,0.3);
        transition: all 0.3s ease;
        border: 1px solid rgba(255,255,255,0.05);
        position: relative;
        overflow: hidden;
    }
    
    .metric-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 8px 30px rgba(0,0,0,0.4);
    }
    
    .metric-card .icon {
        font-size: 28px;
        margin-bottom: 8px;
        display: block;
    }
    
    .metric-card h4 {
        margin: 0;
        font-size: 13px;
        font-weight: 400;
        opacity: 0.8;
        letter-spacing: 0.5px;
        text-transform: uppercase;
    }
    
    .metric-card h2 {
        margin: 8px 0 0 0;
        font-size: 28px;
        font-weight: 700;
        letter-spacing: -0.5px;
    }
    
    .metric-card .change {
        font-size: 12px;
        margin-top: 6px;
        opacity: 0.7;
    }
    
    /* Glass Cards */
    .glass-card {
        background: rgba(30, 41, 59, 0.5);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border: 1px solid rgba(255,255,255,0.05);
        border-radius: 16px;
        padding: 20px;
        margin: 10px 0;
        box-shadow: 0 4px 20px rgba(0,0,0,0.2);
    }
    
    /* Info Boxes */
    .info-box {
        background: linear-gradient(135deg, rgba(30, 58, 95, 0.6), rgba(37, 99, 235, 0.1));
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        padding: 20px;
        border-radius: 16px;
        border-left: 4px solid #3B82F6;
        margin: 10px 0;
        border: 1px solid rgba(59, 130, 246, 0.2);
    }
    
    .info-box h4 {
        margin: 0 0 10px 0;
        color: #60A5FA !important;
        font-weight: 600;
    }
    
    .info-box p, .info-box li {
        color: #E2E8F0 !important;
        line-height: 1.6;
    }
    
    .success-box {
        background: linear-gradient(135deg, rgba(6, 78, 59, 0.6), rgba(16, 185, 129, 0.1));
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        padding: 20px;
        border-radius: 16px;
        border-left: 4px solid #10B981;
        margin: 10px 0;
        border: 1px solid rgba(16, 185, 129, 0.2);
    }
    
    .success-box h4 {
        margin: 0 0 10px 0;
        color: #34D399 !important;
        font-weight: 600;
    }
    
    .warning-box {
        background: linear-gradient(135deg, rgba(120, 53, 15, 0.6), rgba(245, 158, 11, 0.1));
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        padding: 20px;
        border-radius: 16px;
        border-left: 4px solid #F59E0B;
        margin: 10px 0;
        border: 1px solid rgba(245, 158, 11, 0.2);
    }
    
    .warning-box h4 {
        margin: 0 0 10px 0;
        color: #FBBF24 !important;
        font-weight: 600;
    }
    
    /* Dataframe */
    .stDataFrame {
        background: #1E293B;
        border-radius: 16px;
        padding: 10px;
        border: 1px solid rgba(255,255,255,0.05);
    }
    
    /* Download Button */
    .stDownloadButton button {
        background: linear-gradient(135deg, #2563EB, #1D4ED8) !important;
        color: white !important;
        border-radius: 10px !important;
        font-weight: 600 !important;
        padding: 10px 24px !important;
        border: none !important;
        transition: all 0.3s ease !important;
    }
    
    .stDownloadButton button:hover {
        transform: scale(1.02);
        box-shadow: 0 4px 20px rgba(37, 99, 235, 0.4) !important;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: rgba(30, 41, 59, 0.5);
        border-radius: 10px;
        padding: 8px 20px;
        border: 1px solid rgba(255,255,255,0.05);
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background: rgba(37, 99, 235, 0.2);
    }
    
    .stTabs [aria-selected="true"] {
        background: #2563EB !important;
        color: white !important;
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        background: rgba(30, 41, 59, 0.5);
        border-radius: 10px;
        border: 1px solid rgba(255,255,255,0.05);
    }
    
    /* Divider */
    hr {
        border-color: rgba(255,255,255,0.05) !important;
        margin: 24px 0;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================
# HEADER
# ============================================================
st.markdown("""
<div style="text-align:center;padding:10px 0 20px 0;">
    <h1 style="font-size:3rem;font-weight:800;background:linear-gradient(135deg,#60A5FA,#3B82F6,#2563EB);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;margin:0;">
        🧠 Neural Retail Analytics
    </h1>
    <p style="font-size:1.1rem;color:#94A3B8;margin-top:4px;font-weight:300;letter-spacing:1px;">
        INTELLIGENCE DASHBOARD · SALES · CUSTOMERS · FORECASTING · INVENTORY
    </p>
</div>
""", unsafe_allow_html=True)

st.divider()

# ============================================================
# DATA LOADING
# ============================================================
@st.cache_data
def load_data():
    try:
        df = pd.read_csv("data/featured_retail_data.csv")
    except:
        # Create sample data if file not found
        data = """Invoice,StockCode,Description,Quantity,InvoiceDate,Price,CustomerID,Country,TotalAmount,Year,Month,MonthName,Quarter,Week,Day,Weekday,Hour,Sales,CustomerOrderCount,CustomerTotalSales,AverageOrderValue,ProductSales,CountrySales,BasketSize,Recency,Frequency,Monetary
489434,85048,CHRISTMAS GLASS BALL,12,2009-12-01 07:45:00,6.95,13085,United Kingdom,83.4,2009,12,December,4,49,1,Tuesday,7,83.4,6,2017.2,32.535,9669.3,7381644.433,166,315,6,2017.2
489435,79323P,PINK CHERRY LIGHTS,12,2009-12-01 07:46:00,6.75,13085,United Kingdom,81.0,2009,12,December,4,49,1,Tuesday,7,81.0,6,2017.2,32.535,13171.1,7381644.433,166,315,6,2017.2
489436,22041,RECORD FRAME,48,2009-12-01 09:06:00,2.1,13078,United Kingdom,100.8,2009,12,December,4,49,1,Tuesday,9,100.8,32,16904.51,38.159,7338.3,7381644.433,193,2,32,16904.51"""
        df = pd.read_csv(pd.io.common.StringIO(data))
        
        # Generate synthetic data
        np.random.seed(42)
        countries = ['United Kingdom', 'France', 'Germany', 'USA', 'EIRE', 'Netherlands', 'Spain']
        products = ['CHRISTMAS GLASS BALL', 'CHERRY LIGHTS', 'RECORD FRAME', 'TRINKET BOX', 
                    'DOUGHNUT TRINKET', 'SAVE THE PLANET MUG', 'DOORMAT', 'HOT WATER BOTTLE',
                    'CAKE STAND', 'CANDLE HOLDER', 'METAL SIGN', 'PAPER CHAIN KIT']
        
        synthetic_data = []
        base_date = datetime(2009, 12, 1)
        
        for i in range(3000):
            invoice_date = base_date + timedelta(days=np.random.randint(0, 30), hours=np.random.randint(7, 20))
            country = np.random.choice(countries, p=[0.75, 0.08, 0.06, 0.04, 0.03, 0.02, 0.02])
            quantity = np.random.randint(1, 50)
            price = np.round(np.random.uniform(0.5, 25), 2)
            
            row = {
                'Invoice': f'489{np.random.randint(100, 999)}',
                'StockCode': np.random.choice(['85048', '79323P', '79323W', '22041', '21232']),
                'Description': np.random.choice(products),
                'Quantity': quantity,
                'InvoiceDate': invoice_date.strftime('%Y-%m-%d %H:%M:%S'),
                'Price': price,
                'CustomerID': np.random.randint(12000, 19000),
                'Country': country,
                'TotalAmount': np.round(quantity * price, 2),
                'Year': 2009,
                'Month': np.random.randint(1, 13),
                'MonthName': ['January','February','March','April','May','June','July','August','September','October','November','December'][np.random.randint(0, 12)],
                'Quarter': np.random.randint(1, 5),
                'Week': np.random.randint(1, 53),
                'Day': np.random.randint(1, 29),
                'Weekday': np.random.choice(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']),
                'Hour': np.random.randint(7, 20),
                'Sales': np.round(np.random.uniform(5, 200), 2),
                'CustomerOrderCount': np.random.randint(1, 100),
                'CustomerTotalSales': np.round(np.random.uniform(100, 10000), 2),
                'AverageOrderValue': np.round(np.random.uniform(10, 100), 2),
                'ProductSales': np.round(np.random.uniform(100, 50000), 2),
                'CountrySales': np.round(np.random.uniform(10000, 10000000), 2),
                'BasketSize': np.random.randint(1, 500),
                'Recency': np.random.randint(1, 400),
                'Frequency': np.random.randint(1, 100),
                'Monetary': np.round(np.random.uniform(100, 20000), 2)
            }
            synthetic_data.append(row)
        
        df = pd.DataFrame(synthetic_data)
    
    df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])
    df["Sales"] = df["Quantity"] * df["Price"]
    
    if "Profit" not in df.columns:
        df["Profit"] = df["Sales"] * 0.30
    
    df["Year"] = df["InvoiceDate"].dt.year
    df["Month"] = df["InvoiceDate"].dt.strftime("%b %Y")
    df["Month_Num"] = df["InvoiceDate"].dt.month
    df["Day"] = df["InvoiceDate"].dt.date
    df["DayOfWeek"] = df["InvoiceDate"].dt.day_name()
    df["Hour"] = df["InvoiceDate"].dt.hour
    df["WeekOfYear"] = df["InvoiceDate"].dt.isocalendar().week
    
    return df

df = load_data()

# ============================================================
# FILTERING FUNCTION
# ============================================================
def apply_filters(df, country=None, product=None, date_range=None):
    filtered = df.copy()
    
    if country and country != []:
        filtered = filtered[filtered["Country"].isin(country)]
    
    if product and product != []:
        filtered = filtered[filtered["Description"].isin(product)]
    
    if date_range and len(date_range) == 2:
        start, end = date_range
        filtered = filtered[
            (filtered["InvoiceDate"].dt.date >= start) &
            (filtered["InvoiceDate"].dt.date <= end)
        ]
    
    return filtered

# ============================================================
# RFM ANALYSIS FUNCTION (FIXED)
# ============================================================
def calculate_rfm(df):
    now = df["InvoiceDate"].max()
    rfm = df.groupby("CustomerID").agg({
        "InvoiceDate": lambda x: (now - x.max()).days,
        "Invoice": "nunique",
        "Sales": "sum"
    }).rename(columns={
        "InvoiceDate": "Recency",
        "Invoice": "Frequency",
        "Sales": "Monetary"
    })
    
    # Handle duplicate values in qcut
    try:
        rfm["R_Score"] = pd.qcut(rfm["Recency"].rank(method='first'), q=4, labels=[4, 3, 2, 1])
        rfm["F_Score"] = pd.qcut(rfm["Frequency"].rank(method='first'), q=4, labels=[1, 2, 3, 4])
        rfm["M_Score"] = pd.qcut(rfm["Monetary"].rank(method='first'), q=4, labels=[1, 2, 3, 4])
    except Exception:
        try:
            rfm["R_Score"] = pd.qcut(rfm["Recency"], q=4, labels=[4, 3, 2, 1], duplicates='drop')
            rfm["F_Score"] = pd.qcut(rfm["Frequency"], q=4, labels=[1, 2, 3, 4], duplicates='drop')
            rfm["M_Score"] = pd.qcut(rfm["Monetary"], q=4, labels=[1, 2, 3, 4], duplicates='drop')
        except Exception:
            rfm["R_Score"] = pd.cut(
                rfm["Recency"], 
                bins=[-1, rfm["Recency"].quantile(0.25), rfm["Recency"].quantile(0.5), 
                      rfm["Recency"].quantile(0.75), rfm["Recency"].max() + 1],
                labels=[4, 3, 2, 1]
            )
            rfm["F_Score"] = pd.cut(
                rfm["Frequency"], 
                bins=[-1, rfm["Frequency"].quantile(0.25), rfm["Frequency"].quantile(0.5), 
                      rfm["Frequency"].quantile(0.75), rfm["Frequency"].max() + 1],
                labels=[1, 2, 3, 4]
            )
            rfm["M_Score"] = pd.cut(
                rfm["Monetary"], 
                bins=[-1, rfm["Monetary"].quantile(0.25), rfm["Monetary"].quantile(0.5), 
                      rfm["Monetary"].quantile(0.75), rfm["Monetary"].max() + 1],
                labels=[1, 2, 3, 4]
            )
    
    rfm["RFM_Score"] = rfm["R_Score"].astype(str) + rfm["F_Score"].astype(str) + rfm["M_Score"].astype(str)
    
    rfm["Segment"] = rfm["RFM_Score"].apply(lambda x: 
        "👑 Champions" if str(x) in ["444", "443", "434"] else
        "❤️ Loyal Customers" if str(x) in ["344", "343", "334"] else
        "🌟 Potential Loyalists" if str(x) in ["433", "432", "423"] else
        "⚠️ At Risk" if str(x) in ["144", "143", "134"] else
        "📌 Need Attention"
    )
    
    return rfm

# ============================================================
# NAVIGATION
# ============================================================
st.sidebar.markdown("""
<div style="text-align:center;padding:10px 0;">
    <div style="font-size:2rem;margin-bottom:4px;">📊</div>
    <div style="font-weight:600;font-size:16px;color:#60A5FA;">Navigation</div>
</div>
""", unsafe_allow_html=True)

selected = option_menu(
    menu_title=None,
    options=["📈 Sales", "👥 Customers", "🔮 Forecast", "📦 Inventory"],
    icons=[None, None, None, None],
    orientation="vertical",
    default_index=0,
    styles={
        "container": {"padding": "0", "background": "transparent"},
        "nav-link": {
            "font-size": "15px",
            "text-align": "left",
            "margin": "4px 0",
            "color": "#94A3B8",
            "border-radius": "10px",
            "padding": "12px 20px",
            "transition": "all 0.3s ease",
            "border": "1px solid transparent",
        },
        "nav-link-selected": {
            "background": "linear-gradient(135deg, #1E3A5F, #2563EB)",
            "color": "white",
            "font-weight": "600",
            "border": "1px solid rgba(59, 130, 246, 0.3)",
            "boxShadow": "0 4px 15px rgba(37, 99, 235, 0.3)",
        },
        "nav-link-hover": {
            "background": "rgba(37, 99, 235, 0.1)",
            "border": "1px solid rgba(59, 130, 246, 0.1)",
        },
    }
)

# ============================================================
# SALES DASHBOARD
# ============================================================
if selected == "📈 Sales":
    
    st.sidebar.markdown("""
    <div style="margin:15px 0 10px 0;font-weight:600;color:#94A3B8;font-size:13px;letter-spacing:1px;text-transform:uppercase;">
        🔍 Filters
    </div>
    """, unsafe_allow_html=True)
    
    country_options = sorted(df["Country"].dropna().unique())
    country = st.sidebar.multiselect("🌍 Country", country_options, default=country_options[:3])
    product = st.sidebar.multiselect("📦 Product", sorted(df["Description"].dropna().unique()), default=[])
    date_range = st.sidebar.date_input("📅 Date Range", (df["InvoiceDate"].min().date(), df["InvoiceDate"].max().date()))
    
    filtered_df = apply_filters(df, country, product, date_range)
    if not country:
        filtered_df = df.copy()
        country = country_options
    
    # KPI Metrics
    revenue = filtered_df["Sales"].sum()
    orders = filtered_df["Invoice"].nunique()
    customers = filtered_df["CustomerID"].nunique()
    profit = filtered_df["Profit"].sum()
    avg_order_value = revenue / orders if orders > 0 else 0
    items_sold = filtered_df["Quantity"].sum()
    
    st.markdown("### 📈 Key Performance Indicators")
    
    col1, col2, col3, col4, col5, col6 = st.columns(6)
    
    with col1:
        st.markdown(f"""
            <div class="metric-card" style="background:linear-gradient(135deg,#1E3A5F,#2563EB);">
                <span class="icon">💰</span>
                <h4>Revenue</h4>
                <h2>${revenue:,.0f}</h2>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
            <div class="metric-card" style="background:linear-gradient(135deg,#064E3B,#10B981);">
                <span class="icon">📦</span>
                <h4>Orders</h4>
                <h2>{orders:,}</h2>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
            <div class="metric-card" style="background:linear-gradient(135deg,#78350F,#F59E0B);">
                <span class="icon">👤</span>
                <h4>Customers</h4>
                <h2>{customers:,}</h2>
            </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
            <div class="metric-card" style="background:linear-gradient(135deg,#7F1D1D,#EF4444);">
                <span class="icon">📈</span>
                <h4>Profit</h4>
                <h2>${profit:,.0f}</h2>
            </div>
        """, unsafe_allow_html=True)
    
    with col5:
        st.markdown(f"""
            <div class="metric-card" style="background:linear-gradient(135deg,#1A1A2E,#8B5CF6);">
                <span class="icon">🛒</span>
                <h4>Avg Order</h4>
                <h2>${avg_order_value:,.2f}</h2>
            </div>
        """, unsafe_allow_html=True)
    
    with col6:
        st.markdown(f"""
            <div class="metric-card" style="background:linear-gradient(135deg,#1A365D,#EC4899);">
                <span class="icon">📊</span>
                <h4>Items Sold</h4>
                <h2>{items_sold:,}</h2>
            </div>
        """, unsafe_allow_html=True)
    
    st.divider()
    
    # Monthly Sales Trend
    monthly_sales = filtered_df.groupby("Month")["Sales"].sum().reset_index()
    month_order = filtered_df.groupby("Month")["InvoiceDate"].max().sort_values().index.tolist()
    monthly_sales["Month"] = pd.Categorical(monthly_sales["Month"], categories=month_order, ordered=True)
    monthly_sales = monthly_sales.sort_values("Month")
    
    fig = px.area(
        monthly_sales,
        x="Month",
        y="Sales",
        title="<b>Monthly Revenue Trend</b>",
        template="plotly_dark",
        color_discrete_sequence=["#3B82F6"]
    )
    fig.update_layout(height=380, plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig, use_container_width=True)
    
    # Daily Sales with Moving Average
    daily_sales = filtered_df.groupby("Day")["Sales"].sum().reset_index()
    daily_sales["MA7"] = daily_sales["Sales"].rolling(window=7, min_periods=1).mean()
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=daily_sales["Day"], y=daily_sales["Sales"], mode="lines", name="Daily Sales", line=dict(color="#60A5FA", width=1.5), opacity=0.6))
    fig.add_trace(go.Scatter(x=daily_sales["Day"], y=daily_sales["MA7"], mode="lines", name="7-Day MA", line=dict(color="#F59E0B", width=2.5)))
    fig.update_layout(title="<b>Daily Sales with Moving Average</b>", template="plotly_dark", height=380, plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig, use_container_width=True)
    
    # Two Column Charts
    col1, col2 = st.columns(2)
    
    with col1:
        top_products = filtered_df.groupby("Description")["Sales"].sum().nlargest(12).sort_values()
        fig = px.bar(top_products, orientation="h", title="<b>🏆 Top Selling Products</b>", template="plotly_dark", 
                     color=top_products.values, color_continuous_scale="Viridis", labels={"value": "Revenue ($)", "index": ""})
        fig.update_layout(height=380, showlegend=False, plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        country_sales = filtered_df.groupby("Country")["Sales"].sum().sort_values(ascending=True).tail(10)
        fig = px.bar(country_sales, orientation="h", title="<b>🌍 Sales by Country</b>", template="plotly_dark",
                     color=country_sales.values, color_continuous_scale="Plasma", labels={"value": "Revenue ($)", "index": ""})
        fig.update_layout(height=380, showlegend=False, plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig, use_container_width=True)
    
    # Sales vs Profit
    monthly_metrics = filtered_df.groupby("Month").agg({"Sales": "sum", "Profit": "sum"}).reset_index()
    monthly_metrics["Month"] = pd.Categorical(monthly_metrics["Month"], categories=month_order, ordered=True)
    monthly_metrics = monthly_metrics.sort_values("Month")
    
    fig = go.Figure()
    fig.add_trace(go.Bar(x=monthly_metrics["Month"], y=monthly_metrics["Sales"], name="Revenue", marker_color="#3B82F6", opacity=0.8))
    fig.add_trace(go.Scatter(x=monthly_metrics["Month"], y=monthly_metrics["Profit"], name="Profit", mode="lines+markers", 
                             line=dict(color="#10B981", width=3), marker=dict(size=10, symbol="diamond")))
    fig.update_layout(title="<b>💰 Revenue vs Profit</b>", template="plotly_dark", height=380, plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig, use_container_width=True)
    
    # Business Insights
    st.divider()
    st.markdown("### 💡 Business Insights")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        top_country = filtered_df.groupby("Country")["Sales"].sum().idxmax()
        st.markdown(f"""
            <div class="info-box">
                <h4>📍 Best Performing Country</h4>
                <p style="font-size:20px;font-weight:700;color:#60A5FA;">{top_country}</p>
                <p>Revenue: <b>${filtered_df[filtered_df["Country"] == top_country]["Sales"].sum():,.0f}</b></p>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        top_product = filtered_df.groupby("Description")["Sales"].sum().idxmax()
        st.markdown(f"""
            <div class="info-box" style="border-left-color:#F59E0B;">
                <h4>🏆 Top Selling Product</h4>
                <p style="font-size:16px;font-weight:700;color:#FBBF24;">{top_product[:30]}</p>
                <p>Revenue: <b>${filtered_df[filtered_df["Description"] == top_product]["Sales"].sum():,.0f}</b></p>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        peak_hour = filtered_df.groupby("Hour")["Sales"].sum().idxmax()
        st.markdown(f"""
            <div class="info-box" style="border-left-color:#8B5CF6;">
                <h4>⏰ Peak Hour</h4>
                <p style="font-size:20px;font-weight:700;color:#A78BFA;">{peak_hour}:00</p>
                <p>Revenue: <b>${filtered_df[filtered_df["Hour"] == peak_hour]["Sales"].sum():,.0f}</b></p>
            </div>
        """, unsafe_allow_html=True)
    
    # Data Download
    st.divider()
    csv = filtered_df.to_csv(index=False).encode("utf-8")
    st.download_button(label="📥 Download Filtered Data", data=csv, file_name="sales_dashboard_data.csv", mime="text/csv")
    
    with st.expander("📄 View Raw Data"):
        st.dataframe(filtered_df, use_container_width=True, height=300)

# ============================================================
# CUSTOMER DASHBOARD
# ============================================================
elif selected == "👥 Customers":
    
    st.sidebar.markdown("""
    <div style="margin:15px 0 10px 0;font-weight:600;color:#94A3B8;font-size:13px;letter-spacing:1px;text-transform:uppercase;">
        👤 Customer Filters
    </div>
    """, unsafe_allow_html=True)
    
    country = st.sidebar.multiselect("🌍 Country", sorted(df["Country"].dropna().unique()), default=sorted(df["Country"].dropna().unique())[:3])
    customer_df = apply_filters(df, country)
    
    if len(customer_df) == 0:
        st.warning("No data available. Please adjust your filters.")
        st.stop()
    
    sales_range = st.sidebar.slider("💰 Sales Range", float(customer_df["Sales"].min()), float(customer_df["Sales"].max()), 
                                     (float(customer_df["Sales"].min()), float(customer_df["Sales"].max())))
    customer_df = customer_df[(customer_df["Sales"] >= sales_range[0]) & (customer_df["Sales"] <= sales_range[1])]
    
    if len(customer_df) == 0:
        st.warning("No data available after applying sales range.")
        st.stop()
    
    min_qty = st.sidebar.slider("📦 Minimum Quantity", int(customer_df["Quantity"].min()), int(customer_df["Quantity"].max()), int(customer_df["Quantity"].min()))
    customer_df = customer_df[customer_df["Quantity"] >= min_qty]
    
    if len(customer_df) == 0:
        st.warning("No data available after applying quantity filter.")
        st.stop()
    
    customer_menu = option_menu(
        menu_title=None,
        options=["📊 Overview", "🎯 RFM Analysis", "👥 Segments", "⭐ Top Customers", "💡 Insights"],
        icons=[None, None, None, None, None],
        orientation="horizontal",
        default_index=0,
        styles={
            "container": {"padding": "0", "background": "transparent"},
            "nav-link": {
                "font-size": "14px",
                "text-align": "center",
                "margin": "0 4px",
                "color": "#94A3B8",
                "border-radius": "8px",
                "padding": "8px 18px",
                "border": "1px solid transparent",
            },
            "nav-link-selected": {
                "background": "linear-gradient(135deg, #1E3A5F, #2563EB)",
                "color": "white",
                "font-weight": "600",
                "border": "1px solid rgba(59, 130, 246, 0.3)",
            },
        }
    )
    
    if customer_menu == "📊 Overview":
        st.markdown("### 👥 Customer Overview")
        
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("👤 Total Customers", f"{customer_df['CustomerID'].nunique():,}")
        col2.metric("📦 Total Orders", f"{customer_df['Invoice'].nunique():,}")
        col3.metric("💰 Total Revenue", f"${customer_df['Sales'].sum():,.0f}")
        col4.metric("📊 Avg Revenue/Customer", f"${customer_df['Sales'].sum() / customer_df['CustomerID'].nunique():,.0f}")
        
        st.divider()
        
        col1, col2 = st.columns(2)
        
        with col1:
            customers_by_country = customer_df.groupby("Country")["CustomerID"].nunique().sort_values(ascending=False).head(10)
            fig = px.bar(customers_by_country, orientation="h", title="<b>🌍 Customers by Country</b>", template="plotly_dark",
                         color=customers_by_country.values, color_continuous_scale="Blues", labels={"value": "Customers", "index": ""})
            fig.update_layout(height=400, showlegend=False, plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            customer_spending = customer_df.groupby("CustomerID")["Sales"].sum().reset_index()
            fig = px.histogram(customer_spending, x="Sales", nbins=30, title="<b>💰 Customer Spending Distribution</b>",
                               template="plotly_dark", color_discrete_sequence=["#F59E0B"], labels={"Sales": "Total Spending ($)"})
            fig.update_layout(height=400, plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")
            st.plotly_chart(fig, use_container_width=True)
    
    elif customer_menu == "🎯 RFM Analysis":
        st.markdown("### 🎯 RFM Analysis")
        
        rfm = calculate_rfm(customer_df)
        
        col1, col2, col3 = st.columns(3)
        col1.metric("📅 Avg Recency", f"{rfm['Recency'].mean():.1f} days")
        col2.metric("🔄 Avg Frequency", f"{rfm['Frequency'].mean():.1f} orders")
        col3.metric("💰 Avg Monetary", f"${rfm['Monetary'].mean():,.0f}")
        
        st.divider()
        
        segment_counts = rfm["Segment"].value_counts().reset_index()
        segment_counts.columns = ["Segment", "Count"]
        
        fig = px.bar(segment_counts, x="Segment", y="Count", title="<b>🎯 Customer Segments</b>", template="plotly_dark",
                     color="Count", color_continuous_scale="Viridis", labels={"Count": "Number of Customers"})
        fig.update_layout(height=400, plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig, use_container_width=True)
        
        with st.expander("📄 View RFM Data"):
            st.dataframe(rfm, use_container_width=True)
    
    elif customer_menu == "👥 Segments":
        st.markdown("### 👥 Customer Segments Analysis")
        
        col1, col2 = st.columns(2)
        
        with col1:
            segment_data = customer_df.groupby(["Country", "CustomerID"])["Sales"].sum().reset_index()
            segment_by_country = segment_data.groupby("Country")["CustomerID"].count().sort_values(ascending=False).head(10)
            fig = px.bar(segment_by_country, orientation="h", title="<b>👥 Customers by Country</b>", template="plotly_dark",
                         color=segment_by_country.values, color_continuous_scale="Plasma", labels={"value": "Customers", "index": ""})
            fig.update_layout(height=400, showlegend=False, plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            ltv_data = customer_df.groupby("CustomerID")["Sales"].sum().reset_index()
            ltv_data["LTV_Tier"] = pd.cut(ltv_data["Sales"], bins=[0, 100, 500, 1000, 5000, float("inf")],
                                          labels=["< $100", "$100-500", "$500-1k", "$1k-5k", "$5k+"])
            tier_counts = ltv_data["LTV_Tier"].value_counts().reset_index()
            tier_counts.columns = ["Tier", "Count"]
            fig = px.bar(tier_counts, x="Tier", y="Count", title="<b>💰 Customer LTV Tiers</b>", template="plotly_dark",
                         color="Count", color_continuous_scale="Reds", labels={"Count": "Customers"})
            fig.update_layout(height=400, plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")
            st.plotly_chart(fig, use_container_width=True)
    
    elif customer_menu == "⭐ Top Customers":
        st.markdown("### ⭐ Top Customers")
        
        top_customers = customer_df.groupby("CustomerID").agg({
            "Sales": "sum", "Invoice": "nunique", "Quantity": "sum", "Country": "first"
        }).sort_values("Sales", ascending=False).head(20)
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig = px.bar(top_customers.reset_index(), x="CustomerID", y="Sales", title="<b>🏆 Top 20 Customers</b>",
                         template="plotly_dark", color="Sales", color_continuous_scale="Viridis", labels={"Sales": "Revenue ($)"})
            fig.update_layout(height=400, plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            fig = px.scatter(top_customers.reset_index(), x="Invoice", y="Sales", size="Quantity", color="Country",
                             title="<b>📊 Customer Value Matrix</b>", template="plotly_dark",
                             labels={"Invoice": "Orders", "Sales": "Revenue ($)"}, hover_data=["CustomerID"])
            fig.update_layout(height=400, plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")
            st.plotly_chart(fig, use_container_width=True)
        
        st.dataframe(top_customers, use_container_width=True)
    
    elif customer_menu == "💡 Insights":
        st.markdown("### 💡 Customer Insights")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if len(customer_df) > 0:
                top_20_revenue = customer_df.groupby("CustomerID")["Sales"].sum().sort_values(ascending=False)
                top_count = max(1, int(len(top_20_revenue) * 0.2))
                top_revenue = top_20_revenue.head(top_count).sum()
                total_rev = top_20_revenue.sum()
                st.markdown(f"""
                    <div class="info-box">
                        <h4>📊 Revenue Concentration</h4>
                        <p style="font-size:28px;font-weight:700;color:#60A5FA;">{top_revenue/total_rev*100:.1f}%</p>
                        <p><b>Top 20%</b> of customers generate <b>{top_revenue/total_rev*100:.1f}%</b> of revenue</p>
                    </div>
                """, unsafe_allow_html=True)
        
        with col2:
            aov_by_country = customer_df.groupby("Country")["Sales"].mean().sort_values(ascending=False).head(10)
            fig = px.bar(aov_by_country, orientation="h", title="<b>🌍 Avg Order Value by Country</b>", template="plotly_dark",
                         color=aov_by_country.values, color_continuous_scale="Greens", labels={"value": "AOV ($)", "index": ""})
            fig.update_layout(height=300, showlegend=False, plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")
            st.plotly_chart(fig, use_container_width=True)

# ============================================================
# FORECAST DASHBOARD
# ============================================================
elif selected == "🔮 Forecast":
    
    st.sidebar.markdown("""
    <div style="margin:15px 0 10px 0;font-weight:600;color:#94A3B8;font-size:13px;letter-spacing:1px;text-transform:uppercase;">
        🔮 Forecast Parameters
    </div>
    """, unsafe_allow_html=True)
    
    forecast_days = st.sidebar.slider("📅 Forecast Days", 7, 90, 30)
    moving_average = st.sidebar.slider("📊 Moving Average Window", 3, 30, 7)
    country = st.sidebar.selectbox("🌍 Country", sorted(df["Country"].unique()))
    
    # Prepare data
    forecast_df = df[df["Country"] == country]
    forecast_df = forecast_df.groupby("InvoiceDate")["Sales"].sum().reset_index().sort_values("InvoiceDate")
    forecast_df["DayNumber"] = (forecast_df["InvoiceDate"] - forecast_df["InvoiceDate"].min()).dt.days
    
    if len(forecast_df) < 2:
        st.warning("Not enough data for forecasting. Please select a different country.")
        st.stop()
    
    # Model
    model = LinearRegression()
    X = forecast_df[["DayNumber"]]
    y = forecast_df["Sales"]
    model.fit(X, y)
    
    # Generate future predictions
    last_day = forecast_df["DayNumber"].max()
    future_days = np.arange(last_day + 1, last_day + forecast_days + 1).reshape(-1, 1)
    future_dates = pd.date_range(forecast_df["InvoiceDate"].max() + timedelta(days=1), periods=forecast_days, freq="D")
    
    future_df = pd.DataFrame({
        "InvoiceDate": future_dates,
        "PredictedSales": np.maximum(model.predict(future_days), 0)
    })
    
    forecast_menu = option_menu(
        None,
        ["📊 Forecast", "📈 Trend", "🔄 Seasonality", "📋 Table", "💡 Insights"],
        icons=[None, None, None, None, None],
        orientation="horizontal",
        default_index=0,
        styles={
            "container": {"padding": "0", "background": "transparent"},
            "nav-link": {
                "font-size": "14px",
                "text-align": "center",
                "margin": "0 4px",
                "color": "#94A3B8",
                "border-radius": "8px",
                "padding": "8px 18px",
                "border": "1px solid transparent",
            },
            "nav-link-selected": {
                "background": "linear-gradient(135deg, #1E3A5F, #2563EB)",
                "color": "white",
                "font-weight": "600",
                "border": "1px solid rgba(59, 130, 246, 0.3)",
            },
        }
    )
    
    if forecast_menu == "📊 Forecast":
        st.markdown("### 📊 Sales Forecast")
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=forecast_df["InvoiceDate"], y=forecast_df["Sales"], mode="lines", name="Historical", line=dict(color="#3B82F6", width=2)))
        fig.add_trace(go.Scatter(x=future_df["InvoiceDate"], y=future_df["PredictedSales"], mode="lines+markers", name="Forecast", line=dict(color="#F59E0B", width=2.5, dash="dash"), marker=dict(size=6, symbol="diamond")))
        fig.update_layout(title="<b>30-Day Sales Forecast</b>", template="plotly_dark", height=450, plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig, use_container_width=True)
        
        col1, col2, col3 = st.columns(3)
        col1.metric("📅 Forecast Days", forecast_days)
        col2.metric("📊 Total Forecast Revenue", f"${future_df['PredictedSales'].sum():,.0f}")
        col3.metric("📈 R² Score", f"{r2_score(y, model.predict(X)):.3f}")
    
    elif forecast_menu == "📈 Trend":
        st.markdown("### 📈 Historical Sales Trend")
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=forecast_df["InvoiceDate"], y=forecast_df["Sales"], mode="lines", name="Daily Sales", line=dict(color="#60A5FA", width=2), fill="tozeroy", fillcolor="rgba(96, 165, 250, 0.1)"))
        fig.add_trace(go.Scatter(x=forecast_df["InvoiceDate"], y=forecast_df["Sales"].rolling(window=moving_average, min_periods=1).mean(), mode="lines", name=f"{moving_average}-Day MA", line=dict(color="#F59E0B", width=3)))
        fig.update_layout(title=f"<b>Sales Trend with {moving_average}-Day Moving Average</b>", template="plotly_dark", height=450, plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig, use_container_width=True)
    
    elif forecast_menu == "🔄 Seasonality":
        st.markdown("### 🔄 Seasonality Analysis")
        
        col1, col2 = st.columns(2)
        
        with col1:
            df["MonthName"] = df["InvoiceDate"].dt.strftime("%B")
            month_order = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
            monthly_seasonality = df[df["Country"] == country].groupby("MonthName")["Sales"].sum().reindex(month_order).reset_index()
            monthly_seasonality.columns = ["Month", "Sales"]
            monthly_seasonality = monthly_seasonality.dropna()
            fig = px.bar(monthly_seasonality, x="Month", y="Sales", title="<b>📅 Monthly Seasonality</b>", template="plotly_dark",
                         color="Sales", color_continuous_scale="Blues", labels={"Sales": "Revenue ($)"})
            fig.update_layout(height=380, plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            weekday_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
            weekly_seasonality = df[df["Country"] == country].groupby("DayOfWeek")["Sales"].sum().reindex(weekday_order).reset_index()
            weekly_seasonality.columns = ["Day", "Sales"]
            fig = px.bar(weekly_seasonality, x="Day", y="Sales", title="<b>📊 Weekly Seasonality</b>", template="plotly_dark",
                         color="Sales", color_continuous_scale="Reds", labels={"Sales": "Revenue ($)"})
            fig.update_layout(height=380, plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")
            st.plotly_chart(fig, use_container_width=True)
    
    elif forecast_menu == "📋 Table":
        st.markdown("### 📋 Forecast Data")
        
        forecast_display = future_df.copy()
        forecast_display["InvoiceDate"] = forecast_display["InvoiceDate"].dt.strftime("%Y-%m-%d")
        forecast_display["PredictedSales"] = forecast_display["PredictedSales"].apply(lambda x: f"${x:,.2f}")
        forecast_display.columns = ["Date", "Forecast"]
        st.dataframe(forecast_display, use_container_width=True, height=400)
        
        csv = future_df.to_csv(index=False).encode("utf-8")
        st.download_button(label="📥 Download Forecast Data", data=csv, file_name="sales_forecast.csv", mime="text/csv")
    
    elif forecast_menu == "💡 Insights":
        st.markdown("### 💡 Forecast Insights")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f"""
                <div class="success-box">
                    <h4>📈 Forecast Summary</h4>
                    <p>Total Forecast Revenue: <b>${future_df['PredictedSales'].sum():,.0f}</b></p>
                    <p>Average Daily Sales: <b>${future_df['PredictedSales'].mean():,.0f}</b></p>
                    <p style="color:#94A3B8;font-size:13px;">Based on {len(forecast_df)} historical data points</p>
                </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
                <div class="info-box">
                    <h4>🎯 Recommendations</h4>
                    <p>📦 <b>Inventory Planning</b><br>Prepare {int(future_df['PredictedSales'].mean() * 1.3):,} units</p>
                    <p>💰 <b>Revenue Target</b><br>Set ${future_df['PredictedSales'].sum():,.0f} as target</p>
                </div>
            """, unsafe_allow_html=True)

# ============================================================
# INVENTORY DASHBOARD
# ============================================================
elif selected == "📦 Inventory":
    
    st.sidebar.markdown("""
    <div style="margin:15px 0 10px 0;font-weight:600;color:#94A3B8;font-size:13px;letter-spacing:1px;text-transform:uppercase;">
        📦 Inventory Parameters
    </div>
    """, unsafe_allow_html=True)
    
    min_quantity = st.sidebar.slider("📊 Minimum Quantity", 0, int(df["Quantity"].max()), 5)
    top_n = st.sidebar.slider("🏆 Top Products", 5, 50, 20)
    country = st.sidebar.selectbox("🌍 Country", sorted(df["Country"].unique()))
    
    inventory_df = df[df["Country"] == country]
    
    inventory = inventory_df.groupby(["StockCode", "Description"], as_index=False).agg({
        "Quantity": "sum", "Sales": "sum", "Invoice": "nunique", "CustomerID": "nunique"
    })
    inventory.columns = ["StockCode", "Description", "TotalSold", "Revenue", "Orders", "Customers"]
    inventory["AvgOrderValue"] = inventory["Revenue"] / inventory["Orders"]
    
    st.markdown("### 📦 Inventory Dashboard")
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("📦 Total Products", len(inventory))
    col2.metric("📊 Total Units Sold", f"{inventory['TotalSold'].sum():,}")
    col3.metric("💰 Total Revenue", f"${inventory['Revenue'].sum():,.0f}")
    col4.metric("📈 Avg Order Value", f"${inventory['AvgOrderValue'].mean():,.2f}")
    
    st.divider()
    
    inventory_menu = option_menu(
        None,
        ["📊 Overview", "⚡ Fast Moving", "🐢 Slow Moving", "🔄 Reorder"],
        icons=[None, None, None, None],
        orientation="horizontal",
        default_index=0,
        styles={
            "container": {"padding": "0", "background": "transparent"},
            "nav-link": {
                "font-size": "14px",
                "text-align": "center",
                "margin": "0 4px",
                "color": "#94A3B8",
                "border-radius": "8px",
                "padding": "8px 18px",
                "border": "1px solid transparent",
            },
            "nav-link-selected": {
                "background": "linear-gradient(135deg, #1E3A5F, #2563EB)",
                "color": "white",
                "font-weight": "600",
                "border": "1px solid rgba(59, 130, 246, 0.3)",
            },
        }
    )
    
    if inventory_menu == "📊 Overview":
        col1, col2 = st.columns(2)
        
        with col1:
            top_inventory = inventory.nlargest(top_n, "TotalSold")
            fig = px.bar(top_inventory, x="Description", y="TotalSold", title=f"<b>🏆 Top {top_n} Products</b>",
                         template="plotly_dark", color="TotalSold", color_continuous_scale="Viridis", labels={"TotalSold": "Units"})
            fig.update_layout(height=400, plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            fig = px.scatter(inventory, x="TotalSold", y="Revenue", size="Orders", color="AvgOrderValue",
                             hover_data=["Description"], title="<b>📊 Product Performance Matrix</b>", template="plotly_dark",
                             labels={"TotalSold": "Units Sold", "Revenue": "Revenue ($)"}, color_continuous_scale="Plasma")
            fig.update_layout(height=400, plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")
            st.plotly_chart(fig, use_container_width=True)
        
        st.dataframe(inventory, use_container_width=True)
    
    elif inventory_menu == "⚡ Fast Moving":
        fast_moving = inventory.nlargest(top_n * 2, "TotalSold")
        fig = px.bar(fast_moving, x="Description", y="TotalSold", title=f"<b>⚡ Fast Moving Products</b>",
                     template="plotly_dark", color="TotalSold", color_continuous_scale="Viridis", labels={"TotalSold": "Units"})
        fig.update_layout(height=400, plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig, use_container_width=True)
        st.dataframe(fast_moving, use_container_width=True)
    
    elif inventory_menu == "🐢 Slow Moving":
        slow_moving = inventory.nsmallest(top_n, "TotalSold")
        slow_moving = slow_moving[slow_moving["TotalSold"] > 0]
        fig = px.bar(slow_moving, x="Description", y="TotalSold", title=f"<b>🐢 Slow Moving Products</b>",
                     template="plotly_dark", color="TotalSold", color_continuous_scale="Reds", labels={"TotalSold": "Units"})
        fig.update_layout(height=400, plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig, use_container_width=True)
        st.dataframe(slow_moving, use_container_width=True)
    
    elif inventory_menu == "🔄 Reorder":
        reorder = inventory[inventory["TotalSold"] < min_quantity]
        if len(reorder) > 0:
            fig = px.bar(reorder, x="Description", y="TotalSold", title=f"<b>🔄 Products Below Threshold ({min_quantity} units)</b>",
                         template="plotly_dark", color="TotalSold", color_continuous_scale="Oranges", labels={"TotalSold": "Units"})
            fig.update_layout(height=400, plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")
            st.plotly_chart(fig, use_container_width=True)
            st.dataframe(reorder, use_container_width=True)
        else:
            st.markdown("""
                <div class="success-box">
                    <h4>✅ All Products Well Stocked</h4>
                    <p>No products are below the minimum quantity threshold</p>
                </div>
            """, unsafe_allow_html=True)

# ============================================================
# FOOTER
# ============================================================
st.divider()
st.markdown("""
<div style="text-align:center;padding:20px 0 10px 0;">
    <div style="display:flex;justify-content:center;gap:30px;flex-wrap:wrap;margin-bottom:10px;">
        <span style="color:#94A3B8;font-size:12px;">📊 Neural Retail Analytics v2.0</span>
        <span style="color:#94A3B8;font-size:12px;">⚡ AI-Powered Intelligence</span>
        <span style="color:#94A3B8;font-size:12px;">📈 Real-Time Analytics</span>
    </div>
    <div style="height:1px;width:60%;margin:8px auto;background:linear-gradient(90deg,transparent,#2563EB,transparent);"></div>
    <p style="color:#475569;font-size:11px;margin-top:8px;">© 2024 Neural Retail Analytics · Built with Streamlit</p>
</div>
""", unsafe_allow_html=True)