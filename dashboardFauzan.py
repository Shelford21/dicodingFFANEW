import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
import os

sns.set(style='dark')

# Helper function yang dibutuhkan untuk menyiapkan berbagai dataframe

def create_daily_orders_df(df):
    daily_orders_df = df.resample(rule='D', on='dteday').agg({
        "hr": "nunique",
        "cnt": "sum"
    })
    daily_orders_df = daily_orders_df.reset_index()
    
    return daily_orders_df


# Load cleaned data
all_df = pd.read_csv("hour.csv")
all_df2 = pd.read_csv("day.csv")


Q1 = (all_df2['casual']).quantile(0.25)
Q3 = (all_df2['casual']).quantile(0.75)
IQR = Q3 - Q1

maximum = Q3 + (1.5*IQR)
minimum = Q1 - (1.5*IQR)

kondisi_lower_than = all_df2['casual'] < minimum
kondisi_more_than = all_df2['casual'] > maximum

all_df2.drop(all_df2[kondisi_lower_than].index, inplace=True)
all_df2.drop(all_df2[kondisi_more_than].index, inplace=True)


datetime_columns = ["dteday"]
all_df.sort_values(by="dteday", inplace=True)
all_df.reset_index(inplace=True)

for column in datetime_columns:
    all_df[column] = pd.to_datetime(all_df[column])

# Filter data
min_date = all_df["dteday"].min()
max_date = all_df["dteday"].max()

with st.sidebar:
    # Menambahkan logo perusahaan
    st.image("https://github.com/Shelford21/dicodingFFA/raw/main/iya.jpeg")
    
    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

main_df = all_df[(all_df["dteday"] >= str(start_date)) & 
                (all_df["dteday"] <= str(end_date))]

# st.dataframe(main_df)

# # Menyiapkan berbagai dataframe
daily_orders_df = create_daily_orders_df(main_df)


# plot number of daily orders (2021)
st.header('Dicoding Data Scientist 🚴')
st.subheader('Bike Sharing Dataset')

col1, col2 = st.columns(2)

with col1:
    total_orders = daily_orders_df.cnt.sum()
    st.metric("Total sewa sepeda", value=total_orders)

filtered_df = all_df[(all_df['dteday'] >= str(start_date)) & (all_df['dteday'] <= str(end_date))]
hr0=filtered_df.loc[filtered_df['hr'] == 0, 'cnt'].sum()
hr1=filtered_df.loc[filtered_df['hr'] == 1, 'cnt'].sum()
hr2=filtered_df.loc[filtered_df['hr'] == 2, 'cnt'].sum()
hr3=filtered_df.loc[filtered_df['hr'] == 3, 'cnt'].sum()
hr4=filtered_df.loc[filtered_df['hr'] == 4, 'cnt'].sum()
hr5=filtered_df.loc[filtered_df['hr'] == 5, 'cnt'].sum()
hr6=filtered_df.loc[filtered_df['hr'] == 6, 'cnt'].sum()
hr7=filtered_df.loc[filtered_df['hr'] == 7, 'cnt'].sum()
hr8=filtered_df.loc[filtered_df['hr'] == 8, 'cnt'].sum()
hr9=filtered_df.loc[filtered_df['hr'] == 9, 'cnt'].sum()
hr10=filtered_df.loc[filtered_df['hr'] == 10, 'cnt'].sum()
hr11=filtered_df.loc[filtered_df['hr'] == 11, 'cnt'].sum()
hr12=filtered_df.loc[filtered_df['hr'] == 12, 'cnt'].sum()
hr13=filtered_df.loc[filtered_df['hr'] == 13, 'cnt'].sum()
hr14=filtered_df.loc[filtered_df['hr'] == 14, 'cnt'].sum()
hr15=filtered_df.loc[filtered_df['hr'] == 15, 'cnt'].sum()
hr16=filtered_df.loc[filtered_df['hr'] == 16, 'cnt'].sum()
hr17=filtered_df.loc[filtered_df['hr'] == 17, 'cnt'].sum()
hr18=filtered_df.loc[filtered_df['hr'] == 18, 'cnt'].sum()
hr19=filtered_df.loc[filtered_df['hr'] == 19, 'cnt'].sum()
hr20=filtered_df.loc[filtered_df['hr'] == 20, 'cnt'].sum()
hr21=filtered_df.loc[filtered_df['hr'] == 21, 'cnt'].sum()
hr22=filtered_df.loc[filtered_df['hr'] == 22, 'cnt'].sum()
hr23=filtered_df.loc[filtered_df['hr'] == 23, 'cnt'].sum()

datahr = {
  "hr": ['0','1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20','21','22','23'],
  "cnt": [hr0,hr1,hr2,hr3,hr4,hr5,hr6,hr7,hr8,hr9,hr10,hr11,hr12,hr13,hr14,hr15,hr16,hr17,hr18,hr19,hr20,hr21,hr22,hr23]
}
df10 = pd.DataFrame(datahr)

fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(
    daily_orders_df["dteday"],
    daily_orders_df["cnt"],
    marker='o', 
    linewidth=2,
    color="RED"
)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)

st.pyplot(fig)

st.subheader("Grafik total rental sepeda berdasarkan jam:")
with col2:
    fig, ax = plt.subplots(figsize=(20, 10))
    sns.barplot(
        y="cnt", 
        x="hr",
        data=df10,
        ax=ax
    )
ax.set_title("Total Rental Sepeda berdasarkan jam dan tanggal yang sudah ditentukan", loc="center", fontsize=25)
ax.set_ylabel(None)
ax.set_xlabel(None)
ax.tick_params(axis='x', labelsize=35)
ax.tick_params(axis='y', labelsize=30)
st.pyplot(fig)


st.title("Pertanyaan bisnis 1 : Di saat musim apa dimana sepeda banyak disewa ?")
all_df2['season']=all_df2.season.map({1: 'spring', 2: 'summer',3:'fall', 4:'winter'})
# Calculating counts per season
su = all_df2.loc[all_df2['season'] == 'summer', 'cnt'].sum()
sp = all_df2.loc[all_df2['season'] == 'spring', 'cnt'].sum()
fa = all_df2.loc[all_df2['season'] == 'fall', 'cnt'].sum()
wi = all_df2.loc[all_df2['season'] == 'winter', 'cnt'].sum()

# Creating the summarized DataFrame
data_summary = {
    "season": ['summer', 'spring', 'fall', 'winter'],
    "cnt": [su, sp, fa, wi]
}
df0 = pd.DataFrame(data_summary)

# Streamlit app
st.subheader("Jumlah penyewaan berdasarkan musim")

# Create a bar chart using Matplotlib
fig, ax = plt.subplots()
ax.bar(df0['season'], df0['cnt'], color='red')
ax.set_xlabel('Season')
ax.set_ylabel('Count')
#ax.set_title('Jumlah penyewaan berdasarkan musim')
#ax.set_ylim(0, 1000000)
ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'{int(x)}'))

# Display the plot in Streamlit
st.pyplot(fig)
# Display DataFrame
st.write("", df0)

st.title("Pertanyaan bisnis 2 : Di saat cuaca apa dimana sepeda banyak disewa ?")

all_df2['weathersit']=all_df2.weathersit.map({1: 'Clear',2:'Mist + Cloudy',3:'Light Snow'})
# Calculating counts per weather situation
cl = all_df2.loc[all_df2['weathersit'] == 'Clear', 'cnt'].sum()
mi = all_df2.loc[all_df2['weathersit'] == 'Mist + Cloudy', 'cnt'].sum()
li = all_df2.loc[all_df2['weathersit'] == 'Light Snow', 'cnt'].sum()

# Creating the summarized DataFrame
data_summary = {
    "weathersit": ['Clear', 'Mist + Cloudy', 'Light Snow'],
    "cnt": [cl, mi, li]
}
df9 = pd.DataFrame(data_summary)

# Streamlit app
#st.title("Weather Situation Count Summary")


# Create a bar chart using Matplotlib
fig, ax = plt.subplots()
ax.bar(df9['weathersit'], df9['cnt'], color='green')
ax.set_xlabel('Weather Situation')
ax.set_ylabel('Count')
ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'{int(x)}'))  # Format y-axis labels as integers

# Streamlit app
st.subheader("Jumlah penyewaan berdasarkan musim")
# Display the plot in Streamlit
st.pyplot(fig)

# Display DataFrame
st.write("", df9)

st.title("Pertanyaan bisnis 3 : Pada tahun 2011 , kapan tepatnya jumlah rental sepeda terbanyak ?")

# Convert dteday to datetime
all_df2['dteday'] = pd.to_datetime(all_df2['dteday'])

# Extract features
def extract_feature(df):
    df["year"] = df['dteday'].dt.year
    df["day"] = df['dteday'].dt.day
    df["month"] = df['dteday'].dt.month
    df["hour"] = df['dteday'].dt.hour
    df['dayofweek'] = df['dteday'].dt.dayofweek

extract_feature(all_df2)

filtered_df = all_df2[(all_df2['dteday'] >= '2011-01-01') & (all_df2['dteday'] <= '2011-12-31')]
daily_counts = filtered_df.groupby(filtered_df['dteday'].dt.date)['cnt'].sum()

# Plotting daily counts
st.write("### Jumlah sewaan sepeda pada bulan januari hingga febuari tahun 2011")
dates = daily_counts.index
counts = daily_counts.values
fig, ax = plt.subplots(figsize=(8, 6))
ax.bar(dates, counts, color='green')
ax.set_xlabel('Date')
ax.set_ylabel('Count')
plt.xticks(rotation=45)
st.pyplot(fig)

# Find the date with the maximum rentals
max_rental_date = daily_counts.idxmax()
max_rental_count = daily_counts.max()

st.write(
    f"### Tanggal penyewaan sepeda terbanyak pada Tahun 2011 adalah tanggal **{max_rental_date}** dengan jumlah **{max_rental_count}** penyewaan."
)

st.caption('Copyright © Dicoding 2023')
st.caption('Ijin mengikuti referensi dicoding')
