import os
import pandas as pd
import joblib

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score


# ==========================================
# PATHS
# ==========================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

TRAINING_FILE = os.path.join(
    BASE_DIR, "dataset", "Training.csv"
)

TESTING_FILE = os.path.join(
    BASE_DIR, "dataset", "Testing.csv"
)

MODEL_DIR = os.path.join(
    BASE_DIR, "model"
)

MODEL_FILE = os.path.join(
    MODEL_DIR, "disease_model.pkl"
)


# ==========================================
# CHECK FILES
# ==========================================

if not os.path.exists(TRAINING_FILE):
    print("❌ Training.csv not found!")
    print(f"Expected location: {TRAINING_FILE}")
    exit()

if not os.path.exists(TESTING_FILE):
    print("❌ Testing.csv not found!")
    print(f"Expected location: {TESTING_FILE}")
    exit()


# ==========================================
# CREATE MODEL FOLDER
# ==========================================

os.makedirs(MODEL_DIR, exist_ok=True)


# ==========================================
# LOAD DATA
# ==========================================

print("📂 Loading dataset...")

training_data = pd.read_csv(TRAINING_FILE)
testing_data = pd.read_csv(TESTING_FILE)

print(f"✅ Training data: {training_data.shape}")
print(f"✅ Testing data:  {testing_data.shape}")


# ==========================================
# FIND TARGET COLUMN
# ==========================================

target_column = "prognosis"

if target_column not in training_data.columns:
    print("❌ 'prognosis' column not found in Training.csv")
    print("Available columns:")
    print(training_data.columns.tolist())
    exit()


# ==========================================
# SEPARATE FEATURES AND TARGET
# ==========================================

X_train = training_data.drop(
    columns=[target_column]
)

y_train = training_data[target_column]


X_test = testing_data.drop(
    columns=[target_column]
)

y_test = testing_data[target_column]


# ==========================================
# MAKE SURE TRAINING & TESTING FEATURES MATCH
# ==========================================

X_test = X_test.reindex(
    columns=X_train.columns,
    fill_value=0
)


# ==========================================
# TRAIN RANDOM FOREST MODEL
# ==========================================

print("\n🤖 Training Random Forest model...")

model = RandomForestClassifier(
    n_estimators=200,
    random_state=42,
    n_jobs=-1
)

model.fit(X_train, y_train)


# ==========================================
# TEST MODEL
# ==========================================

print("🧪 Testing model...")

predictions = model.predict(X_test)

accuracy = accuracy_score(
    y_test,
    predictions
)


# ==========================================
# SAVE MODEL
# ==========================================

joblib.dump(
    model,
    MODEL_FILE
)


# ==========================================
# SAVE SYMPTOM LIST
# ==========================================

symptoms_file = os.path.join(
    MODEL_DIR, "symptoms.pkl"
)

joblib.dump(
    list(X_train.columns),
    symptoms_file
)


# ==========================================
# RESULTS
# ==========================================

print("\n" + "=" * 50)
print("        PREDICTSITE MODEL TRAINING")
print("=" * 50)

print(f"Training samples : {len(X_train)}")
print(f"Testing samples  : {len(X_test)}")
print(f"Number of symptoms: {len(X_train.columns)}")
print(f"Disease classes  : {y_train.nunique()}")
print(f"Model accuracy   : {accuracy * 100:.2f}%")

print("\n✅ Model saved successfully!")
print(f"📁 {MODEL_FILE}")

print("\n✅ Symptom list saved successfully!")
print(f"📁 {symptoms_file}")

print("=" * 50)