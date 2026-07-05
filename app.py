# ==========================================
# SHOPPER SPECTRUM
# Customer Segmentation & Recommendation
# ==========================================

import streamlit as st
import pandas as pd
import joblib
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import gdown
import os
import streamlit as st
# -------------------------------
# Page Configuration
# -------------------------------

st.set_page_config(
    page_title="Shopper Spectrum",
    page_icon="🛒",
    layout="wide"
)

# ==========================================
# Custom Header
# ==========================================

st.markdown("""
<style>

.main-title{
    font-size:42px;
    font-weight:700;
    color:#00BFFF;
}

.sub-title{
    font-size:18px;
    color:#CFCFCF;
}
/* ===========================
KPI CARDS
=========================== */

div[data-testid="metric-container"]{
    background: linear-gradient(135deg,#17233c,#1f3558);
    border:1px solid #3b82f6;
    padding:18px;
    border-radius:18px;
    box-shadow:0 0 15px rgba(59,130,246,.25);
    transition:.3s;
}

div[data-testid="metric-container"]:hover{
    transform:translateY(-6px);
    box-shadow:0 0 25px rgba(59,130,246,.45);
}

div[data-testid="metric-container"] label{
    color:#cbd5e1;
    font-size:15px;
    font-weight:600;
}

/* ===========================
NAVIGATION
=========================== */
/* ===========================
SIDEBAR RADIO
=========================== */

section[data-testid="stSidebar"] div[data-testid="stRadio"]{
    background:#1B2747;
    padding:12px;
    border-radius:18px;
    border:1px solid rgba(96,165,250,.25);
    box-shadow:0 4px 12px rgba(0,0,0,.25);
}

/* Each option */
section[data-testid="stSidebar"] div[data-testid="stRadio"] label{
    display:flex;
    align-items:center;
    width:100%;
    padding:10px 12px;
    margin-bottom:6px;
    border-radius:10px;
}
/* Text */
section[data-testid="stSidebar"] div[data-testid="stRadio"] p{
    font-size:19px !important;
    font-weight:700 !important;
    color:white;
    white-space:nowrap;
    overflow:hidden;
    text-overflow:ellipsis;
}

section[data-testid="stSidebar"] div[data-testid="stRadio"] label:hover{
    background:#27457A;
}
            /* Radio group ka top gap remove */
section[data-testid="stSidebar"] div[data-testid="stRadio"] > div{
    gap:4px !important;
    margin-top:0px !important;
    padding-top:0px !important;
}

/* First option ke upar ka gap remove */
section[data-testid="stSidebar"] div[data-testid="stRadio"] label:first-child{
    margin-top:0px !important;
    padding-top:10px !important;
}

/* ===========================
INFO BOX
=========================== */

div[data-testid="stAlert"]{
    border-radius:18px;
}
</style>
""", unsafe_allow_html=True)


# ==========================================
# SIDEBAR LOGO
# ==========================================


st.sidebar.markdown("""
<div style="text-align:center;">
    <img src="data:image/png;base64,{}" width="120">
</div>
""".format(
    __import__("base64").b64encode(open("shopper.png","rb").read()).decode()
), unsafe_allow_html=True)

st.sidebar.markdown("""
<div style="text-align:center; margin-top:8px; margin-bottom:12px;">

<h3 style="
color:white;
margin-bottom:2px;
font-weight:700;">
Shopper Spectrum
</h3>

<p style="
color:#60A5FA;
font-size:17px;
margin-top:0px;">
AI Customer Analytics
</p>

</div>
""", unsafe_allow_html=True)
st.sidebar.markdown(
    "<hr style='margin-top:5px; margin-bottom:8px;'>",
    unsafe_allow_html=True
)

# ==========================================
# MYSQL CONNECTION
# ==========================================
# -------------------------------
# Load Files
# -------------------------------
# ==========================================
# DOWNLOAD FILES FROM GOOGLE DRIVE
# ==========================================

FILES = {
    "clean_online_retail.csv": "1gDUs_d9a-0fHA3RN7m70qkxB7_cpPkIP",
    "customer_segments.csv": "1uxuGGVFSnLIIO-hbvtqiCoyRIw97V3lp",
    "kmeans_model.pkl": "1LXGykamwTJgZZx3jg-385gywlJnD0zX7",
    "online_retail.csv": "1puTsRgmMEfXLDmIqMPxkhbpjYt6KmANC",
    "product_list.pkl": "1X6tVm3Awfkfc16Br4HZDwSjHuVo-jiHm",
    "product_similarity.pkl": "1dd2brkKSQYZgGhEdOq3tSmRSlVB33vLf",
    "scaler.pkl": "1RptXNgHhPZOiOqNUoOXLwIRRjTVA8oR5",
    "shopper.png": "1NoQ0pqt13ZYkoMyDFSx2EjejgWCM8nJH"
}

for filename, file_id in FILES.items():
    if not os.path.exists(filename):
        gdown.download(
            f"https://drive.google.com/uc?id={file_id}",
            filename,
            quiet=False
        )

segments = pd.read_csv("customer_segments.csv")
retail_df = pd.read_csv("clean_online_retail.csv")

rfm = pd.read_csv("customer_segments.csv")

similarity_df = joblib.load("product_similarity.pkl")

product_list = joblib.load("product_list.pkl")

scaler = joblib.load("scaler.pkl")

kmeans = joblib.load("kmeans_model.pkl")

# -------------------------------
# Sidebar
# -------------------------------
# ==============================
# Navigation
# ==============================


page = st.sidebar.radio(
    label="🧭 Navigation", 
    options=[
        "🏠 Home",
        "👥 Segments",
        "📊 RFM Analysis",
        "📈 Dashboard",
        "🗄 SQL Analytics",
        "🎯 Recommendation"
    ],
    label_visibility="collapsed"
)
# ==========================================
# GLOBAL MYSQL FILTERS
# ==========================================

st.sidebar.markdown("---")

st.sidebar.markdown("""
<h3 style="
color:white;
font-size:22px;
font-weight:700;
margin-bottom:12px;">
🔍 Dashboard Filters
</h3>
""", unsafe_allow_html=True)

# Country List from MySQL
country_query = """
SELECT DISTINCT Country
FROM retail_sales
ORDER BY Country;
"""

country_df = pd.DataFrame({
    "Country": sorted(retail_df["Country"].dropna().unique())
})

country_list = ["All"] + country_df["Country"].tolist()

selected_country = st.sidebar.selectbox(
    "🌍 Select Country",
    country_list
)

# Top N Filter
top_n = st.sidebar.slider(
    "📊 Select Top Records",
    min_value=5,
    max_value=20,
    value=10,
    step=5
)
st.sidebar.success(f"🌍 Country : {selected_country}")
st.sidebar.info(f"📊 Top Records : {top_n}")
st.sidebar.markdown("---")

st.sidebar.markdown("""
<div style="
background:#1B2747;
padding:16px;
border-radius:12px;
border-left:5px solid #3B82F6;
">

<h4 style="color:#60A5FA;margin-top:0;margin-bottom:8px;">
👨‍💻 Developed By
</h4>

<h3 style="color:white;margin:0;">
Yashvardhan Yadav
</h3>

<p style="color:#D1D5DB;font-size:14px;margin-top:5px;">
MBA Business Analytics
</p>

<hr style="border:1px solid #334155;">

<p style="color:white;font-size:13px;line-height:1.8;margin-bottom:0;">
🐍 Python &nbsp;|&nbsp; 🗄 SQL <br>
🤖 Machine Learning <br>
🚀 Streamlit
</p>

</div>
""", unsafe_allow_html=True)
# ==========================================
# HOME PAGE
# ==========================================

if page == "🏠 Home":

    st.markdown("""
    <div style="
    background:linear-gradient(135deg,#0F172A,#1E3A8A);
    padding:28px 35px;
    border-radius:22px;
    border:1px solid #2563EB;
    box-shadow:0px 8px 20px rgba(37,99,235,.30);
    width:100%;
    ">

    <h1 style="
    font-size:52px;
    font-weight:800;
    color:white;
    margin-bottom:8px;
    line-height:1.1;">
    🛒 Shopper Spectrum
    </h1>

    <h3 style="
    color:#8B5CF6;
    margin-top:0;
    margin-bottom:18px;
    font-size:22px;
    font-weight:700;
    white-space:nowrap;
    overflow:hidden;
    text-overflow:ellipsis;">
    AI-Powered Customer Analytics & Product Recommendation System
    </h3>

    <p style="
    font-size:17px;
    color:#CBD5E1;
    line-height:1.6;
    margin-bottom:18px;">
    Transform retail sales data into <b>actionable business insights</b> using
    <span style="color:#38BDF8;">Python</span>,
    <span style="color:#22C55E;">SQL</span>,
    <span style="color:#F59E0B;">Machine Learning</span> and
    <span style="color:#A855F7;">Streamlit</span>.
    </p>

    <hr style="border:1px solid #334155; margin:18px 0;">

    <div style="
    display:flex;
    justify-content:space-between;
    align-items:center;
    gap:15px;
    font-size:15px;
    font-weight:600;
    color:white;
    white-space:nowrap;">

    <div>👥 Customer Segmentation</div>

    <div>📊 RFM Analysis</div>

    <div>📈 Business Dashboard</div>

    <div>🗄 SQL Analytics</div>

    <div>🎯 Product Recommendation</div>

    </div>

    </div>
    """, unsafe_allow_html=True)

    st.write("")
    st.markdown("""
    <div style="
    background:#111827;
    padding:18px;
    border-radius:18px;
    border:1px solid #374151;
    margin-top:10px;
    margin-bottom:25px;">

    <div style="
    display:flex;
    justify-content:space-around;
    text-align:center;
    flex-wrap:wrap;">

    <div>
    <h3 style="color:#60A5FA;margin:0;">🤖 AI Model</h3>
    <p style="color:#D1D5DB;">K-Means Clustering</p>
    </div>

    <div>
    <h3 style="color:#22C55E;margin:0;">🗄 Database</h3>
    <p style="color:#D1D5DB;">MySQL</p>
    </div>

    <div>
    <h3 style="color:#F59E0B;margin:0;">📈 Analytics</h3>
    <p style="color:#D1D5DB;">RFM Analysis</p>
    </div>

    <div>
    <h3 style="color:#A855F7;margin:0;">🎯 Recommendation</h3>
    <p style="color:#D1D5DB;">Cosine Similarity</p>
    </div>

    </div>

    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns([1, 1.35, 1, 1])

    with col1:
        st.markdown(f"""
        <div style="
            background:linear-gradient(135deg,#13294B,#1E3A8A);
            padding:22px;
            border-radius:18px;
            border:1px solid #3B82F6;
            min-height:160px;
            display:flex;
            flex-direction:column;
            justify-content:space-between;">
            <div style="font-size:40px;">👥</div>
            <div style="color:#D1D5DB;font-size:18px;">Customers</div>
            <div style="
            font-size:38px;
            font-weight:bold;
            color:white;
            white-space:nowrap;
            overflow:hidden;
            text-overflow:ellipsis;">
                {segments['CustomerID'].nunique():,}
            </div>
            <div style="color:#9CA3AF;">
                Total Customers
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div style="
            background:linear-gradient(135deg,#123524,#166534);
            padding:22px;
            border-radius:18px;
            border:1px solid #22C55E;
            min-height:170px;
            display:flex;
            flex-direction:column;
            justify-content:space-between;">
            <div style="font-size:40px;">💰</div>
            <div style="color:#D1D5DB;font-size:18px;">Revenue</div>
            <div style="
            font-size:38px;
            font-weight:bold;
            color:white;
            white-space:nowrap;
            overflow:hidden;
            ">
                ${segments['Monetary'].sum():,.0f}
            </div>
            <div style="color:#9CA3AF;">
                Total Revenue Generated
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div style="
            background:linear-gradient(135deg,#4A2C09,#92400E);
            padding:22px;
            border-radius:18px;
            border:1px solid orange;
            min-height:170px;
            display:flex;
            flex-direction:column;
            justify-content:space-between;">
            <div style="font-size:40px;">🛒</div>
            <div style="color:#D1D5DB;font-size:18px;">Orders</div>
            <div style="
            font-size:38px;
            font-weight:bold;
            color:white;
            white-space:nowrap;
            overflow:hidden;
            text-overflow:ellipsis;">
                {segments['Frequency'].sum():,.0f}
            </div>
            <div style="color:#9CA3AF;">
                Total Orders
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown("""
        <div style="
            background:linear-gradient(135deg,#34114E,#6D28D9);
            padding:22px;
            border-radius:18px;
            border:1px solid #A855F7;
            min-height:170px;
            display:flex;
            flex-direction:column;
            justify-content:space-between;">
            <div style="font-size:40px;">🎯</div>
            <div style="color:#D1D5DB;font-size:18px;">Segments</div>
           <div style="
            font-size:38px;
            font-weight:bold;
            color:white;
            white-space:nowrap;
            overflow:hidden;
            text-overflow:ellipsis;">
                3
            </div>
            <div style="color:#9CA3AF;">
                Customer Segments
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.write("---")

    st.subheader("🚀 Dashboard Capabilities")

    st.write("")

    col1, col2 = st.columns(2)

    with col1:

        st.markdown("""
        <div style="
        background:linear-gradient(135deg,#16213E,#1F3B73);
        padding:25px;
        border-radius:18px;
        border:1px solid #3B82F6;
        min-height:220px;">

        <h3>👥 Customer Segmentation</h3>

        <p style="color:#CBD5E1;">
        Classify customers into
        High Value,
        Regular and
        At Risk groups
        using Machine Learning.
        </p>

        <hr>

        ✅ K-Means Clustering<br>
        ✅ Predict New Customer<br>
        ✅ Segment Distribution

        </div>
        """, unsafe_allow_html=True)

        st.write("")

        st.markdown("""
        <div style="
        background:linear-gradient(135deg,#143A2D,#166534);
        padding:25px;
        border-radius:18px;
        border:1px solid #22C55E;
        min-height:220px;">

        <h3>📊 RFM Analysis</h3>

        <p style="color:#CBD5E1;">
        Analyze purchasing behaviour
        using
        Recency,
        Frequency
        and Monetary metrics.
        </p>

        <hr>

        ✅ Customer Behaviour<br>
        ✅ RFM Charts<br>
        ✅ Segment Summary

        </div>
        """, unsafe_allow_html=True)

    with col2:

        st.markdown("""
        <div style="
        background:linear-gradient(135deg,#3B2408,#92400E);
        padding:25px;
        border-radius:18px;
        border:1px solid orange;
        min-height:220px;">

        <h3>📈 Business Dashboard</h3>

        <p style="color:#CBD5E1;">
        Interactive business KPIs,
        revenue analysis,
        customer insights
        and visual analytics.
        </p>

        <hr>

        ✅ KPI Cards<br>
        ✅ Interactive Charts<br>
        ✅ Business Insights

        </div>
        """, unsafe_allow_html=True)

        st.write("")

        st.markdown("""
        <div style="
        background:linear-gradient(135deg,#34114E,#6D28D9);
        padding:25px;
        border-radius:18px;
        border:1px solid #A855F7;
        min-height:220px;">

        <h3>🎯 Product Recommendation</h3>

        <p style="color:#CBD5E1;">
        Recommend similar products
        using
        Cosine Similarity
        and customer purchase behaviour.
        </p>

        <hr>

        ✅ AI Recommendation<br>
        ✅ Cross Selling<br>
        ✅ Similar Products

        </div>
        """, unsafe_allow_html=True)

    st.write("---")

    st.subheader("📂 Project Overview")

    col1, col2 = st.columns([1,1])

    with col1:

        st.markdown(f"""
        <div style="
        background:linear-gradient(135deg,#16213E,#1E3A8A);
        padding:22px;
        border-radius:18px;
        border:1px solid #3B82F6;
        min-height:320px;
        ">

        <h3 style="margin-top:0;margin-bottom:15px;">
        📊 Dataset Information
        </h3>

        <hr style="margin-bottom:18px; border:1px solid rgba(255,255,255,0.15);">

        <p style="margin:0 0 15px 0;">
            <b>Total Customers</b><br>
            <span style="font-size:22px;font-weight:bold;">
                {len(segments):,}
            </span>
        </p>

        <p style="margin:0 0 15px 0;">
            <b>Total Products</b><br>
            <span style="font-size:22px;font-weight:bold;">
                {len(product_list):,}
            </span>
        </p>

        <p style="margin:0 0 15px 0;">
            <b>Customer Segments</b><br>
            <span style="font-size:22px;font-weight:bold;">
                3
            </span>
        </p>

        <p style="margin:0;">
            <b>Database</b><br>
            <span style="font-size:20px;font-weight:bold;">
                MySQL
            </span>
        </p>

        </div>
        """, unsafe_allow_html=True)

    with col2:

        st.markdown("""
        <div style="
        background:linear-gradient(135deg,#123524,#166534);
        padding:22px;
        border-radius:18px;
        border:1px solid #22C55E;
        min-height:320px;
        ">

        <h3 style="margin-top:0;margin-bottom:15px;">
        ⚙️ Technology Stack
        </h3>

        <hr style="margin-bottom:18px; border:1px solid rgba(255,255,255,0.15);">

        <p style="margin:0 0 15px 0;font-size:18px;">
            🐍 <b>Python</b>
        </p>

        <p style="margin:0 0 15px 0;font-size:18px;">
            🗄️ <b>MySQL</b>
        </p>

        <p style="margin:0 0 15px 0;font-size:18px;">
            🤖 <b>Machine Learning</b>
        </p>

        <p style="margin:0 0 15px 0;font-size:18px;">
            📊 <b>Plotly</b>
        </p>

        <p style="margin:0;font-size:18px;">
            🚀 <b>Streamlit</b>
        </p>

        </div>
        """, unsafe_allow_html=True)

    # ==========================================
# CUSTOMER SEGMENTATION
# ==========================================

elif page == "👥 Segments":

    st.title("👥 Customer Segmentation")

    st.write("Predict customer segment using RFM values.")

    st.write("---")
# ======================================
# KPI CARDS
# ======================================
    st.info("""
    ### How it Works

    Enter the customer's:

    • Recency
    • Frequency
    • Monetary Value

    Then click **Predict Customer Segment** to classify the customer using the trained K-Means Machine Learning model.
    """)

    st.write("---")
    col1, col2, col3 = st.columns(3)

    with col1:
        recency = st.number_input(
            "Recency",
            min_value=0.0,
            value=30.0
        )

    with col2:
        frequency = st.number_input(
            "Frequency",
            min_value=0.0,
            value=5.0
        )

    with col3:
        monetary = st.number_input(
            "Monetary",
            min_value=0.0,
            value=500.0
        )

    st.write("")

    predict = st.button("Predict Customer Segment")

    if predict:

        new_customer=pd.DataFrame({
            "Recency":[recency],
            "Frequency":[frequency],
            "Monetary":[monetary]
        })

        new_scaled=scaler.transform(new_customer)

        prediction=kmeans.predict(new_scaled)[0]

        st.write("---")

        if prediction==2:

            segment="🌟 High Value Customer"

            color="green"

            desc="""
    High spending customer with recent purchases.
    Highly loyal and profitable.
    """

            recommendation="""
    ✅ Offer VIP Membership

    ✅ Premium Products

    ✅ Early Access Offers

    ✅ Exclusive Discounts
    """

        elif prediction==1:

            segment="🙂 Regular Customer"

            color="blue"

            desc="""
    Average purchase behaviour.
    Can be converted into loyal customers.
    """

            recommendation="""
    ✅ Personalized Offers

    ✅ Bundle Products

    ✅ Loyalty Points

    ✅ Festival Discounts
    """

        else:

            segment="⚠ At Risk Customer"

            color="red"

            desc="""
    Customer hasn't purchased recently.
    Needs retention strategy.
    """

            recommendation="""
    ✅ Win Back Campaign

    ✅ Discount Coupons

    ✅ Email Marketing

    ✅ Product Reminder
    """

        st.success(segment)

        st.info(desc)

        st.warning(recommendation)
        
        fig=px.scatter(

            x=[frequency],
            y=[monetary],

            size=[monetary],

            color=[segment],

            labels={
                "x":"Frequency",
                "y":"Monetary"
            },

            title="Predicted Customer Position"
        )

        fig.update_layout(
            template="plotly_dark",
            height=450
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )   

    st.subheader("📊 Customer Segment Distribution")

    segment_counts = (
        segments["Customer_Segment"]
        .value_counts()
        .reset_index()
    )

    segment_counts.columns = ["Customer Segment", "Customers"]

    fig = px.bar(
        segment_counts,
        x="Customer Segment",
        y="Customers",
        color="Customer Segment",
        text="Customers",
        title="Customer Segment Distribution"
    )

    fig.update_layout(
        template="plotly_dark",
        height=450,
        xaxis_title="Customer Segment",
        yaxis_title="Number of Customers"
    )

    st.plotly_chart(fig, use_container_width=True)
    st.info("""
    ### 📖 Chart Description

    This chart shows the distribution of customers across different customer segments
    generated using the K-Means clustering algorithm based on RFM analysis.

    • High Value Customers – Customers with high spending and frequent purchases.
    • Regular Customers – Customers with average purchasing behaviour.
    • At Risk Customers – Customers who have not purchased recently and may churn.
    """)
    st.success("""
    ### 💡 Business Insight

    • Regular Customers represent the largest customer group, indicating a stable customer base.

    • At Risk Customers form a significant portion of customers, suggesting the need for retention strategies.

    • High Value Customers are few in number but contribute the highest revenue and should be treated as premium customers.
    """)
    st.warning("""
    ### 🎯 Business Recommendation

    • Launch loyalty programs for High Value Customers.

    • Use personalized offers to convert Regular Customers into High Value Customers.

    • Run win-back campaigns, discount coupons, and reminder emails for At Risk Customers.

    • Continuously monitor customer segments to improve retention and maximize revenue.
    """)


# ==========================================
# RFM ANALYSIS
# ==========================================

elif page == "📊 RFM Analysis":

    st.markdown("""
    <h1 style="font-size:50px;font-weight:700;">
    📊 RFM Analysis Dashboard
    </h1>

    <h4 style="color:#60A5FA;">
    Customer Behaviour Analysis using RFM Model
    </h4>

    <p style="color:#B8C1CC;font-size:18px;">
    Analyse customer purchasing behaviour based on
    <b>Recency</b>, <b>Frequency</b> and <b>Monetary</b> values.
    </p>
    """,unsafe_allow_html=True)

    st.write("---")

    # ============================
    # KPI Cards
    # ============================
    col1, col2, col3 = st.columns([0.9,0.9,0.9])

    with col1:
        st.markdown(f"""
        <div style="
        background:linear-gradient(135deg,#2563EB,#111827);
        padding:18px;
        border-radius:15px;
        text-align:center;
        border:1px solid #3B82F6;
        box-shadow:0px 4px 15px rgba(37,99,235,0.35);
        ">
        <h2 style="font-size:38px;">👥</h2>
        <h4 style="color:#D1D5DB; font-size:20px; margin-bottom:15px;">
            Total Customers
        </h4>
        <h2 style="color:white; font-size:24px; margin-bottom:10px;">
            {len(rfm):,}
        </h2>
        <p style="color:#93C5FD; font-size:14px;">
            Customers in Dataset
        </p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div style="
        background:linear-gradient(135deg,#16A34A,#111827);
        padding:18px;
        border-radius:15px;
        text-align:center;
        border:1px solid #22C55E;
        box-shadow:0px 4px 15px rgba(34,197,94,0.35);
        ">
            <h1>🔁</h1>
            <h4 style="color:#D1D5DB;">Average Frequency</h4>
            <h2 style="color:white;">{rfm['Frequency'].mean():.2f}</h2>
            <p style="color:#86EFAC;">Orders per Customer</p>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div style="
        background:linear-gradient(135deg,#F59E0B,#111827);
        padding:18px;
        border-radius:15px;
        text-align:center;
        border:1px solid #FBBF24;
        box-shadow:0px 4px 15px rgba(245,158,11,0.35);
        ">
            <h1>💰</h1>
            <h4 style="color:#D1D5DB;">Average Monetary</h4>
            <h2 style="color:white;">${rfm['Monetary'].mean():,.2f}</h2>
            <p style="color:#FCD34D;">Average Customer Spend</p>
        </div>
        """, unsafe_allow_html=True)
    st.info("""
        These KPIs provide a quick summary of customer activity
        and overall spending behaviour.
        """)
    st.write("---")

    # ============================
    # Dataset Preview
    # ============================

    st.subheader("📄 RFM Dataset Preview")

    st.dataframe(rfm.head(10), use_container_width=True)
    st.caption("""
    First 10 records showing customer Recency,
    Frequency, Monetary value and assigned segment.
    """)
    st.write("---")

    # ============================
    # RFM Distribution Charts
    # ============================

    st.subheader("📈 RFM Distribution")

    fig, axes = plt.subplots(1, 3, figsize=(18,5))

    sns.histplot(
        rfm["Recency"],
        bins=30,
        kde=True,
        color="royalblue",
        ax=axes[0]
    )
    axes[0].set_title("Recency")

    sns.histplot(
        rfm["Frequency"],
        bins=30,
        kde=True,
        color="green",
        ax=axes[1]
    )
    axes[1].set_title("Frequency")

    sns.histplot(
        rfm["Monetary"],
        bins=30,
        kde=True,
        color="orange",
        ax=axes[2]
    )
    axes[2].set_title("Monetary")

    st.pyplot(fig)
    st.info("""
    📖 Chart Description

    These histograms display the distribution of Recency,
    Frequency and Monetary values across all customers.

    They help identify customer purchasing patterns,
    buying frequency and spending behaviour.
    """)
    st.success("""
    💡 Business Insight

    • Most customers purchase infrequently.

    • Monetary values are highly skewed due to premium buyers.

    • Recency distribution indicates several inactive customers.
    """)
    st.write("---")

    # ============================
    # RFM Boxplots
    # ============================

    st.subheader("📦 RFM Boxplots")

    fig, axes = plt.subplots(1, 3, figsize=(18,5))

    sns.boxplot(
        y=rfm["Recency"],
        color="royalblue",
        ax=axes[0]
    )
    axes[0].set_title("Recency")

    sns.boxplot(
        y=rfm["Frequency"],
        color="green",
        ax=axes[1]
    )
    axes[1].set_title("Frequency")

    sns.boxplot(
        y=rfm["Monetary"],
        color="orange",
        ax=axes[2]
    )
    axes[2].set_title("Monetary")

    st.pyplot(fig)
    st.info("""
    📖 Chart Description

    Boxplots highlight the spread,
    median and outliers of RFM values.

    Outliers indicate premium customers
    or inactive customers.
    """)
    st.success("""
    💡 Business Insight

    • High Monetary outliers represent VIP customers.

    • High Recency outliers indicate inactive customers.

    • Frequency outliers are loyal repeat buyers.
    """)
    st.write("---")
    # ============================
    # Cluster Summary
    # ============================

    st.subheader("📊 Cluster Summary")
  
    cluster_summary = (
        rfm.groupby("Customer_Segment")[["Recency", "Frequency", "Monetary"]]
        .mean()
        .round(2)
    )

    st.dataframe(cluster_summary, use_container_width=True)
    st.caption("""
        Average RFM values for each customer segment.
        """)
    st.info("""
        The table compares the average behaviour of
        High Value, Regular and At Risk customers.
        """)
    cluster_summary = (
    rfm.groupby("Customer_Segment")[["Recency","Frequency","Monetary"]]
    .mean()
    .reset_index()
)

    fig = px.bar(
        cluster_summary,
        x="Customer_Segment",
        y="Monetary",
        color="Customer_Segment",
        text="Monetary",
        title="Average Monetary by Customer Segment"
    )

    fig.update_layout(
        template="plotly_dark",
        height=450
    )

    st.plotly_chart(fig,use_container_width=True)
    fig = px.bar(
    cluster_summary,
    x="Customer_Segment",
    y="Recency",
    color="Customer_Segment",
    text="Recency",
    title="Average Recency by Customer Segment"
)

    fig.update_layout(
        template="plotly_dark",
        height=450
    )

    st.plotly_chart(fig,use_container_width=True)
    st.write("---")

    st.subheader("💡 Business Insights")

    st.info("""
    • High Value customers purchase frequently and spend the most money.

    • Regular customers contribute the largest share of customers.

    • At Risk customers have not purchased recently and require attention.

    • Monetary value varies significantly across customer segments.

    • Customer segmentation enables targeted marketing strategies.
    """)

    st.write("---")

    st.subheader("🎯 Business Recommendations")

    st.markdown("""
    ✅ Reward High Value customers with exclusive loyalty programs.

    ✅ Send personalized offers to Regular customers to increase purchase frequency.

    ✅ Launch win-back campaigns for At Risk customers.

    ✅ Recommend premium products to customers with high monetary value.

    ✅ Use RFM segments for targeted email and promotional campaigns.
    """)
    
# ==========================================
# BUSINESS DASHBOARD
# ==========================================

elif page == "📈 Dashboard":

    st.markdown("""
    <div style="
    background:linear-gradient(90deg,#0F172A,#1E3A8A);
    padding:30px;
    border-radius:20px;
    border:1px solid #3B82F6;
    margin-bottom:20px;
    ">

    <h1 style="color:white;">
    📈 Business Dashboard
    </h1>

    <h4 style="color:#93C5FD;">
    Retail Sales Performance Overview
    </h4>

    <p style="color:#CBD5E1;font-size:17px;">
    Interactive Business Dashboard built using
    <b>Python</b>,
    <b>SQL</b>,
    <b>Machine Learning</b> &
    <b>Streamlit</b>.
    </p>

    </div>
    """, unsafe_allow_html=True)
    # ==========================================
    # Apply Country Filter (Business Dashboard)
    # ==========================================

    if selected_country == "All":

        business_df = segments.copy()

    else:
        customer_query = f"""
        SELECT DISTINCT CustomerID
        FROM retail_sales
        WHERE Country = '{selected_country}';
        """

        customer_ids = (
            retail_df[retail_df["Country"] == selected_country][["CustomerID"]]
            .drop_duplicates()
            .sort_values("CustomerID")
        )

        business_df = segments[
            segments["CustomerID"].isin(customer_ids["CustomerID"])
        ]

    st.write("---")

    # KPI Cards


    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(f"""
        <div style="background:linear-gradient(135deg,#2563EB,#111827);
        padding:25px;border-radius:20px;text-align:center;color:white;">
            <h1>👥</h1>
            <h4>Total Customers</h4>
            <h2>{business_df['CustomerID'].nunique():,}</h2>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div style="background:linear-gradient(135deg,#16A34A,#111827);
        padding:25px;border-radius:20px;text-align:center;color:white;">
            <h1>💰</h1>
            <h4>Total Revenue</h4>
            <h2>${business_df['Monetary'].sum():,.0f}</h2>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div style="background:linear-gradient(135deg,#EA580C,#111827);
        padding:25px;border-radius:20px;text-align:center;color:white;">
            <h1>🛒</h1>
            <h4>Total Orders</h4>
            <h2>{business_df['Frequency'].sum():,.0f}</h2>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown(f"""
        <div style="background:linear-gradient(135deg,#7C3AED,#111827);
        padding:25px;border-radius:20px;text-align:center;color:white;">
            <h1>📦</h1>
            <h4>Average Order Value</h4>
            <h2>${business_df['Monetary'].mean():,.2f}</h2>
        </div>
        """, unsafe_allow_html=True)
    st.write("---")
    

    st.subheader("📊 Customer Segment Distribution")

    segment_count = (
        business_df["Customer_Segment"]
        .value_counts()
        .reset_index()
    )

    segment_count.columns = ["Segment", "Customers"]

    fig = px.bar(
        segment_count,
        x="Segment",
        y="Customers",
        color="Segment",
        text="Customers",
        color_discrete_sequence=["#2563EB", "#16A34A", "#EA580C"]
    )

    fig.update_traces(textposition="outside")

    fig.update_layout(
        template="plotly_dark",
        title="Customer Segment Distribution",
        xaxis_title="Customer Segment",
        yaxis_title="Number of Customers",
        height=500
    )

    st.plotly_chart(fig, use_container_width=True)

    st.info("""
    📌 Chart Description:
    This chart illustrates the distribution of customers across different customer segments
    (High Value, Regular, and At Risk). It helps businesses understand the composition of
    their customer base and identify which segment represents the largest proportion of customers.
    """)

    st.info("""
    💡 Business Insight:
    • Regular Customers constitute the largest customer segment, indicating a stable and loyal customer base.
    • High Value Customers are fewer in number but contribute significantly to overall revenue.
    • At Risk Customers represent potential churn and should be targeted with personalized retention campaigns.
    """)

    st.write("---")

    st.subheader("💰 Revenue by Customer Segment")

    revenue = (
        business_df.groupby("Customer_Segment")["Monetary"]
        .sum()
        .reset_index()
    )

    fig = px.bar(
        revenue,
        x="Customer_Segment",
        y="Monetary",
        color="Customer_Segment",
        text="Monetary",
        title="Revenue by Customer Segment"
    )

    fig.update_traces(texttemplate='$%{text:,.0f}', textposition='outside')

    fig.update_layout(
        template="plotly_dark",
        height=500,
        xaxis_title="Customer Segment",
        yaxis_title="Revenue ($)"
    )

    st.plotly_chart(fig, use_container_width=True)
    st.info("""
    ### 📖 Chart Description

    This chart compares the total revenue generated by each customer segment.

    - High Value customers contribute the highest revenue.
    - Regular customers generate stable income.
    - At Risk customers contribute less due to lower recent purchases.

    Businesses can identify which customer group drives overall profitability.
    """)

    st.write("---")

    st.subheader("🛒 Average Purchase Frequency")

    freq = (
        business_df.groupby("Customer_Segment")["Frequency"]
        .mean()
        .reset_index()
    )

    fig = px.bar(
        freq,
        x="Customer_Segment",
        y="Frequency",
        color="Customer_Segment",
        text="Frequency",
        title="Average Purchase Frequency"
    )

    fig.update_traces(texttemplate='%{text:.2f}', textposition='outside')

    fig.update_layout(
        template="plotly_dark",
        height=500,
        xaxis_title="Customer Segment",
        yaxis_title="Average Frequency"
    )

    st.plotly_chart(fig, use_container_width=True)
    st.info("""
    ### 📖 Chart Description

    This chart displays the average purchase frequency of each customer segment.

    - High frequency indicates loyal customers.
    - Low frequency indicates declining engagement.
    - Businesses can use this insight to improve customer retention.

    Frequent buyers should receive loyalty rewards and personalized offers.
    """)

    st.write("---")

    st.subheader("🏆 Top 10 High Value Customers")

    top_customers = (
        business_df
        .sort_values("Monetary", ascending=False)
        [["CustomerID", "Monetary"]]
        .head(top_n)
    )

    top_customers["CustomerID"] = top_customers["CustomerID"].astype(str)

    fig = px.bar(
        top_customers.sort_values("Monetary"),
        x="Monetary",
        y="CustomerID",
        orientation="h",
        text="Monetary",
        color="Monetary",
        color_continuous_scale="Blues",
        title="Top High Value Customers by Revenue"
    )

    fig.update_traces(
        texttemplate='$%{text:,.0f}',
        textposition="outside"
    )

    fig.update_layout(
        template="plotly_dark",
        height=600,
        xaxis_title="Revenue ($)",
        yaxis_title="Customer ID",
        coloraxis_showscale=False
    )

    st.plotly_chart(fig, use_container_width=True)
    st.info("""
    ### 📖 Chart Description

    This chart identifies the customers generating the highest revenue.

    These customers are the company's most valuable assets.

    Businesses should:
    • Offer VIP benefits
    • Provide personalized recommendations
    • Launch exclusive loyalty programs
    • Maintain strong customer relationships
    """)

    st.write("---")

    st.subheader("📋 Customer Segment Summary")

    segment_summary = (
        business_df.groupby("Customer_Segment")
        .agg(
            Customers=("CustomerID", "count"),
            Avg_Recency=("Recency", "mean"),
            Avg_Frequency=("Frequency", "mean"),
            Avg_Monetary=("Monetary", "mean")
        )
        .round(2)
    )

    st.dataframe(
        segment_summary,
        use_container_width=True
    )

    st.write("---")

    st.subheader("📌 Business Insights")

    st.info("""
    ✅ Regular Customers contribute the largest share of the customer base.

    ✅ High Value Customers have the highest average spending.

    ✅ At Risk Customers require retention campaigns.

    ✅ Personalized recommendations can increase repeat purchases.

    ✅ Loyalty programs should target High Value Customers.

    ✅ Discount campaigns should focus on At Risk Customers.
    """)

# ==========================================
# SQL ANALYTICS DASHBOARD
# ==========================================

elif page == "🗄 SQL Analytics":

    st.markdown("""
    <h1 style="
    font-size:48px;
    font-weight:800;
    color:white;
    margin-bottom:0px;">
    🗄 SQL Analytics Dashboard
    </h1>

    <h3 style="
    color:#60A5FA;
    margin-top:-5px;">
    Interactive Business Insights from MySQL Database
    </h3>

    <p style="
    font-size:18px;
    color:#B8C1CC;
    line-height:1.8;">
    Analyse retail sales using optimized SQL queries to uncover revenue trends,
    customer behaviour and business opportunities.
    </p>
    """, unsafe_allow_html=True)

    st.write("---")

    st.subheader("❓ Query 1: Which are the Top 10 Products generating the highest revenue?")

    if selected_country == "All":

     query = f"""
        SELECT
        Description AS Product,
        ROUND(SUM(Quantity*UnitPrice),2) AS Revenue
        FROM retail_sales
        GROUP BY Description
        ORDER BY Revenue DESC
        LIMIT {top_n};
        """

    else:

     query = f"""
     SELECT
        Description AS Product,
        ROUND(SUM(Quantity*UnitPrice),2) AS Revenue
        FROM retail_sales
        WHERE Country='{selected_country}'
        GROUP BY Description
        ORDER BY Revenue DESC
        LIMIT {top_n};
        """
    
      top_products = (
        retail_df.assign(
            Revenue=retail_df["Quantity"] * retail_df["UnitPrice"]
        )
        .groupby("Description", as_index=False)["Revenue"]
        .sum()
        .sort_values("Revenue", ascending=False)
        .head(top_n)
        )
    
      top_products.rename(
        columns={"Description": "Product"},
        inplace=True
        )

st.dataframe(top_products, use_container_width=True)

st.bar_chart(
    data=top_products,
    x="Product",
    y="Revenue"
)
    st.info("""
    ### 📊 Business Insight

    The top-selling products generate a significant portion of overall revenue.
    These products represent the company's strongest-performing inventory and
    customer demand.

    """)

    st.success("""
    ### 💡 Business Recommendation

    Focus inventory replenishment for these products to avoid stock-outs.

    Bundle top-selling products with slow-moving items to increase cross-selling.

    Use these products in promotional campaigns and homepage recommendations.

    Regularly monitor pricing strategies to maximize profitability.
    """)
    st.write("---")


    st.subheader("❓ Query 2: Which countries generated the highest revenue?")

    query = f"""
    SELECT
        Country,
        ROUND(SUM(Quantity * UnitPrice),2) AS Revenue
    FROM retail_sales
    GROUP BY Country
    ORDER BY Revenue DESC
    LIMIT {top_n};
    """

    country_sales = (
        retail_df.assign(Revenue=retail_df["Quantity"] * retail_df["UnitPrice"])
        .groupby("Country", as_index=False)["Revenue"]
        .sum()
        .sort_values("Revenue", ascending=False)
    )

    st.dataframe(
        country_sales,
        use_container_width=True
    )

    st.bar_chart(
        data=country_sales,
        x="Country",
        y="Revenue"
    )
    st.info("""
    ### 📊 Business Insight
    The dashboard highlights the countries contributing the highest revenue,
    allowing businesses to identify their strongest markets and prioritize sales efforts.
    """)

    st.success("""
    ### 💡 Business Recommendation
    Focus marketing campaigns and inventory planning on the top-performing countries.
    For low-performing regions, introduce promotional offers and localized marketing
    strategies to improve customer engagement and revenue.
    """)
    st.write("---")

    st.subheader("❓ Query 3: Which month generated the highest sales revenue?")

    if selected_country == "All":

        query = """
        SELECT
            MONTHNAME(InvoiceDate) AS Month,
            ROUND(SUM(Quantity*UnitPrice),2) AS Revenue
        FROM retail_sales
        GROUP BY MONTH(InvoiceDate), MONTHNAME(InvoiceDate)
        ORDER BY MONTH(InvoiceDate);
        """

    else:

        query = f"""
        SELECT
            MONTHNAME(InvoiceDate) AS Month,
            ROUND(SUM(Quantity*UnitPrice),2) AS Revenue
        FROM retail_sales
        WHERE Country='{selected_country}'
        GROUP BY MONTH(InvoiceDate), MONTHNAME(InvoiceDate)
        ORDER BY MONTH(InvoiceDate);
        """

    retail_df["Month"] = retail_df["InvoiceDate"].dt.to_period("M").astype(str)

    monthly_sales = (
        retail_df.assign(Revenue=retail_df["Quantity"] * retail_df["UnitPrice"])
        .groupby("Month", as_index=False)["Revenue"]
        .sum()
    )

    st.dataframe(
        monthly_sales,
        use_container_width=True
    )

    st.line_chart(
        data=monthly_sales,
        x="Month",
        y="Revenue"
    )
    st.info("""
    ### 📊 Business Insight

    Monthly sales trends reveal seasonal buying patterns and peak revenue periods.

    Identifying high-performing months helps businesses forecast demand more
    accurately and prepare inventory accordingly.
    """)

    st.success("""
    ### 💡 Business Recommendation

    Increase inventory before peak sales months.

    Launch marketing campaigns ahead of seasonal demand.

    Offer discounts during low-performing months to improve sales consistency.

    Use monthly trends for production and workforce planning.
    """)
    st.write("---")

    st.subheader("❓ Query 4: Which customers placed the highest number of orders?")

    if selected_country == "All":

        query = f"""
        SELECT
            CustomerID,
            COUNT(DISTINCT InvoiceNo) AS Orders
        FROM retail_sales
        GROUP BY CustomerID
        ORDER BY Orders DESC
        LIMIT {top_n};
        """

    else:

        query = f"""
        SELECT
            CustomerID,
            COUNT(DISTINCT InvoiceNo) AS Orders
        FROM retail_sales
        WHERE Country='{selected_country}'
        GROUP BY CustomerID
        ORDER BY Orders DESC
        LIMIT {top_n};
        """

    top_orders = (
        retail_df.groupby("CustomerID")["InvoiceNo"]
        .nunique()
        .reset_index(name="Orders")
        .sort_values("Orders", ascending=False)
    )

    st.dataframe(
        top_orders,
        use_container_width=True
    )

    st.bar_chart(
        data=top_orders,
        x="CustomerID",
        y="Orders"
    )
    st.info("""
    ### 📊 Business Insight

    A small group of customers contributes a large number of total orders,
    indicating strong customer loyalty and repeat purchasing behaviour.
    """)

    st.success("""
    ### 💡 Business Recommendation

    Reward frequent customers through loyalty programs.

    Provide exclusive offers and personalized recommendations.

    Introduce VIP memberships for top customers.

    Use email marketing to retain repeat buyers.
    """)
    st.write("---")

    st.subheader("❓ Query 5: What is the Average Order Value (AOV) for each country?")

    if selected_country == "All":

        query = """
        SELECT
            Country,
            ROUND(AVG(Quantity*UnitPrice),2) AS Average_Order_Value
        FROM retail_sales
        GROUP BY Country
        ORDER BY Average_Order_Value DESC;
        """

    else:

        query = f"""
        SELECT
            Country,
            ROUND(AVG(Quantity*UnitPrice),2) AS Average_Order_Value
        FROM retail_sales
        WHERE Country='{selected_country}'
        GROUP BY Country
        ORDER BY Average_Order_Value DESC;
        """

        aov = (
        retail_df.assign(OrderValue=retail_df["Quantity"] * retail_df["UnitPrice"])
        .groupby("Country", as_index=False)["OrderValue"]
        .mean()
        )

    st.dataframe(
        aov,
        use_container_width=True
    )

    st.bar_chart(
        data=aov,
        x="Country",
        y="Average_Order_Value"
    )
    st.info("""
    ### 📊 Business Insight

    Average Order Value (AOV) highlights the purchasing power of customers across
    different countries.

    Higher AOV indicates stronger customer spending behaviour.
    """)

    st.success("""
    ### 💡 Business Recommendation

    Increase AOV using product bundles and upselling strategies.

    Offer free shipping above a spending threshold.

    Introduce premium product recommendations for high-value markets.

    Design country-specific pricing and promotional strategies.
    """)
    # ==========================================
# PRODUCT RECOMMENDATION
# ==========================================

elif page == "🎯 Recommendation":

    st.markdown("""
    <h1 style="
    font-size:48px;
    font-weight:800;
    color:white;
    margin-bottom:0px;">
    🎯 AI Product Recommendation System
    </h1>

    <h4 style="
    color:#60A5FA;
    margin-top:-5px;">
    Smart Cross-Selling & Customer Purchase Intelligence
    </h4>
    """, unsafe_allow_html=True)

    st.markdown("""
    <p style="
    font-size:18px;
    color:#B8C1CC;
    line-height:1.8;">
    Discover products frequently purchased together using an
    <b>AI-powered Recommendation Engine</b> based on
    <b>Cosine Similarity</b> and customer purchasing behaviour.
    </p>
    """, unsafe_allow_html=True)
    
    st.divider()

    st.subheader("🔍 Search Product")

    search = st.text_input(
        "Type Product Name",
        placeholder="Example: WHITE HANGING HEART T-LIGHT HOLDER"
    )

    filtered_products = [
        p for p in sorted(product_list)
        if search.lower() in p.lower()
    ]

    selected_product = st.selectbox(
        "Select Product",
        filtered_products if filtered_products else ["No Product Found"]
    )
    st.write("")

    recommend = st.button(
        "🚀 Recommend Products",
        use_container_width=True
        )

    if recommend:

        if selected_product == "No Product Found":
            st.error("❌ Please search a valid product.")
        else:

            recommendations = similarity_df[selected_product].sort_values(
                ascending=False
            )[1:6]

            st.markdown("## 🎯 Top 5 Recommended Products")
            st.info(f"""
            Selected Product:
            **{selected_product}**
            """)

            cols = st.columns(2)

            for i, product in enumerate(recommendations.index):

                with cols[i % 2]:

                    score = recommendations.iloc[i]

                    st.markdown(f"""
                    <div style="
                    background:linear-gradient(135deg,#16213E,#1E3A8A);
                    padding:20px;
                    border-radius:18px;
                    border:1px solid #3B82F6;
                    margin-bottom:15px;
                    box-shadow:0 0 12px rgba(59,130,246,.30);
                    ">

                    <h4 style="color:white;margin-bottom:12px;">
                    📦 {product}
                    </h4>

                    <p style="color:#93C5FD;margin:0;font-size:18px;">
                    Similarity Score:
                    <b>{score:.2f}</b>
                    </p>

                    </div>
                    """, unsafe_allow_html=True)

            st.success("✅ AI Recommendation Generated Successfully")
            st.success("""
                ### 💡 Recommendation Summary

                ✔ Top 5 similar products identified

                ✔ Based on customer purchase behaviour

                ✔ Generated using Cosine Similarity

                ✔ Helps improve cross-selling opportunities
                """)
            st.write("---")


st.markdown("""
<hr style="border:1px solid #2D3748;">

<div style="text-align:center; padding:10px;">

<h3 style="color:white;">🛒 Shopper Spectrum</h3>

<p style="color:#9CA3AF; font-size:16px;">
AI Powered Customer Analytics • Product Recommendation • Retail Intelligence
</p>

<p style="color:#60A5FA; font-size:14px;">
🚀 Built with Python | SQL | Machine Learning | Streamlit
</p>

</div>
""", unsafe_allow_html=True)


