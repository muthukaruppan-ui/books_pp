from fastapi import FastAPI
import joblib
from pydantic import BaseModel
from scipy.sparse import hstack

app = FastAPI()

# Load model
model = joblib.load("model/model.pkl")
tfidf = joblib.load("model/tfidf.pkl")
le_author = joblib.load("model/author.pkl")
le_genre = joblib.load("model/genre.pkl")

class Book(BaseModel):
    title: str
    author: str
    genre: str
    rating: float
    reviews: int

@app.get("/")
def home():
    return {"message": "API Running"}

@app.post("/predict")
def predict(book: Book):

    author = book.author if book.author in le_author.classes_ else "Unknown"
    genre = book.genre if book.genre in le_genre.classes_ else "Unknown"

    author_enc = le_author.transform([author])[0]
    genre_enc = le_genre.transform([genre])[0]

    title_vec = tfidf.transform([book.title])

    X = hstack([title_vec, [[author_enc, genre_enc, book.rating, book.reviews]]])

    price = model.predict(X)[0]

    return {"predicted_price": float(price)}
