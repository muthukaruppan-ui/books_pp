from fastapi import FastAPI
import joblib
import numpy as np
from pydantic import BaseModel

app = FastAPI()

model = joblib.load("model/model.pkl")

class Book(BaseModel):
    title: str
    author: str
    rating: float
    popularity: float
    pages: int

@app.post("/predict")
def predict(book: Book):

    X = np.array([[book.pages, book.rating, book.popularity]])

    # Main prediction
    price_log = model.predict(X)[0]
    price = np.expm1(price_log)

    # 🔥 Confidence (based on tree variance)
    preds = []
    for tree in model.estimators_:
        preds.append(np.expm1(tree.predict(X)[0]))

    confidence = max(0, 100 - np.std(preds))  # lower std = higher confidence
    confidence = round(min(confidence, 100), 2)

    return {
        "predicted_price": round(float(price), 2),
        "confidence": confidence
    }