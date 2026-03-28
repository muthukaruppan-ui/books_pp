import streamlit as st
import requests

st.title("📚 Book Price Prediction System")

st.write("Enter book details:")

# All inputs (UX purpose)
title = st.text_input("Book Title")
author = st.text_input("Author Name")
rating = st.slider("Rating", 0.0, 5.0, 3.5)
popularity = st.number_input("Popularity (Rating × Reviews)", min_value=0.0, value=100.0)
pages = st.number_input("Pages", min_value=1, value=200)

# Predict
if st.button("Predict Price"):

    data = {
        "title": title,
        "author": author,
        "rating": rating,
        "popularity": popularity,
        "pages": pages
    }

    response = requests.post("http://127.0.0.1:8000/predict", json=data)

    if response.status_code == 200:
        result = response.json()

        st.success(f"💰 Predicted Price: ₹{result['predicted_price']}")
        st.info("Prediction based on pages, rating, and popularity")
    else:
        st.error("Backend error")