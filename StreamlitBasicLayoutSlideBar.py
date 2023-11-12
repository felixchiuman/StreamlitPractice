import streamlit as st

st.title("Belajar analisis data")

with st.sidebar:
    st.text("Ini sidebar")

    values = st.slider(
        label="select a range",
        min_value=0, max_value=100, value=(0, 100)
    )
    st.write("values: ", values)
