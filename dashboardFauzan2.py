import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency

# Configure Seaborn style
sns.set(style='darkgrid')

# Helper function to create daily orders DataFrame
def create_daily_orders_df(df):
    daily_orders_df = df.resample(rule='D', on='dteday').agg({
        "hr": "nunique",
        "cnt": "sum"
    }).reset_index()
    return daily_orders_df

# Load cleaned data
all_df = pd.read_csv("hour.csv")
all_df.sort_values(by="dteday", inplace=True)
all_df.reset_index(drop=True, inplace=True)
all_df["dteday"] = pd.to_datetime(all_df["dteday"])

# Filter data
min_date, max_date = all_df["dteday"].min(), all_df["dteday"].max()

# Sidebar configuration
with st.sidebar:
    st.image("https://github.com/Shelford21/dicodingFFA/raw/main/iya.jpeg", caption="Company Logo")
    start_date, end_date = st.date_input(
        label='Rentang Waktu',
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

# Filter main DataFrame based on date range
main_df = all_df[(all_df["dteday"] >= start_date) & (all_df["dteday"] <= end_date)]

# Create daily orders DataFrame
daily_orders_df = create_daily_orders_df(main_df)

# Display headers
st.header('Dicoding Data Scientist 🚴')
st.subheader('Bike Sharing Dataset')

# Display metrics
col1, col2 = st.columns(2)
with col1:
    total_orders = daily_orders_df["cnt"].sum()
    st.metric("Total Sewa Sepeda", value=total_orders)

# Aggregate hourly rentals
hourly_counts = main_df.groupby("hr")["cnt"].sum().reset_index()

# Plot daily rentals over time
fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(daily_orders_df["dteday"], daily_orders_df["cnt"], marker='o', linewidth=2, color="red")
ax.set_title("Total Rental Sepeda Harian", fontsize=20)
ax.set_xlabel("Tanggal", fontsize=15)
ax.set_ylabel("Jumlah Sewa", fontsize=15)
ax.tick_params(axis='x', labelsize=12)
ax.tick_params(axis='y', labelsize=12)
st.pyplot(fig)

# Plot hourly rentals
st.subheader("Grafik Total Rental Sepeda Berdasarkan Jam")
with col2:
    fig, ax = plt.subplots(figsize=(20, 10))
    sns.barplot(x="hr", y="cnt", data=hourly_counts, ax=ax, palette="coolwarm")
    ax.set_title("Total Rental Sepeda per Jam", fontsize=25)
    ax.set_xlabel("Jam", fontsize=18)
    ax.set_ylabel("Jumlah Sewa", fontsize=18)
    ax.tick_params(axis='x', labelsize=15)
    ax.tick_params(axis='y', labelsize=15)
st.pyplot(fig)

# Footer
st.caption('Copyright © Dicoding 2023')
st.caption('Referensi: Dicoding')
