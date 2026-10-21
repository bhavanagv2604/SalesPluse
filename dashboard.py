import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

# Project configuration
st.set_page_config(
    page_title="SalesPulse Analytics",
    page_icon="📊",
    layout="wide"
)

# Locate the processed sales data
PROJECT_FOLDER = Path(__file__).resolve().parent
DATA_FILE = PROJECT_FOLDER / "data" / "cleaned_sales.csv"

st.title("📊 SalesPulse Analytics")
st.subheader("E-commerce Sales Intelligence Dashboard")

st.markdown(
    "Explore sales performance, revenue, and product insights."
)

# Load the data
df = pd.read_csv(DATA_FILE)

# Calculate dashboard metrics
total_revenue = df["revenue"].sum()
total_orders = df["order_id"].nunique()
units_sold = df["quantity"].sum()
products_count = df["product"].nunique()

# Display KPI cards
col1, col2, col3, col4 = st.columns(4)

col1.metric("💰 Total Revenue", f"₹{total_revenue:,.0f}")
col2.metric("🛒 Unique Orders", f"{total_orders}")
col3.metric("📦 Units Sold", f"{units_sold}")
col4.metric("🏷️ Products", f"{products_count}")

st.divider()

# Revenue by product
st.subheader("Revenue by Product")

product_sales = (
    df.groupby("product", as_index=False)["revenue"]
    .sum()
    .sort_values("revenue", ascending=False)
)

fig = px.bar(
    product_sales,
    x="product",
    y="revenue",
    color="product",
    title="Total Revenue by Product",
    labels={
        "product": "Product",
        "revenue": "Revenue (₹)"
    },
    text_auto=True
)

st.plotly_chart(fig, use_container_width=True)

# Sales data table
st.subheader("📋 Processed Sales Records")

st.dataframe(df, use_container_width=True)

st.caption("SalesPulse | Python • Pandas • ETL • Interactive Analytics")
