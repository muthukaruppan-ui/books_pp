import os
import pandas as pd
import numpy as np
import joblib

from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_absolute_error
from sklearn.ensemble import RandomForestRegressor

os.makedirs("model", exist_ok=True)

# Load dataset
df = pd.read_csv("data/books.csv")

# Remove outliers
df = df[df["Price"] < df["Price"].quantile(0.95)]

# Create popularity
df["Popularity"] = df["Rating"] * df["Reviews"]

# Features (ONLY THESE)
X = df[["Pages", "Rating", "Popularity"]]

# Target
y = np.log1p(df["Price"])

# Split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# Model
model = RandomForestRegressor(n_estimators=300)
model.fit(X_train, y_train)

# Evaluate
y_pred = model.predict(X_test)

y_test_actual = np.expm1(y_test)
y_pred_actual = np.expm1(y_pred)

print("R2:", r2_score(y_test_actual, y_pred_actual))
print("MAE:", mean_absolute_error(y_test_actual, y_pred_actual))

# Save
joblib.dump(model, "model/model.pkl")

print("Model trained!")