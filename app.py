import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# 1. Page Configuration
st.set_page_config(page_title="E-Commerce Analytics Dashboard", layout="wide")

st.title("📊 E-Commerce Business Performance Dashboard")
st.markdown("An interactive data analysis platform designed to process multi-source commercial data, extract actionable insights, and track key business performance metrics.")

# 2. Data Sourcing, Cleaning, & Loading Simulation
@st.cache_data
def load_and_clean_data():
    # Simulating data collection from multiple sources
    np.random.seed(42)
    dates = pd.date_range(start="2025-01-01", end="2026-05-31", freq="D")
    categories = ['Electronics', 'Clothing', 'Home Decor', 'Books', 'Fitness']
    regions = ['North', 'South', 'East', 'West']
    
    data = pd.DataFrame({
        'Order_Date': np.random.choice(dates, size=1000),
        'Category': np.random.choice(categories, size=1000),
        'Region': np.random.choice(regions, size=1000),
        'Units_Sold': np.random.randint(1, 10, size=1000),
        'Unit_Price': np.random.uniform(15.0, 500.0, size=1000),
    })
    
    # Simulating Data Cleaning and Validation
    data['Revenue'] = data['Units_Sold'] * data['Unit_Price']
    data['Revenue'] = data['Revenue'].round(2)
    data = data.sort_values(by='Order_Date').reset_index(drop=True)
    return data

df = load_and_clean_data()

# 3. Sidebar Filters (Supports User Decision Making)
st.sidebar.header("🎯 Filter Options")
selected_region = st.sidebar.multiselect("Select Region", options=df['Region'].unique(), default=df['Region'].unique())
selected_category = st.sidebar.multiselect("Select Category", options=df['Category'].unique(), default=df['Category'].unique())

# Filter Datasets based on choices
filtered_df = df[(df['Region'].isin(selected_region)) & (df['Category'].isin(selected_category))]

# 4. Key Performance Indicators (KPI Metrics)
total_revenue = filtered_df['Revenue'].sum()
total_units = filtered_df['Units_Sold'].sum()
avg_order_value = filtered_df['Revenue'].mean() if len(filtered_df) > 0 else 0

col1, col2, col3 = st.columns(3)
with col1:
    st.metric(label="Total Revenue", value=f"₹{total_revenue:,.2f}")
with col2:
    st.metric(label="Total Units Sold", value=f"{total_units:,}")
with col3:
    st.metric(label="Avg Order Value", value=f"₹{avg_order_value:.2f}")

st.markdown("---")

# 5. Data Visualizations & Trends
chart_col1, chart_col2 = st.columns(2)

with chart_col1:
    st.subheader("📈 Monthly Revenue Trend")
    # Aggregating for trend tracking
    monthly_df = filtered_df.copy()
    monthly_df['Month'] = monthly_df['Order_Date'].dt.to_period('M').astype(str)
    trend_data = monthly_df.groupby('Month')['Revenue'].sum().reset_index()
    fig_trend = px.line(trend_data, x='Month', y='Revenue', markers=True, title="Revenue Generation Path")
    st.plotly_chart(fig_trend, use_container_width=True)

with chart_col2:
    st.subheader("📦 Sales Shares by Category")
    cat_data = filtered_df.groupby('Category')['Revenue'].sum().reset_index()
    fig_pie = px.pie(cat_data, values='Revenue', names='Category', hole=0.4, title="Market Domain Share")
    st.plotly_chart(fig_pie, use_container_width=True)

# 6. Structured Regional Evaluation
st.subheader("🗺️ Regional Distribution Matrix")
region_data = filtered_df.groupby('Region')[['Revenue', 'Units_Sold']].sum().reset_index()
st.dataframe(region_data.style.format({'Revenue': '₹{:.2f}'}), use_container_width=True)
