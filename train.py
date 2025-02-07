# train.py - Train and save Linear Regression model
import pandas as pd
import pickle
import datetime
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

# Load dataset
df = pd.read_csv("data/dataset.csv")

# Split features and target
X = df[["YearsExperience"]]
y = df["Salary"]

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
model = LinearRegression()
model.fit(X_train, y_train)

# Save previous model with timestamp
timestamp = datetime.datetime.now().strftime("%d%m%y%H%M")
with open(f"models/model_{timestamp}.pkl", "wb") as f:
    pickle.dump(model, f)

# Save latest model
with open("models/model.pkl", "wb") as f:
    pickle.dump(model, f)

print("Model trained and saved!")