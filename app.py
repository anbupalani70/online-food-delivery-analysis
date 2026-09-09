
import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Online Food Delivery Analysis",
    page_icon="🍔",
    layout="wide"
)

# Load dataset
df = pd.read_csv("/content/ONLINE_FOOD_DELIVERY_CLEANED.csv")

# Convert date
df["Order_Date"] = pd.to_datetime(df["Order_Date"], errors="coerce")

# Title
st.title("🍔 Online Food Delivery Analysis")
st.subheader("Data-Driven Business Insights")

# ---------------- SIDEBAR FILTERS ----------------

st.sidebar.header("🔎 Dashboard Filters")

city_options = ["All"] + sorted(df["City"].dropna().unique().tolist())
selected_city = st.sidebar.selectbox("City", city_options)

cuisine_options = ["All"] + sorted(df["Cuisine_Type"].dropna().unique().tolist())
selected_cuisine = st.sidebar.selectbox("Cuisine", cuisine_options)

status_options = ["All"] + sorted(df["Order_Status"].dropna().unique().tolist())
selected_status = st.sidebar.selectbox("Order Status", status_options)

min_date = df["Order_Date"].min().date()
max_date = df["Order_Date"].max().date()

selected_dates = st.sidebar.date_input(
    "Date Range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

# ---------------- APPLY FILTERS ----------------

filtered_df = df.copy()

if selected_city != "All":
    filtered_df = filtered_df[
        filtered_df["City"] == selected_city
    ]

if selected_cuisine != "All":
    filtered_df = filtered_df[
        filtered_df["Cuisine_Type"] == selected_cuisine
    ]

if selected_status != "All":
    filtered_df = filtered_df[
        filtered_df["Order_Status"] == selected_status
    ]

if len(selected_dates) == 2:
    start_date, end_date = selected_dates

    filtered_df = filtered_df[
        (filtered_df["Order_Date"].dt.date >= start_date) &
        (filtered_df["Order_Date"].dt.date <= end_date)
    ]

# ---------------- KPI CALCULATIONS ----------------

total_orders = len(filtered_df)

total_revenue = filtered_df["Final_Amount"].sum()

avg_order_value = filtered_df["Order_Value"].mean()

avg_delivery_time = filtered_df["Delivery_Time_Min"].mean()

cancelled_orders = (
    filtered_df["Order_Status"] == "Cancelled"
).sum()

cancellation_rate = (
    cancelled_orders / total_orders * 100
    if total_orders > 0 else 0
)

avg_delivery_rating = filtered_df["Delivery_Rating"].mean()

profit_margin = filtered_df["Profit_Margin"].mean()

# ---------------- KPI CARDS ----------------

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Orders", f"{total_orders:,}")

with col2:
    st.metric("Total Revenue", f"{total_revenue:,.2f}")

with col3:
    st.metric("Avg Order Value", f"{avg_order_value:,.2f}")

with col4:
    st.metric("Avg Delivery Time", f"{avg_delivery_time:.1f} min")

col5, col6, col7 = st.columns(3)

with col5:
    st.metric("Cancellation Rate", f"{cancellation_rate:.2f}%")

with col6:
    st.metric("Avg Delivery Rating", f"{avg_delivery_rating:.2f}")

with col7:
    st.metric("Profit Margin", f"{profit_margin:.2f}%")

st.divider()

# ---------------- MONTHLY REVENUE ----------------

st.header("📈 Monthly Revenue Trend")

monthly_revenue = (
    filtered_df
    .groupby(filtered_df["Order_Date"].dt.to_period("M"))["Final_Amount"]
    .sum()
)

monthly_revenue.index = monthly_revenue.index.astype(str)

st.line_chart(monthly_revenue)

# ---------------- CITY ORDERS ----------------

st.header("🏙️ City-wise Orders")

city_orders = filtered_df["City"].value_counts()

st.bar_chart(city_orders)

# ---------------- CUISINE ORDERS ----------------

st.header("🍜 Cuisine-wise Orders")

cuisine_orders = filtered_df["Cuisine_Type"].value_counts()

st.bar_chart(cuisine_orders)

# ---------------- CANCELLATION REASONS ----------------

st.header("❌ Cancellation Reasons")

cancelled_data = filtered_df[
    filtered_df["Order_Status"] == "Cancelled"
]

if len(cancelled_data) > 0:
    cancellation_reasons = (
        cancelled_data["Cancellation_Reason"]
        .value_counts()
    )

    st.bar_chart(cancellation_reasons)
else:
    st.info("No cancelled orders for the selected filters.")

# ---------------- DATA SUMMARY ----------------

st.divider()

st.write(
    f"Showing **{len(filtered_df):,} records** after applying filters."
)
