from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import pandas as pd
import os

app = Flask(__name__)
CORS(app)

# ============================================================
# MODEL PATH
# ============================================================

MODEL_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "disease_model.pkl"
)

# ============================================================
# LOAD MODEL
# ============================================================

try:
    loaded_model = joblib.load(MODEL_PATH)

    print("=" * 50)
    print("MODEL LOADED SUCCESSFULLY")
    print("Loaded object type:", type(loaded_model))

    # Your trained model is stored as a dictionary
    if isinstance(loaded_model, dict):

        print("Dictionary keys:", loaded_model.keys())

        model = loaded_model["pipeline"]
        label_encoder = loaded_model.get("label_encoder", None)
        feature_columns = loaded_model.get("feature_columns", None)

    else:
        model = loaded_model
        label_encoder = None
        feature_columns = None

    print("Final model type:", type(model))
    print("=" * 50)

except Exception as e:

    print("MODEL LOADING ERROR:")
    print(e)

    model = None
    label_encoder = None
    feature_columns = None


# ============================================================
# HOME
# ============================================================

@app.route("/")
def home():

    return jsonify({
        "message": "Disease Prediction API is running successfully!"
    })


# ============================================================
# PREDICTION
# ============================================================

@app.route("/predict", methods=["POST"])
def predict():

    try:

        # Get JSON data from frontend
        data = request.get_json()

        if not data:
            return jsonify({
                "success": False,
                "error": "No data received"
            }), 400

        print("\nReceived data:")
        print(data)

        # Convert data into DataFrame
        input_data = pd.DataFrame([data])

        # ====================================================
        # Make sure columns are in correct order
        # ====================================================

        if feature_columns is not None:

            # Add missing columns
            for column in feature_columns:

                if column not in input_data.columns:

                    input_data[column] = "No"

            # Keep exactly the columns used during training
            input_data = input_data[feature_columns]

        print("\nInput Data:")
        print(input_data)

        # ====================================================
        # MODEL PREDICTION
        # ====================================================

        prediction = model.predict(input_data)[0]

        print("\nRaw prediction:", prediction)

        # ====================================================
        # CONVERT 0 / 1 TO ORIGINAL LABEL
        # ====================================================

        if label_encoder is not None:

            try:

                prediction_label = label_encoder.inverse_transform(
                    [prediction]
                )[0]

            except Exception:

                prediction_label = str(prediction)

        else:

            # Fallback
            if str(prediction) == "1":
                prediction_label = "Positive"
            elif str(prediction) == "0":
                prediction_label = "Negative"
            else:
                prediction_label = str(prediction)

        print("Final prediction:", prediction_label)

        # ====================================================
        # RESPONSE
        # ====================================================

        return jsonify({

            "success": True,

            "prediction": str(prediction_label),

            "raw_prediction": str(prediction)

        })

    except Exception as e:

        print("\nPREDICTION ERROR:")
        print(e)

        return jsonify({

            "success": False,

            "error": str(e)

        }), 400


# ============================================================
# RUN SERVER
# ============================================================

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )