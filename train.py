import os
import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_absolute_error
from sklearn.linear_model import LinearRegression

os.makedirs("model", exist_ok=True)

# Load dataset
df = pd.read_csv("data/books.csv")

# Features
X = df[["Rating", "Pages", "Popularity"]]

# Target
y = df["Price"]

# Split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# ✅ FINAL MODEL
model = LinearRegression()
model.fit(X_train, y_train)

# Predict
y_pred = model.predict(X_test)

print("✅ R2 Score:", r2_score(y_test, y_pred))
print("✅ MAE:", mean_absolute_error(y_test, y_pred))

# Save model
joblib.dump(model, "model/model.pkl")

print("🚀 Model trained successfully!")