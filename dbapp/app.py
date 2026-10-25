from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///iris.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


class Prediction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sepal_length = db.Column(db.Float, nullable=False)
    sepal_width = db.Column(db.Float, nullable=False)
    petal_length = db.Column(db.Float, nullable=False)
    petal_width = db.Column(db.Float, nullable=False)
    species = db.Column(db.String(50), nullable=False)


with app.app_context():
    db.create_all()


@app.route("/")
def home():
    return "Iris Database Service is Running!"


@app.route("/predictions", methods=["GET"])
def get_predictions():
    records = Prediction.query.all()

    return jsonify([
        {
            "id": r.id,
            "sepal_length": r.sepal_length,
            "sepal_width": r.sepal_width,
            "petal_length": r.petal_length,
            "petal_width": r.petal_width,
            "species": r.species
        }
        for r in records
    ])


@app.route("/predictions", methods=["POST"])
def save_prediction():
    data = request.get_json(silent=True) or {}

    try:
        measurements = [
            float(data[key])
            for key in [
                "sepal_length",
                "sepal_width",
                "petal_length",
                "petal_width"
            ]
        ]

        species = data["species"]

        if not all(0 < value <= 10 for value in measurements):
            raise ValueError("Measurements must be between 0 and 10.")

        if species not in [
            "setosa",
            "versicolor",
            "virginica"
        ]:
            raise ValueError("Invalid Iris species.")

    except (KeyError, TypeError, ValueError) as error:
        return jsonify({"error": str(error)}), 400

    record = Prediction(
        sepal_length=measurements[0],
        sepal_width=measurements[1],
        petal_length=measurements[2],
        petal_width=measurements[3],
        species=species
    )

    db.session.add(record)
    db.session.commit()

    return jsonify({
        "message": "Prediction saved successfully",
        "id": record.id
    }), 201


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8001)