# ============================================================
# Disease Prediction - Model Training
# ============================================================

import os
import joblib
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, LabelEncoder
from sklearn.impute import SimpleImputer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report


# ============================================================
# 1. FIND PROJECT DIRECTORY
# ============================================================

# train_model.py is inside:
# Disease-Prediction-MLOps-Starter/backend/

BACKEND_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(BACKEND_DIR)

DATA_DIR = os.path.join(PROJECT_DIR, "data")
DATA_FILE = os.path.join(DATA_DIR, "diabetes_data_upload.csv")

MODEL_FILE = os.path.join(BACKEND_DIR, "disease_model.pkl")


print("\n" + "=" * 60)
print("DISEASE PREDICTION - MODEL TRAINING")
print("=" * 60)

print("\nProject directory:")
print(PROJECT_DIR)

print("\nDataset path:")
print(DATA_FILE)


# ============================================================
# 2. CHECK DATASET
# ============================================================

if not os.path.exists(DATA_FILE):
    print("\nERROR: Dataset file not found!")
    print("Expected location:")
    print(DATA_FILE)
    raise FileNotFoundError(
        f"Dataset not found: {DATA_FILE}"
    )

print("\nDataset found successfully!")


# ============================================================
# 3. LOAD DATASET
# ============================================================

df = pd.read_csv(DATA_FILE)

print("\nDataset loaded successfully!")
print("Rows:", df.shape[0])
print("Columns:", df.shape[1])

print("\nColumn names:")
print(df.columns.tolist())


# ============================================================
# 4. CLEAN COLUMN NAMES
# ============================================================

df.columns = df.columns.str.strip()

# Remove completely empty rows
df = df.dropna(how="all")

print("\nDataset shape after cleaning:")
print(df.shape)


# ============================================================
# 5. FIND TARGET COLUMN
# ============================================================

possible_targets = [
    "Outcome",
    "outcome",
    "Class",
    "class",
    "target",
    "Target",
    "Diabetes",
    "diabetes"
]

target_column = None

for column in possible_targets:
    if column in df.columns:
        target_column = column
        break

if target_column is None:
    raise ValueError(
        "\nTarget column not found!\n"
        "Available columns are:\n"
        + str(df.columns.tolist())
    )

print("\nTarget column:")
print(target_column)


# ============================================================
# 6. REMOVE MISSING TARGET VALUES
# ============================================================

df = df.dropna(subset=[target_column])

X = df.drop(columns=[target_column])
y = df[target_column]


# ============================================================
# 7. ENCODE TARGET
# ============================================================

label_encoder = LabelEncoder()

y = label_encoder.fit_transform(y.astype(str))

print("\nTarget classes:")
print(label_encoder.classes_)


# ============================================================
# 8. IDENTIFY NUMERIC AND CATEGORICAL COLUMNS
# ============================================================

numeric_columns = X.select_dtypes(
    include=["int64", "int32", "float64", "float32"]
).columns.tolist()

categorical_columns = X.select_dtypes(
    include=["object", "category", "bool"]
).columns.tolist()


print("\nNumeric columns:")
print(numeric_columns)

print("\nCategorical columns:")
print(categorical_columns)


# ============================================================
# 9. NUMERIC DATA PIPELINE
# ============================================================

numeric_pipeline = Pipeline(
    steps=[
        (
            "imputer",
            SimpleImputer(strategy="median")
        )
    ]
)


# ============================================================
# 10. CATEGORICAL DATA PIPELINE
# ============================================================

categorical_pipeline = Pipeline(
    steps=[
        (
            "imputer",
            SimpleImputer(strategy="most_frequent")
        ),
        (
            "onehot",
            OneHotEncoder(
                handle_unknown="ignore",
                sparse_output=False
            )
        )
    ]
)


# ============================================================
# 11. COLUMN TRANSFORMER
# ============================================================

transformers = []

if numeric_columns:
    transformers.append(
        (
            "numeric",
            numeric_pipeline,
            numeric_columns
        )
    )

if categorical_columns:
    transformers.append(
        (
            "categorical",
            categorical_pipeline,
            categorical_columns
        )
    )

preprocessor = ColumnTransformer(
    transformers=transformers,
    remainder="drop"
)


# ============================================================
# 12. RANDOM FOREST MODEL
# ============================================================

model = RandomForestClassifier(
    n_estimators=100,
    random_state=42,
    class_weight="balanced"
)


# ============================================================
# 13. COMPLETE ML PIPELINE
# ============================================================

pipeline = Pipeline(
    steps=[
        (
            "preprocessor",
            preprocessor
        ),
        (
            "classifier",
            model
        )
    ]
)


# ============================================================
# 14. TRAIN TEST SPLIT
# ============================================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

print("\nTraining data:", X_train.shape)
print("Testing data:", X_test.shape)


# ============================================================
# 15. TRAIN MODEL
# ============================================================

print("\nTraining model...")

pipeline.fit(
    X_train,
    y_train
)

print("Model training completed!")


# ============================================================
# 16. PREDICTION
# ============================================================

y_pred = pipeline.predict(X_test)


# ============================================================
# 17. MODEL ACCURACY
# ============================================================

accuracy = accuracy_score(
    y_test,
    y_pred
)

print("\n" + "=" * 60)
print("MODEL PERFORMANCE")
print("=" * 60)

print("\nAccuracy:")
print(f"{accuracy * 100:.2f}%")


# ============================================================
# 18. CLASSIFICATION REPORT
# ============================================================

print("\nClassification Report:")

print(
    classification_report(
        y_test,
        y_pred,
        target_names=[
            str(label)
            for label in label_encoder.classes_
        ]
    )
)


# ============================================================
# 19. SAVE MODEL + LABEL ENCODER
# ============================================================

model_data = {
    "pipeline": pipeline,
    "label_encoder": label_encoder,
    "target_column": target_column,
    "feature_columns": X.columns.tolist()
}

joblib.dump(
    model_data,
    MODEL_FILE
)


# ============================================================
# 20. SUCCESS MESSAGE
# ============================================================

print("\n" + "=" * 60)
print("MODEL SAVED SUCCESSFULLY!")
print("=" * 60)

print("\nModel location:")
print(MODEL_FILE)

print("\nTraining completed successfully!")
print("=" * 60)