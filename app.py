# ==========================================================
# RESTAURANT ANALYTICS DASHBOARD
# Cognifyz Internship Project
# Final Premium Version
# Save as: app.py
# Run: py -m streamlit run app.py
# ==========================================================

import streamlit as st
import pandas as pd
import plotly.express as px
import warnings

warnings.filterwarnings("ignore")

# ----------------------------------------------------------
# PAGE CONFIG
# ----------------------------------------------------------
st.set_page_config(
    page_title="Restaurant Dashboard",
    page_icon="🍽",
    layout="wide"
)

# ----------------------------------------------------------
# CUSTOM THEME
# ----------------------------------------------------------
st.markdown("""
<style>
.main {background-color:#fffaf5;}
[data-testid="stSidebar"] {background-color:#f8efe6;}
h1,h2,h3 {color:#5c3d2e;}
div.stMetric {
    background:#fff3e6;
    padding:12px;
    border-radius:12px;
}
</style>
""", unsafe_allow_html=True)

# ----------------------------------------------------------
# LOAD DATA
# ----------------------------------------------------------
@st.cache_data
def load_data():
    return pd.read_csv("Dataset .csv")

df = load_data()

# ----------------------------------------------------------
# CLEAN DATA
# ----------------------------------------------------------
df["City"] = df["City"].fillna("Unknown")
df["Cuisines"] = df["Cuisines"].fillna("Unknown")
df["Restaurant Name"] = df["Restaurant Name"].fillna("Unknown")

# ----------------------------------------------------------
# SIDEBAR
# ----------------------------------------------------------
st.sidebar.title("🍴 Navigation")
menu = st.sidebar.radio(
    "Go To",
    ["Home","Level 1","Level 2","Level 3","Final Insights"]
)

# ==========================================================
# HOME
# ==========================================================
if menu == "Home":

    st.title("📊 Restaurant Analytics Dashboard")

    c1,c2,c3,c4 = st.columns(4)

    c1.metric("Restaurants", len(df))
    c2.metric("Cities", df["City"].nunique())
    c3.metric("Avg Rating", round(df["Aggregate rating"].mean(),2))
    c4.metric("Countries", df["Country Code"].nunique())

    st.subheader("Dataset Preview")
    st.dataframe(df.head(10), width="stretch")

    st.success("""
    Dashboard Summary:
    This dashboard analyzes cuisines, pricing,
    customer ratings, delivery trends,
    geography, and business opportunities.
    """)

# ==========================================================
# LEVEL 1
# ==========================================================
elif menu == "Level 1":

    task = st.sidebar.selectbox(
        "Select Task",
        ["Top Cuisines","City Analysis","Price Range Distribution","Online Delivery"]
    )

    if task == "Top Cuisines":

        st.title("🍜 Top Cuisines")

        cuisines = df["Cuisines"].str.split(", ").explode()
        top = cuisines.value_counts().head(10)

        fig = px.bar(
            x=top.index,
            y=top.values,
            color=top.values,
            color_continuous_scale=["#b45309","#ea580c"],
            title="Top 10 Cuisines"
        )
        st.plotly_chart(fig, width="stretch")

        st.info("""
        Insight:
        A few cuisines dominate demand.
        These cuisines have stronger market potential.
        """)

    elif task == "City Analysis":

        st.title("🏙 City Analysis")

        avg = df.groupby("City")["Aggregate rating"].mean().sort_values(ascending=False)

        fig = px.bar(
            x=avg.head(10).index,
            y=avg.head(10).values,
            color=avg.head(10).values,
            color_continuous_scale=["#7c2d12","#c2410c"],
            title="Top Rated Cities"
        )
        st.plotly_chart(fig, width="stretch")

        st.info("""
        Insight:
        Top cities show better restaurant ecosystems,
        customer activity, and competition.
        """)

    elif task == "Price Range Distribution":

        st.title("💰 Price Range Distribution")

        pr = df["Price range"].value_counts().sort_index()

        fig = px.bar(
            x=pr.index,
            y=pr.values,
            color=pr.values,
            color_continuous_scale=["#92400e","#f59e0b"],
            title="Price Range Distribution"
        )
        st.plotly_chart(fig, width="stretch")

        st.info("""
        Insight:
        Mid-price restaurants usually attract
        the broadest customer base.
        """)

    elif task == "Online Delivery":

        st.title("🚚 Online Delivery")

        delivery = df["Has Online delivery"].value_counts()

        fig = px.pie(
            names=delivery.index,
            values=delivery.values,
            title="Delivery Availability",
            color_discrete_sequence=["#b45309","#fb923c"]
        )
        st.plotly_chart(fig, width="stretch")

        st.info("""
        Insight:
        Delivery services increase convenience,
        reach, and repeat orders.
        """)

# ==========================================================
# LEVEL 2
# ==========================================================
elif menu == "Level 2":

    task = st.sidebar.selectbox(
        "Select Task",
        ["Restaurant Ratings","Cuisine Combination","Geographic Analysis","Restaurant Chains"]
    )

    if task == "Restaurant Ratings":

        st.title("⭐ Restaurant Ratings")

        fig = px.histogram(
            df,
            x="Aggregate rating",
            nbins=20,
            title="Rating Distribution",
            color_discrete_sequence=["#d97706"]
        )

        fig.update_layout(
            plot_bgcolor="#fffaf5",
            paper_bgcolor="#fffaf5"
        )

        st.plotly_chart(fig, width="stretch")

        st.info("""
        Insight:
        Highly rated restaurants gain stronger trust,
        visibility, and repeat customers.
        """)

    elif task == "Cuisine Combination":

        st.title("🍽 Cuisine Combination")

        combo = df["Cuisines"].value_counts().head(10)

        fig = px.bar(
            x=combo.index,
            y=combo.values,
            color=combo.values,
            color_continuous_scale=["#b45309","#f59e0b"],
            title="Most Common Cuisine Combinations"
        )
        st.plotly_chart(fig, width="stretch")

        st.info("""
        Insight:
        Multi-cuisine menus attract wider audiences
        and increase variety appeal.
        """)

    elif task == "Geographic Analysis":

        st.title("🗺 Geographic Analysis")

        geo = df[["Latitude","Longitude"]].dropna().copy()
        geo.columns = ["lat","lon"]

        st.map(geo, width="stretch")

        st.info("""
        Insight:
        Restaurant clusters usually form in
        commercial and densely populated areas.
        """)

    elif task == "Restaurant Chains":

        st.title("🏪 Restaurant Chains")

        chain = df["Restaurant Name"].value_counts()
        chains = chain[chain > 1].head(15)

        fig = px.bar(
            x=chains.index,
            y=chains.values,
            color=chains.values,
            color_continuous_scale=["#8e6e53","#c7a17a"],
            title="Popular Restaurant Chains"
        )
        st.plotly_chart(fig, width="stretch")

        st.info("""
        Insight:
        Chains benefit from trust,
        standard quality, and loyalty.
        """)

# ==========================================================
# LEVEL 3
# ==========================================================
elif menu == "Level 3":

    task = st.sidebar.selectbox(
        "Select Task",
        ["Votes Analysis","Price Range vs Services"]
    )

    if task == "Votes Analysis":

        st.title("🗳 Votes Analysis")

        fig = px.scatter(
            df,
            x="Votes",
            y="Aggregate rating",
            color="Aggregate rating",
            color_continuous_scale=["#b45309","#f59e0b"],
            title="Votes vs Rating"
        )
        st.plotly_chart(fig, width="stretch")

        st.info("""
        Insight:
        More votes usually indicate higher
        popularity and customer engagement.
        """)

    elif task == "Price Range vs Services":

        st.title("💳 Price Range vs Delivery")

        delivery = pd.crosstab(df["Price range"], df["Has Online delivery"])

        fig = px.bar(
            delivery,
            barmode="group",
            title="Price Range vs Online Delivery",
            color_discrete_sequence=["#c97b63","#f0a500"]
        )
        st.plotly_chart(fig, width="stretch")

        st.info("""
        Insight:
        Higher-priced restaurants often provide
        premium convenience services.
        """)

# ==========================================================
# FINAL INSIGHTS
# ==========================================================
elif menu == "Final Insights":

    st.title("🍽 Executive Summary & Strategic Insights")

    st.markdown("---")

    c1, c2 = st.columns(2)

    with c1:
        st.subheader("📊 Industry Insights")

        st.success("""
        • A few cuisine categories dominate demand.

        • Restaurant activity is concentrated in top cities.

        • Mid-priced restaurants attract the most customers.

        • Competitive markets improve service quality.
        """)

    with c2:
        st.subheader("👥 Customer Insights")

        st.info("""
        • Better engagement supports higher ratings.

        • Delivery improves convenience and retention.

        • Premium restaurants offer booking facilities.

        • Positive experiences strengthen reputation.
        """)

    st.markdown("---")

    st.subheader("🎯 Business Recommendations")

    st.warning("""
    1. Expand delivery partnerships.

    2. Focus on high-demand cuisines.

    3. Improve ratings via better service.

    4. Introduce reservation systems.

    5. Expand into strong urban markets.
    """)

    st.markdown("---")

    st.subheader("🏁 Final Conclusion")

    st.write("""
    Sustainable restaurant growth depends on
    customer experience, pricing strategy,
    convenience, and service excellence.
    """)

    # ------------------------------------------------------
    # RANDOM FALLING FOOD ANIMATION
    # ------------------------------------------------------
    st.markdown("""
    <style>
    .food{
        position:fixed;
        top:-60px;
        font-size:28px;
        animation:fall linear infinite;
        z-index:9999;
    }

    @keyframes fall{
        0%{transform:translateY(-50px) rotate(0deg);}
        100%{transform:translateY(110vh) rotate(360deg);}
    }

    .a{left:5%;animation-duration:7s;}
    .b{left:15%;animation-duration:9s;}
    .c{left:25%;animation-duration:6s;}
    .d{left:35%;animation-duration:8s;}
    .e{left:45%;animation-duration:10s;}
    .f{left:55%;animation-duration:7.5s;}
    .g{left:65%;animation-duration:8.5s;}
    .h{left:75%;animation-duration:6.5s;}
    .i{left:85%;animation-duration:9.5s;}
    .j{left:95%;animation-duration:7.2s;}
    </style>

    <div class="food a">🍕</div>
    <div class="food b">🍔</div>
    <div class="food c">🍟</div>
    <div class="food d">🍜</div>
    <div class="food e">🌮</div>
    <div class="food f">🍩</div>
    <div class="food g">🍣</div>
    <div class="food h">☕</div>
    <div class="food i">🍰</div>
    <div class="food j">🍗</div>
    """, unsafe_allow_html=True)