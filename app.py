import streamlit as st
import requests

st.title("📚 Book Price Prediction")

# Inputs
title = st.text_input("Book Title")
author = st.text_input("Author")

rating = st.slider("Rating", 0.0, 5.0, 3.5)

pages = st.number_input("Pages", min_value=1, value=200)
popularity = st.number_input("Popularity", min_value=0.0, value=100.0)

# Predict
if st.button("Predict Price"):

    data = {
        "title": title,
        "author": author,
        "rating": rating,
        "popularity": popularity,
        "pages": pages
    }

    try:
        response = requests.post(
            "https://books-pp.onrender.com/predict",
            json=data
        )

        if response.status_code == 200:
            result = response.json()
            st.success(f"💰 Predicted Price: ₹{result['predicted_price']}")
        else:
            st.error("Backend error")

    except:
        st.error("Cannot connect to API")