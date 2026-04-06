import streamlit as st
import requests
import pandas as pd
import os
from datetime import datetime

st.set_page_config(page_title="Book Price Predictor", page_icon="📚")

st.title("📚 Book Price Predictor")

# 📖 Inputs
book_name = st.text_input("📖 Book Name")
author = st.text_input("✍️ Author Name")

# ⭐ Rating
st.markdown("### ⭐ Select Rating")

if "rating" not in st.session_state:
    st.session_state.rating = 3

cols = st.columns(5)
for i in range(5):
    if cols[i].button("⭐", key=i):
        st.session_state.rating = i + 1

rating = float(st.session_state.rating)
st.markdown("### " + "⭐"*int(rating) + "☆"*(5-int(rating)))

# 📄 Pages
pages = st.number_input("Pages (10–500)", 10, 500, 200)

# 🔥 Popularity
popularity = st.slider("Popularity (10–100)", 10, 100, 50)

st.markdown("---")

# 🚀 Predict
if st.button("🚀 Predict Price"):

    if not book_name or not author:
        st.error("Enter Book Name and Author")

    else:
        data = {
            "title": book_name,
            "author": author,
            "rating": rating,
            "pages": pages,
            "popularity": popularity
        }

        try:
            response = requests.post(
                "http://127.0.0.1:8000/predict",
                json=data
            )

            if response.status_code == 200:
                price = response.json()["predicted_price"]

                st.success(f"💰 Estimated Price: ₹{price}")

                # 💾 Save history
                file = "history.csv"

                new_data = pd.DataFrame([{
                    "Book": book_name,
                    "Author": author,
                    "Rating": rating,
                    "Pages": pages,
                    "Popularity": popularity,
                    "Price": price,
                    "Time": datetime.now()
                }])

                if os.path.exists(file):
                    old_data = pd.read_csv(file)
                    final_data = pd.concat([old_data, new_data], ignore_index=True)
                else:
                    final_data = new_data

                final_data.to_csv(file, index=False)

                st.info("📁 Saved to history.csv")

            else:
                st.error("❌ Backend error")

        except Exception as e:
            st.error(f"⚠️ Error: {e}")

# 📊 HISTORY SECTION WITH DELETE
if os.path.exists("history.csv"):
    st.markdown("---")
    st.markdown("### 📊 Prediction History")

    df = pd.read_csv("history.csv")

    if not df.empty:

        # 🗑️ Clear all button
        if st.button("🗑️ Clear All History"):
            os.remove("history.csv")
            st.rerun()

        for i, row in df.iterrows():
            col1, col2 = st.columns([8, 1])

            with col1:
                st.write(
                    f"📖 {row['Book']} | ✍️ {row['Author']} | ⭐ {row['Rating']} | "
                    f"📄 {row['Pages']} | 🔥 {row['Popularity']} → 💰 ₹{row['Price']}"
                )

            with col2:
                if st.button("❌", key=f"delete_{i}"):
                    df = df.drop(i)
                    df.to_csv("history.csv", index=False)
                    st.rerun()

    else:
        st.info("No history available")