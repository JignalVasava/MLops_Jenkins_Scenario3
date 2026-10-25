from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier
import pickle

iris = load_iris()

X = iris.data
y = iris.target

model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)

model.fit(X, y)

with open("model.pkl", "wb") as file:
    pickle.dump(model, file)

print("Iris model trained and saved successfully.")