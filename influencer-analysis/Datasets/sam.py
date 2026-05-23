
"""
INFLUENCER TRUST & AUTHENTICITY INTELLIGENCE DASHBOARD (FINAL VERSION)

Project:
Influencer Impact: Analyzing the Authenticity of Social Media Influencers
Author: agals
"""

# ================= IMPORTS =================
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ================= PAGE CONFIG =================
st.set_page_config(
    page_title="Influencer Authenticity",
    page_icon="📊",
    layout="wide"
)

# ================= LOAD DATA =================
@st.cache_data
def load_data():
    return pd.read_csv("INFLUENCER_AUTHENTICITY_ANALYSIS.csv")

df = load_data()

if df.empty:
    st.error("Dataset is empty.")
    st.stop()

# ================= DATA CLEANING =================
df["speech_sentiment"] = pd.to_numeric(df["speech_sentiment"], errors="coerce")
df["product_sentiment"] = pd.to_numeric(df["product_sentiment"], errors="coerce")
df["engagement_rate_%"] = pd.to_numeric(df["engagement_rate_%"], errors="coerce")
df["authenticity_score"] = pd.to_numeric(df["authenticity_score"], errors="coerce")
df["product_review_count"] = pd.to_numeric(df["product_review_count"], errors="coerce")

df = df.dropna(subset=["speech_sentiment", "product_sentiment"])

# ================= SIMPLE PRODUCT NAME =================
df["simple_product_name"] = df["product_name"].astype(str).str.split(",").str[0]

# ================= AUTH CATEGORY CREATION =================
def categorize(row):

    auth = row["authenticity_score"]
    promo = str(row["promotion"]).strip().lower() in ["true", "1", "yes"]

    if auth >= 80 and promo:
        return "High Authentic - Sponsored"

    elif auth < 50 and promo:
        return "Low Authentic - Sponsored"

    elif auth >= 80 and not promo:
        return "High Authentic - Non Sponsored"

    elif 50 <= auth < 80 and not promo:
        return "Moderate Authentic -  Non Sponsored"

    elif auth < 50 and not promo:
        return "Low Authentic -  Non Sponsored"

    else:
        return "Moderate Authentic - Sponsored"

df["auth_category"] = df.apply(categorize, axis=1)

# ================= SIDEBAR FILTER =================
st.sidebar.markdown("## 🎯 Smart Filters")

selected_influencer = st.sidebar.selectbox(
    "👤 Select Influencer",
    sorted(df["influencer_name"].dropna().unique())
)

df_inf = df[df["influencer_name"] == selected_influencer]

selected_product = st.sidebar.selectbox(
    "📦 Select Product",
    df_inf["simple_product_name"].dropna().unique()
)

df_product = df_inf[df_inf["simple_product_name"] == selected_product]

if df_product.empty:
    st.error("No data available for selected influencer & product.")
    st.stop()

row = df_product.iloc[0]

# ================= HEADER =================
st.markdown("""
<h1 style='text-align:center;'>Influencer Authenticity</h1>
<p style='text-align:center; color:gray;'>
Sentiment Alignment • Market Reality • Engagement Analysis • Promotion Detection
</p>
""", unsafe_allow_html=True)

st.markdown("---")

# ================= KPI METRICS =================
c1, c2, c3, c4, c5, c6 = st.columns(6)

c1.metric("🎤 Speech Sentiment", round(float(row["speech_sentiment"]), 3))
c2.metric("🛒 Product Sentiment", round(float(row["product_sentiment"]), 3))
c3.metric("⭐ Product Rating", row["product_rating"])
c4.metric("📊 Engagement %", f"{round(float(row['engagement_rate_%']),2)}%")

promotion_status = str(row["promotion"]).strip().lower() in ["true", "1", "yes"]
promotion_text = "YES" if promotion_status else "NO"
c5.metric("📢 Promotion", promotion_text)

c6.metric("📝 Review Count", int(row["product_review_count"]))

# ================= AUTHENTICITY + SENTIMENT SIDE BY SIDE =================



colA, colB = st.columns(2)

# -------- AUTHENTICITY GAUGE --------
with colA:
    st.subheader("Authenticity Score")
    score = float(row["authenticity_score"])

    fig_gauge = go.Figure(go.Indicator(
        mode="gauge+number",
        value=score,
        number={"suffix": " / 100"},
        gauge={
            "axis": {"range": [0, 100]},
            "bar": {"color": "darkblue"},
            "steps": [
                {"range": [0, 50], "color": "#ffe6e6"},
                {"range": [50, 80], "color": "#fff9e6"},
                {"range": [80, 100], "color": "#e6ffe6"}
            ]
        }
    ))

    fig_gauge.update_layout(height=350)
    st.plotly_chart(fig_gauge, use_container_width=True)


# -------- SENTIMENT COMPARISON --------

    
with colB:
    st.subheader("Influencer Opinion vs Customer Reviews")
    fig_bar = px.bar(
        x=["Influencer Speech", "Customer Reviews"],
        y=[float(row["speech_sentiment"]), float(row["product_sentiment"])],
        range_y=[-1, 1],
        color=["Influencer Speech", "Customer Reviews"],
        color_discrete_sequence=["#4C78FF", "#FF6B6B"],
        height=350
    )

    fig_bar.update_layout(showlegend=False)
    st.plotly_chart(fig_bar, use_container_width=True)

# ================= AUTHENTICITY VERDICT =================
category = row["auth_category"]

if "High Authentic" in category:
    emoji = "🟢"
    bg = "#e6ffe6"

elif "Moderate" in category:
    emoji = "🟡"
    bg = "#fff9e6"

else:
    emoji = "🔴"
    bg = "#ffe6e6"

st.markdown(f"""
<div style="background-color:{bg}; padding:15px; border-radius:10px; text-align:center;">
    <h3>{emoji} {category}</h3>
</div>
""", unsafe_allow_html=True)

# ================= GLOBAL ANALYSIS SCATTER =================
st.subheader("Global Sentiment Alignment & Authenticity Distribution")

fig_scatter = px.scatter(
    df,
    x="speech_sentiment",
    y="product_sentiment",
    color="auth_category",
    size="engagement_rate_%",
    hover_data={
        "influencer_name": True,
        "simple_product_name": True,
        "product_review_count": True,
        "authenticity_score": True
    },
    range_x=[-1, 1],
    range_y=[-1, 1],
    height=500
)

fig_scatter.update_layout(
    xaxis_title="Influencer Speech Sentiment",
    yaxis_title="Customer Product Sentiment",
    legend_title="Authenticity Category",
    plot_bgcolor="white"
)

st.plotly_chart(fig_scatter, use_container_width=True)

# ================= HISTORY TABLE =================
st.subheader("Influencer Promotion History")

history_columns = [
    "simple_product_name",
    "promotion",
    "speech_sentiment",
    "product_sentiment",
    "engagement_rate_%",
    "product_rating",
    "product_review_count",
    "authenticity_score",
    "auth_category"
]

st.dataframe(
    df_inf[history_columns],
    use_container_width=True
)