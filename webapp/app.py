from flask import Flask, render_template, request
import numpy as np
import pickle
import requests

app = Flask(__name__)

DBAPP_URL = "http://dbapp:8001"

# Load trained model
with open("model.pkl", "rb") as file:
    model = pickle.load(file)

species_names = [
    "setosa",
    "versicolor",
    "virginica"
]


@app.route("/", methods=["GET", "POST"])
def index():
    prediction = None
    error = None

    if request.method == "POST":
        try:
            measurements = [
                float(request.form["sepal_length"]),
                float(request.form["sepal_width"]),
                float(request.form["petal_length"]),
                float(request.form["petal_width"])
            ]

            if not all(0 < value <= 10 for value in measurements):
                raise ValueError(
                    "Measurements must be between 0 and 10."
                )

            values = np.array([measurements])
            result = model.predict(values)[0]

            prediction = species_names[int(result)]

            data = {
                "sepal_length": measurements[0],
                "sepal_width": measurements[1],
                "petal_length": measurements[2],
                "petal_width": measurements[3],
                "species": prediction
            }

            response = requests.post(
                f"{DBAPP_URL}/predictions",
                json=data,
                timeout=5
            )
            response.raise_for_status()

        except (ValueError, KeyError):
            error = "Please enter valid flower measurements."

        except requests.RequestException:
            error = (
                "Database service is unavailable. "
                "Please try again."
            )

    return render_template(
        "index.html",
        prediction=prediction,
        error=error
    )


@app.route("/health")
def health():
    return {"status": "healthy"}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)