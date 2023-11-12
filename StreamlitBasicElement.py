# Import library yang diperlukan
import datetime

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Menampilkan DataFrame sederhana menggunakan Streamlit
st.write(pd.DataFrame({
    'c1': [1, 2, 3, 4],
    'c2': [10, 20, 30, 40]
}))

# Menampilkan judul utama menggunakan markdown
st.markdown(
    """
    # My first app
    Hello, para calon praktisi data masa depan!
    """
)

# Menampilkan judul utama menggunakan title
st.title('Belajar Analisis Data')

# Menampilkan header menggunakan header
st.header('Pengembangan Dashboard')

# Menampilkan subheader menggunakan subheader
st.subheader('Pengembangan Dashboard')

# Menampilkan caption di bagian bawah
st.caption('Copyright (c) 2023')

# Menampilkan blok kode Python menggunakan code
code = """def hello():
    print("Hello, Streamlit!")"""
st.code(code, language='python')

# Menampilkan teks menggunakan text
st.text('Halo, calon praktisi data masa depan.')

# Menampilkan rumus matematika menggunakan LaTeX
st.latex(r"""
    \sum_{k=0}^{n-1} ar^k =
    a \left(\frac{1-r^{n}}{1-r}\right)
""")

# Menampilkan DataFrame dalam bentuk tabel menggunakan dataframe
df = pd.DataFrame({
    'c1': [1, 2, 3, 4],
    'c2': [10, 20, 30, 40],
})

# Menampilkan DataFrame dalam bentuk tabel menggunakan table
st.dataframe(data=df, width=500, height=150)
st.table(data=df)

# Menampilkan metric menggunakan metric
st.metric(label="Temperature", value="28 °C", delta="1.2 °C")

# Menampilkan data dalam format JSON menggunakan json
st.json({
    'c1': [1, 2, 3, 4],
    'c2': [10, 20, 30, 40],
})

# Membuat histogram menggunakan pyplot
x = np.random.normal(15, 5, 250)
fig, ax = plt.subplots()
ax.hist(x=x, bins=15)

# Menampilkan plot menggunakan pyplot
st.pyplot(fig)

# Text input
name = st.text_input(label="Nama Lengkap", value="")
st.write("Nama: ", name)

# Text area
text = st.text_area("Feedback")
st.write("Feedback: ", text)

# Number input
number = st.number_input(label="Umur")
st.write("Umur: ", int(number), " tahun")

# Date input
date = st.date_input(label="Tanggal lahir", min_value=datetime.datetime(1900, 1, 1))
st.write("Tanggal lahir: ", date)

# File uploader
uploaded_file = st.file_uploader("choose a csv file")

if uploaded_file:
    try:
        # Mencoba membaca file CSV
        df = pd.read_csv(uploaded_file)
        # Menampilkan DataFrame jika berhasil dibaca
        st.dataframe(df)
    except Exception as e:
        # Menangani kesalahan pembacaan file
        st.error(f"Error: {str(e)}")

# Camera input
picture = st.camera_input("Take a input")
if picture:
    st.image(picture)

# Button
if st.button("say hello"):
    st.write("hello there")

# Check box
agree = st.checkbox("I agree")
if agree:
    st.write("Welcome to MyApp")

# Radio btn
genre = st.radio(
    label="what's your fav genre",
    options=("comedy", "drama", "documentary"),
    horizontal=False
)

# Select box
genre2 = st.selectbox(
    label="what's your fav genre",
    options=("comedy", "drama", "documentary")
)

# Multiselect
genre3 = st.multiselect(
    label="What's your favorite movie genre",
    options=('Comedy', 'Drama', 'Documentary')
)

# Slider
values = st.slider(
    label="select a range of values",
    min_value=0, max_value=100, value=(0, 100)
)
st.write("Values: ", values)