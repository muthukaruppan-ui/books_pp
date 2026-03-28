from fastapi import FastAPI
import joblib
import numpy as np
from pydantic import BaseModel


app = FastAPI()

# Load model
model = joblib.load("model/model.pkl")

# Root route
@app.get("/")
def home():
    return {"message": "API is running"}

# Input schema
class Book(BaseModel):
    title: str
    author: str
    rating: float
    popularity: float
    pages: int

# Prediction API
@app.post("/predict")
def predict(book: Book):

    X = np.array([[book.pages, book.rating, book.popularity]])

    price_log = model.predict(X)[0]
    price = np.expm1(price_log)

    return {
        "predicted_price": round(float(price), 2)
    }