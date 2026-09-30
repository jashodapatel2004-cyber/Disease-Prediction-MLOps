import React, { useState } from "react";
import { createRoot } from "react-dom/client";
import "./styles.css";

const symptoms = [
  "Polyuria",
  "Polydipsia",
  "sudden weight loss",
  "weakness",
  "Polyphagia",
  "Genital thrush",
  "visual blurring",
  "Itching",
  "Irritability",
  "delayed healing",
  "partial paresis",
  "muscle stiffness",
  "Alopecia",
  "Obesity",
];

function App() {
  const [age, setAge] = useState("");
  const [gender, setGender] = useState("Male");

  const [values, setValues] = useState({});

  const [result, setResult] = useState("");

  const [loading, setLoading] = useState(false);

  // ==========================================================
  // HANDLE SYMPTOM CHANGE
  // ==========================================================

  const handleChange = (symptom, value) => {
    setValues((previousValues) => ({
      ...previousValues,
      [symptom]: value,
    }));
  };

  // ==========================================================
  // PREDICT DISEASE
  // ==========================================================

  const predictDisease = async () => {
    if (!age) {
      alert("Please enter Age");
      return;
    }

    // Create request data
    const data = {
      Age: Number(age),
      Gender: gender,
    };

    // Add all symptoms
    symptoms.forEach((symptom) => {
      data[symptom] = values[symptom] || "No";
    });

    console.log("Sending data to backend:");
    console.log(data);

    try {
      setLoading(true);
      setResult("");

      // ======================================================
      // SEND DATA TO DEPLOYED FLASK API
      // ======================================================

      const response = await fetch(
        "https://disease-prediction-latest.onrender.com/predict",
        {
          method: "POST",

          headers: {
            "Content-Type": "application/json",
          },

          body: JSON.stringify(data),
        }
      );

      const resultData = await response.json();

      console.log("Backend response:");
      console.log(resultData);

      // ======================================================
      // SUCCESS
      // ======================================================

      if (resultData.success) {
        setResult(resultData.prediction);
      }

      // ======================================================
      // BACKEND ERROR
      // ======================================================

      else {
        setResult("Error: " + resultData.error);
      }
    }

    // ========================================================
    // CONNECTION ERROR
    // ========================================================

    catch (error) {
      console.error(error);

      setResult(
        "Backend connection failed. Please try again."
      );
    }

    finally {
      setLoading(false);
    }
  };

  // ==========================================================
  // UI
  // ==========================================================

  return (
    <div className="app">

      <div className="container">

        <h1>
          🩺 DiabetesAI
        </h1>

        <p className="subtitle">
          Diabetes Disease Prediction System
        </p>

        <div className="form">

          {/* AGE */}

          <label>
            Age
          </label>

          <input
            type="number"
            value={age}
            onChange={(e) => setAge(e.target.value)}
            placeholder="Enter age"
          />

          {/* GENDER */}

          <label>
            Gender
          </label>

          <select
            value={gender}
            onChange={(e) => setGender(e.target.value)}
          >

            <option value="Male">
              Male
            </option>

            <option value="Female">
              Female
            </option>

          </select>

          {/* SYMPTOMS */}

          <h2>
            Symptoms
          </h2>

          {symptoms.map((symptom) => (

            <div
              className="symptom"
              key={symptom}
            >

              <label>
                {symptom}
              </label>

              <select
                value={values[symptom] || "No"}

                onChange={(e) =>
                  handleChange(
                    symptom,
                    e.target.value
                  )
                }
              >

                <option value="Yes">
                  Yes
                </option>

                <option value="No">
                  No
                </option>

              </select>

            </div>

          ))}

          {/* BUTTON */}

          <button
            onClick={predictDisease}
            disabled={loading}
          >

            {loading
              ? "Predicting..."
              : "Predict Disease"
            }

          </button>

          {/* RESULT */}

          {result && (

            <div className="result">

              <h2>
                Prediction Result
              </h2>

              <p>
                {result}
              </p>

            </div>

          )}

        </div>

      </div>

    </div>
  );
}

createRoot(
  document.getElementById("root")
).render(

  <React.StrictMode>

    <App />

  </React.StrictMode>

);