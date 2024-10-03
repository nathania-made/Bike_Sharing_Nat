import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
sns.set(style='dark')

def create_bike_d(df):
    bike_d_count_holiday = df.groupby(by="holiday").dteday.count()
    return bike_d_count_holiday

def create_rfm_df(df):
    rfm_df = bike_d.groupby(by="weekday", as_index=False).agg({
    "dteday": "max", 
    "holiday": "nunique",
    "cnt": "sum",
    })
    rfm_df.columns = ["dteday", "max_dteday", "frequency", "monetary"]  
    rfm_df["max_dteday"] = rfm_df["max_dteday"].dt.date
    recent_date = bike_d["dteday"].dt.date.max()
    rfm_df["recency"] = rfm_df["max_dteday"].apply(lambda x: (recent_date - x).days)
    
    rfm_df.drop("max_dteday", axis=1, inplace=True)
    rfm_df.head()

    return rfm_df

all_df = pd.read_csv("all_data.csv")
total_holiday = pd.read_csv("total_holiday.csv")
merge_total_holiday = pd.read_csv("merge_total_holiday.csv")
mean_weekday = pd.read_csv("mean_weekday.csv")
mean_most_holiday = pd.read_csv("mean_most_holiday.csv")


datetime_columns = ["dteday"]
all_df.sort_values(by="dteday", inplace=True)
all_df.reset_index(inplace=True)
 
for column in datetime_columns:
    all_df[column] = pd.to_datetime(all_df[column])

min_date = all_df["dteday"].min()
max_date = all_df["dteday"].max()
 
with st.sidebar:
    # Menambahkan logo perusahaan
    st.image("https://trexsporting.com/images/products/117-OPTB_-rA6l.png",caption="Let's Ride!", use_column_width=True)
    
    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

main_df = all_df[(all_df["dteday"] >= str(start_date)) & 
                (all_df["dteday"] <= str(end_date))]

bike_d_count_holiday = create_bike_d(main_df)

st.header('Bike Sharing Dashboard :sparkles:')

st.subheader('Daily Count')
 
col1 = st.columns(1)
 
with col1[0]:
    total_count = all_df.cnt.sum()
    st.metric("Total count", value=total_count)
 
 
fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(
    all_df["dteday"],
    all_df["cnt"],
    marker='o', 
    linewidth=2,
    color="#90CAF9"
)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)
 
st.pyplot(fig)

# Pertanyaan 1
# 1a
st.title("Total hari libur di 2011-2012")
fig, ax = plt.subplots()
total_holiday.plot(kind='bar', stacked=False, ax=ax)

# Menambahkan judul dan label
ax.set_xlabel(None)
ax.set_ylabel('Total hari')
plt.legend(['Total tidak libur', 'Total libur'])
plt.xticks(rotation=0)

# Menampilkan plot di Streamlit
st.pyplot(fig)
# 1b
st.title("Persebaran hari libur")
fig, ax = plt.subplots()
merge_total_holiday.plot(x='weekday', kind='bar', stacked=False, ax=ax)

# Menambahkan judul dan label
ax.set_xlabel('Hari')
ax.set_ylabel('Total hari')
weekday_labels = ['Minggu', 'Senin', 'Selasa', 'Rabu', 'Kamis', 'Jumat', 'Sabtu']
plt.xticks(ticks=merge_total_holiday['weekday'], labels=weekday_labels)
plt.xticks(rotation=0)
plt.legend(['Total tidak libur', 'Total libur'])

# Menampilkan plot di Streamlit
st.pyplot(fig)

# Pertanyaan 3
st.title("Perbandingan penggunaan sepeda pada akhir pekan (Sabtu, Minggu) dibandingkan hari kerja")
fig, ax = plt.subplots()
mean_weekday.plot(kind='bar', stacked=False, ax=ax).set_xticks([])

# Menambahkan judul dan label
ax.set_xlabel('Mean')
ax.set_ylabel('Count')
plt.legend(['Hari Kerja (Senin-Jumat)', 'Weekend (Sabtu-Minggu)'])

# Menampilkan plot di Streamlit
st.pyplot(fig)

# Pertanyaan 4
st.title("Performa penggunaan sepeda di hari libur")
fig, ax = plt.subplots()
mean_most_holiday.plot(kind='bar', stacked=False, ax=ax).set_xticks([])

# Menambahkan judul dan label
ax.set_xlabel('Mean')
ax.set_ylabel('Count')
plt.xticks(rotation=0)
plt.legend(['Hari Senin tidak libur', 'Hari Senin libur'])

# Menampilkan plot di Streamlit
st.pyplot(fig)