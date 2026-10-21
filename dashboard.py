import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

# ==========================================
# 1. PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="SalesPulse Analytics",
    page_icon="📊",
    layout="wide"
)

# ==========================================
# 2. LOAD SALES DATA
# ==========================================

PROJECT_FOLDER = Path(__file__).resolve().parent

# Find the sales CSV file
possible_files = [
    PROJECT_FOLDER / "data" / "cleaned_sales.csv",
    PROJECT_FOLDER / "cleaned_sales.csv",
    PROJECT_FOLDER / "data" / "sales.csv",
    PROJECT_FOLDER / "sales.csv"
]

DATA_FILE = next(
    (file for file in possible_files if file.exists()),
    None
)

st.title("📊 SalesPulse Analytics")
st.markdown("### E-commerce Sales Intelligence Dashboard")
st.write(
    "Explore sales performance using interactive filters "
    "and product revenue charts."
)

if DATA_FILE is None:
    st.error(
        "Sales CSV file not found. Place cleaned_sales.csv "
        "in your data folder or project folder."
    )
    st.stop()

try:
    df = pd.read_csv(DATA_FILE)
except Exception as error:
    st.error(f"Could not read the CSV file: {error}")
    st.stop()

# ==========================================
# 3. VALIDATE AND CLEAN DATA
# ==========================================

required_columns = [
    "category",
    "product",
    "revenue",
    "order_id",
    "quantity"
]

missing_columns = [
    column for column in required_columns
    if column not in df.columns
]

if missing_columns:
    st.error(
        f"Missing columns in your CSV: {missing_columns}"
    )
    st.stop()

df["revenue"] = pd.to_numeric(
    df["revenue"],
    errors="coerce"
)

df["quantity"] = pd.to_numeric(
    df["quantity"],
    errors="coerce"
)

df["category"] = df["category"].astype("string").str.strip()
df["product"] = df["product"].astype("string").str.strip()

df = df.dropna(
    subset=[
        "category",
        "product",
        "revenue",
        "order_id",
        "quantity"
    ]
).copy()

df = df[
    (df["category"] != "") &
    (df["product"] != "")
].copy()

if df.empty:
    st.warning("There are no valid sales records to display.")
    st.stop()

# ==========================================
# 4. SIDEBAR FILTERS
# ==========================================

st.sidebar.header("🔎 Filter Sales")

categories = ["All"] + sorted(
    df["category"].unique().tolist()
)

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
    filtered_df["product"].unique().tolist()
)

selected_product = st.sidebar.selectbox(
    "Choose Product",
    products
)

if selected_product != "All":
    filtered_df = filtered_df[
        filtered_df["product"] == selected_product
    ]

# ==========================================
# 5. CHECK FILTERED DATA
# ==========================================

if filtered_df.empty:
    st.warning(
        "No sales records match your filters. "
        "Please choose different options in the sidebar."
    )
    st.stop()

# ==========================================
# 6. SALES OVERVIEW METRICS
# ==========================================

st.subheader("📌 Sales Overview")

total_revenue = filtered_df["revenue"].sum()

total_orders = filtered_df["order_id"].nunique()

units_sold = filtered_df["quantity"].sum()

products_count = filtered_df["product"].nunique()

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "💰 Total Revenue",
    f"₹{total_revenue:,.0f}"
)

col2.metric(
    "🛒 Unique Orders",
    f"{total_orders}"
)

col3.metric(
    "📦 Units Sold",
    f"{units_sold:,.0f}"
)

col4.metric(
    "🏷️ Products",
    f"{products_count}"
)

st.divider()

# ==========================================
# 7. REVENUE BY PRODUCT
# ==========================================

st.subheader("📈 Revenue by Product")

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

st.plotly_chart(
    fig_product,
    use_container_width=True
)

st.divider()

# ==========================================
# 8. TOP PERFORMING PRODUCT
# ==========================================

top_product = product_sales.iloc[0]["product"]

top_revenue = product_sales.iloc[0]["revenue"]

st.success(
    f"🏆 Top-Performing Product: {top_product} "
    f"(Revenue: ₹{top_revenue:,.0f})"
)

st.divider()

# ==========================================
# 9. TOP 5 PRODUCTS BY REVENUE
# ==========================================

st.subheader("🏆 Top 5 Products by Revenue")

top_5_products = (
    product_sales
    .nlargest(5, "revenue")
    .sort_values("revenue", ascending=True)
    .copy()
)

if len(top_5_products) == 1:
    st.info(
        "Only one distinct product is available with the "
        "current filters. Select All for Category and Product "
        "to see more products."
    )

fig_top5 = px.bar(
    top_5_products,
    x="revenue",
    y="product",
    orientation="h",
    title="Top 5 Products Ranked by Revenue",
    labels={
        "product": "Product",
        "revenue": "Revenue (₹)"
    },
    text_auto=True
)

fig_top5.update_layout(
    showlegend=False,
    xaxis_title="Revenue (₹)",
    yaxis_title="Product"
)

st.plotly_chart(
    fig_top5,
    use_container_width=True
)

st.divider()

# ==========================================
# 10. REVENUE BY CATEGORY
# ==========================================

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

st.plotly_chart(
    fig_category,
    use_container_width=True
)

st.divider()

# ==========================================
# 11. FILTERED SALES RECORDS
# ==========================================

st.subheader("📋 Filtered Sales Records")

st.dataframe(
    filtered_df,
    use_container_width=True,
    hide_index=True
)

# ==========================================
# 12. FOOTER
# ==========================================

st.divider()

st.caption(
    "SalesPulse Analytics | Built with Python, "
    "Pandas, Plotly, and Streamlit"
)
