from fastapi import FastAPI
import joblib
from pydantic import BaseModel
import os

app = FastAPI()

# Load model
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
model = joblib.load(os.path.join(BASE_DIR, "../model/model.pkl"))

@app.get("/")
def home():
    return {"message": "API is running"}

class Book(BaseModel):
    title: str
    author: str
    rating: float
    pages: int
    popularity: float

@app.post("/predict")
def predict(book: Book):

    X = [[book.rating, book.pages, book.popularity]]

    price = model.predict(X)[0]

    return {"predicted_price": round(float(price), 2)}