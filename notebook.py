# Mengimpor library pandas dengan alias pd
import pandas as pd

# Mengimpor library matplotlib dengan alias plt
import matplotlib.pyplot as plt

# Mengimpor library seaborn dengan alias sns
import seaborn as sns

# Mengimpor library streamlit dengan alias st
import streamlit as st

# Mengimpor fungsi format_currency dari library babel untuk memformat mata uang
from babel.numbers import format_currency

# Mengatur gaya tampilan seaborn menjadi "dark"
sns.set(style="dark")


# Fungsi untuk membuat DataFrame harian dari DataFrame utama
def create_daily_orders_df(df):
    # Meresample DataFrame harian berdasarkan order_date dan menghitung jumlah order dan total harga
    daily_orders_df = df.resample(rule="D", on="order_date").agg({
        "order_id": "nunique",
        "total_price": "sum"
    })
    # Me-reset index DataFrame
    daily_orders_df = daily_orders_df.reset_index()
    # Mengganti nama kolom untuk lebih jelas
    daily_orders_df.rename(columns={
        "order_id": "order_count",
        "total_price": "revenue"
    }, inplace=True)

    return daily_orders_df


# Fungsi untuk membuat DataFrame jumlah item pesanan
def create_sum_order_items_df(df):
    # Mengelompokkan DataFrame berdasarkan nama produk dan menghitung jumlah item
    sum_order_items_df = df.groupby("product_name").quantity_x.sum().sort_values(ascending=False).reset_index()
    return sum_order_items_df


# Fungsi untuk membuat DataFrame berdasarkan jenis kelamin pelanggan
def create_bygender_df(df):
    # Mengelompokkan DataFrame berdasarkan gender dan menghitung jumlah pelanggan unik
    bygender_df = df.groupby(by="gender").customer_id.nunique().reset_index()
    bygender_df.rename(columns={
        "customer_id": "customer_count"
    }, inplace=True)

    return bygender_df


# Fungsi untuk membuat DataFrame berdasarkan kelompok usia pelanggan
def create_byage_df(df):
    # Mengelompokkan DataFrame berdasarkan age_group dan menghitung jumlah pelanggan unik
    byage_df = df.groupby(by="age_group").customer_id.nunique().reset_index()
    byage_df.rename(columns={
        "customer_id": "customer_count"
    }, inplace=True)
    # Mengurutkan age_group dan mengonversi kolom menjadi kategori
    byage_df["age_group"] = pd.Categorical(byage_df["age_group"], ["Youth", "Adults", "Seniors"])

    return byage_df


# Fungsi untuk membuat DataFrame berdasarkan negara bagian pelanggan
def create_bystate_df(df):
    # Mengelompokkan DataFrame berdasarkan state dan menghitung jumlah pelanggan unik
    bystate_df = df.groupby(by="state").customer_id.nunique().reset_index()
    bystate_df.rename(columns={
        "customer_id": "customer_count"
    }, inplace=True)

    return bystate_df


# Fungsi untuk membuat DataFrame RFM (Recency, Frequency, Monetary)
def create_rfm_df(df):
    # Mengelompokkan DataFrame berdasarkan customer_id dan menghitung recency, frequency, dan monetary
    rfm_df = df.groupby(by="customer_id", as_index=False).agg({
        "order_date": "max",
        "order_id": "nunique",
        "total_price": "sum"
    })
    # Mengganti nama kolom untuk lebih jelas
    rfm_df.columns = ["customer_id", "max_order_timestamp", "frequency", "monetary"]

    # Mengonversi max_order_timestamp ke format tanggal
    rfm_df["max_order_timestamp"] = rfm_df["max_order_timestamp"].dt.date
    # Menghitung recency berdasarkan tanggal pemesanan terakhir
    recent_date = df["order_date"].dt.date.max()
    rfm_df["recency"] = rfm_df["max_order_timestamp"].apply(lambda x: (recent_date - x).days)
    # Menghapus kolom max_order_timestamp
    rfm_df.drop("max_order_timestamp", axis=1, inplace=True)

    return rfm_df


# Membaca data dari file CSV
all_df = pd.read_csv("all_data.csv")

# Kolom-kolom dengan tipe data datetime
datetime_columns = ["order_date", "delivery_date"]

# Mengurutkan DataFrame berdasarkan order_date
all_df.sort_values(by="order_date", inplace=True)
# Me-reset index DataFrame
all_df.reset_index(inplace=True)

# Mengonversi kolom dengan tipe data datetime
for column in datetime_columns:
    all_df[column] = pd.to_datetime(all_df[column])

# Menentukan tanggal minimum dan maksimum
min_date = all_df["order_date"].min()
max_date = all_df["order_date"].max()

# Membuat sidebar Streamlit
with st.sidebar:
    # Menambahkan logo perusahaan
    st.image("https://github.com/dicodingacademy/assets/raw/main/logo.png")

    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu', min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

# Memfilter DataFrame utama berdasarkan rentang tanggal yang dipilih
main_df = all_df[(all_df["order_date"] >= str(start_date)) &
                 (all_df["order_date"] <= str(end_date))]

# Membuat DataFrames menggunakan fungsi yang telah dibuat
daily_orders_df = create_daily_orders_df(main_df)
sum_order_items_df = create_sum_order_items_df(main_df)
bygender_df = create_bygender_df(main_df)
byage_df = create_byage_df(main_df)
bystate_df = create_bystate_df(main_df)
rfm_df = create_rfm_df(main_df)

# Membuat tampilan dashboard menggunakan Streamlit
st.header('Dicoding Collection Dashboard :sparkles:')

# Menampilkan bagian Daily Orders
st.subheader('Daily Orders')

col1, col2 = st.columns(2)

with col1:
    # Menampilkan total orders
    total_orders = daily_orders_df.order_count.sum()
    st.metric("Total orders", value=total_orders)

with col2:
    # Menampilkan total revenue dengan format mata uang
    total_revenue = format_currency(daily_orders_df.revenue.sum(), "AUD", locale='es_CO')
    st.metric("Total Revenue", value=total_revenue)

# Menampilkan grafik garis Daily Orders
fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(
    daily_orders_df["order_date"],
    daily_orders_df["order_count"],
    marker='o',
    linewidth=2,
    color="#90CAF9"
)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)

st.pyplot(fig)

# Menampilkan bagian Best & Worst Performing Product
st.subheader("Best & Worst Performing Product")

fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(35, 15))

colors = ["#90CAF9", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]

# Menampilkan bar plot produk terbaik
sns.barplot(x="quantity_x", y="product_name", data=sum_order_items_df.head(5), palette=colors, ax=ax[0])
ax[0].set_ylabel(None)
ax[0].set_xlabel("Number of Sales", fontsize=30)
ax[0].set_title("Best Performing Product", loc="center", fontsize=50)
ax[0].tick_params(axis='y', labelsize=35)
ax[0].tick_params(axis='x', labelsize=30)

# Menampilkan bar plot produk terburuk
sns.barplot(x="quantity_x", y="product_name",
            data=sum_order_items_df.sort_values(by="quantity_x", ascending=True).head(5), palette=colors, ax=ax[1])
ax[1].set_ylabel(None)
ax[1].set_xlabel("Number of Sales", fontsize=30)
ax[1].invert_xaxis()
ax[1].yaxis.set_label_position("right")
ax[1].yaxis.tick_right()
ax[1].set_title("Worst Performing Product", loc="center", fontsize=50)
ax[1].tick_params(axis='y', labelsize=35)
ax[1].tick_params(axis='x', labelsize=30)

st.pyplot(fig)

# Menampilkan bagian Customer Demographics
st.subheader("Customer Demographics")

col1, col2 = st.columns(2)

with col1:
    fig, ax = plt.subplots(figsize=(20, 10))

    colors = ["#D3D3D3", "#90CAF9", "#D3D3D3", "#D3D3D3", "#D3D3D3"]

    # Menampilkan bar plot jumlah pelanggan berdasarkan gender
    sns.barplot(
        y="customer_count",
        x="gender",
        data=bygender_df.sort_values(by="customer_count", ascending=False),
        palette=colors,
        ax=ax
    )
    ax.set_title("Number of Customer by Gender", loc="center", fontsize=50)
    ax.set_ylabel(None)
    ax.set_xlabel(None)
    ax.tick_params(axis='x', labelsize=35)
    ax.tick_params(axis='y', labelsize=30)
    st.pyplot(fig)

with col2:
    fig, ax = plt.subplots(figsize=(20, 10))

    colors = ["#D3D3D3", "#90CAF9", "#D3D3D3", "#D3D3D3", "#D3D3D3"]

    # Menampilkan bar plot jumlah pelanggan berdasarkan kelompok usia
    sns.barplot(
        y="customer_count",
        x="age_group",
        data=byage_df.sort_values(by="age_group", ascending=False),
        palette=colors,
        ax=ax
    )
    ax.set_title("Number of Customer by Age", loc="center", fontsize=50)
    ax.set_ylabel(None)
    ax.set_xlabel(None)
    ax.tick_params(axis='x', labelsize=35)
    ax.tick_params(axis='y', labelsize=30)
    st.pyplot(fig)

# Menampilkan bar plot jumlah pelanggan berdasarkan negara bagian
fig, ax = plt.subplots(figsize=(20, 10))
colors = ["#90CAF9", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]
sns.barplot(
    x="customer_count",
    y="state",
    data=bystate_df.sort_values(by="customer_count", ascending=False),
    palette=colors,
    ax=ax
)
ax.set_title("Number of Customer by States", loc="center", fontsize=30)
ax.set_ylabel(None)
ax.set_xlabel(None)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)
st.pyplot(fig)

# Menampilkan bagian Best Customer Based on RFM Parameters
st.subheader("Best Customer Based on RFM Parameters")

col1, col2, col3 = st.columns(3)

with col1:
    # Menampilkan rata-rata recency
    avg_recency = round(rfm_df.recency.mean(), 1)
    st.metric("Average Recency (days)", value=avg_recency)

with col2:
    # Menampilkan rata-rata frequency
    avg_frequency = round(rfm_df.frequency.mean(), 2)
    st.metric("Average Frequency", value=avg_frequency)

with col3:
    # Menampilkan rata-rata monetary dengan format mata uang
    avg_frequency = format_currency(rfm_df.monetary.mean(), "AUD", locale='es_CO')
    st.metric("Average Monetary", value=avg_frequency)

# Menampilkan bar plot RFM
fig, ax = plt.subplots(nrows=1, ncols=3, figsize=(35, 15))
colors = ["#90CAF9", "#90CAF9", "#90CAF9", "#90CAF9", "#90CAF9"]

# Menampilkan bar plot berdasarkan recency
sns.barplot(y="recency", x="customer_id", data=rfm_df.sort_values(by="recency", ascending=True).head(5), palette=colors,
            ax=ax[0])
ax[0].set_ylabel(None)
ax[0].set_xlabel("customer_id", fontsize=30)
ax[0].set_title("By Recency (days)", loc="center", fontsize=50)
ax[0].tick_params(axis='y', labelsize=30)
ax[0].tick_params(axis='x', labelsize=35)

# Menampilkan bar plot berdasarkan frequency
sns.barplot(y="frequency", x="customer_id", data=rfm_df.sort_values(by="frequency", ascending=False).head(5),
            palette=colors, ax=ax[1])
ax[1].set_ylabel(None)
ax[1].set_xlabel("customer_id", fontsize=30)
ax[1].set_title("By Frequency", loc="center", fontsize=50)
ax[1].tick_params(axis='y', labelsize=30)
ax[1].tick_params(axis='x', labelsize=35)

# Menampilkan bar plot berdasarkan monetary
sns.barplot(y="monetary", x="customer_id", data=rfm_df.sort_values(by="monetary", ascending=False).head(5),
            palette=colors, ax=ax[2])
ax[2].set_ylabel(None)
ax[2].set_xlabel("customer_id", fontsize=30)
ax[2].set_title("By Monetary", loc="center", fontsize=50)
ax[2].tick_params(axis='y', labelsize=30)
ax[2].tick_params(axis='x', labelsize=35)

st.pyplot(fig)

# Menampilkan caption
st.caption('Copyright (c) Dicoding 2023')
