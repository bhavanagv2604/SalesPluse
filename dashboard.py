import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

# Page settings
st.set_page_config(
    page_title="SalesPulse Analytics",
    page_icon="📊",
    layout="wide"
)

# Load data
PROJECT_FOLDER = Path(__file__).resolve().parent
DATA_FILE = PROJECT_FOLDER  / "cleaned_sales.csv"

st.title("📊 SalesPulse Analytics")
st.markdown("### E-commerce Sales Intelligence Dashboard")
st.write("Explore sales performance with interactive filters.")

df = pd.read_csv(DATA_FILE)

# Sidebar filters
st.sidebar.header("🔎 Filter Sales")

categories = ["All"] + sorted(df["category"].dropna().unique().tolist())
selected_category = st.sidebar.selectbox(
    "Choose Category",
    categories
)

filtered_df = df.copy()

if selected_category != "All":
    filtered_df = filtered_df[
        filtered_df["category"] == selected_category
    ]

products = ["All"] + sorted(
    filtered_df["product"].dropna().unique().tolist()
)

selected_product = st.sidebar.selectbox(
    "Choose Product",
    products
)

if selected_product != "All":
    filtered_df = filtered_df[
        filtered_df["product"] == selected_product
    ]

# Metrics
total_revenue = filtered_df["revenue"].sum()
total_orders = filtered_df["order_id"].nunique()
units_sold = filtered_df["quantity"].sum()
products_count = filtered_df["product"].nunique()

col1, col2, col3, col4 = st.columns(4)

col1.metric("💰 Total Revenue", f"₹{total_revenue:,.0f}")
col2.metric("🛒 Unique Orders", f"{total_orders}")
col3.metric("📦 Units Sold", f"{units_sold}")
col4.metric("🏷️ Products", f"{products_count}")

st.divider()

# Revenue by product
st.subheader("📈 Revenue by Product")

if not filtered_df.empty:
    product_sales = (
        filtered_df.groupby("product", as_index=False)["revenue"]
        .sum()
        .sort_values("revenue", ascending=False)
    )

    fig_product = px.bar(
        product_sales,
        x="product",
        y="revenue",
        color="product",
        title="Revenue by Product",
        labels={
            "product": "Product",
            "revenue": "Revenue (₹)"
        },
        text_auto=True
    )

    st.plotly_chart(fig_product, use_container_width=True)

    # Revenue by category
    st.subheader("📊 Revenue by Category")

    category_sales = (
        filtered_df.groupby("category", as_index=False)["revenue"]
        .sum()
        .sort_values("revenue", ascending=False)
    )

    fig_category = px.pie(
        category_sales,
        names="category",
        values="revenue",
        title="Revenue Share by Category",
        hole=0.4
    )

    st.plotly_chart(fig_category, use_container_width=True)

    # Data table
    st.subheader("📋 Filtered Sales Records")
    st.dataframe(filtered_df, use_container_width=True)

else:
    st.warning("No sales records match your selected filters.")

st.caption("SalesPulse | Python • Pandas • ETL • Streamlit • Plotly")
