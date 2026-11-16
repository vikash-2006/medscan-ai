import os
import joblib
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score

# Feature definitions for Sanjeevani Diagnostic ML Engine
FEATURE_NAMES = [
    "age",
    "blood_sugar",        # Fasting Glucose (mg/dL)
    "blood_pressure_sys", # Systolic (mmHg)
    "blood_pressure_dia", # Diastolic (mmHg)
    "bmi",                # Body Mass Index (kg/m^2)
    "cholesterol",        # Total Cholesterol (mg/dL)
    "hba1c"               # Glycated Hemoglobin (%)
]

def generate_synthetic_clinical_data(n_samples=2500, random_state=42):
    """
    Generates realistic clinical patient records with true physiological correlations.
    Risk Levels:
      0: Low Risk (Healthy)
      1: Moderate Risk (Borderline / Lifestyle changes required)
      2: High Risk (Significant Clinical Risk / Immediate medical consult)
    """
    rng = np.random.RandomState(random_state)
    
    # Generate age: 18 to 80
    age = rng.normal(48, 15, n_samples).clip(18, 85)
    
    # Fasting glucose: Normal ~85-99, Prediabetes ~100-125, Diabetes >= 126
    glucose_base = 75 + (age * 0.3) + rng.normal(15, 25, n_samples)
    blood_sugar = glucose_base.clip(65, 320)
    
    # Blood pressure: Systolic ~110-180, Diastolic ~70-110
    bp_sys = (100 + (age * 0.4) + rng.normal(10, 15, n_samples)).clip(90, 200)
    bp_dia = (65 + (bp_sys * 0.2) + rng.normal(5, 8, n_samples)).clip(60, 125)
    
    # BMI: ~18.5 - 42
    bmi = rng.normal(25.5, 4.8, n_samples).clip(16.0, 48.0)
    
    # Cholesterol: ~140 - 320 mg/dL
    cholesterol = (150 + (age * 0.6) + (bmi * 1.5) + rng.normal(10, 30, n_samples)).clip(120, 380)
    
    # HbA1c: Normal <5.7%, Prediabetes 5.7-6.4%, Diabetes >=6.5%
    hba1c = (4.5 + (blood_sugar / 30.0) + rng.normal(0, 0.4, n_samples)).clip(4.2, 13.5)
    
    X = np.column_stack([age, blood_sugar, bp_sys, bp_dia, bmi, cholesterol, hba1c])
    
    # Compute clinical severity risk score
    risk_score = (
        (blood_sugar > 125).astype(int) * 3 +
        ((blood_sugar >= 100) & (blood_sugar <= 125)).astype(int) * 1 +
        (bp_sys >= 140).astype(int) * 2 +
        ((bp_sys >= 125) & (bp_sys < 140)).astype(int) * 1 +
        (hba1c >= 6.5).astype(int) * 3 +
        ((hba1c >= 5.7) & (hba1c < 6.5)).astype(int) * 1 +
        (cholesterol >= 240).astype(int) * 2 +
        ((cholesterol >= 200) & (cholesterol < 240)).astype(int) * 1 +
        (bmi >= 30).astype(int) * 2 +
        (age > 60).astype(int) * 1
    )
    
    # Map score to 3-class risk: 0=Low (0-2), 1=Moderate (3-5), 2=High (6+)
    y = np.zeros(n_samples, dtype=int)
    y[(risk_score >= 3) & (risk_score <= 5)] = 1
    y[risk_score >= 6] = 2
    
    return X, y

def train_and_save_pipeline(output_path=None):
    if output_path is None:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        output_path = os.path.join(base_dir, "diagnostic_model.joblib")
        
    print("Generating clinical training dataset...")
    X, y = generate_synthetic_clinical_data(n_samples=3000)
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    # Preprocessor using StandardScaler (as described in resume)
    preprocessor = ColumnTransformer(
        transformers=[
            ('scaler', StandardScaler(), list(range(len(FEATURE_NAMES))))
        ]
    )
    
    # Random Forest Classifier with calibrated probability estimation
    classifier = RandomForestClassifier(
        n_estimators=150,
        max_depth=10,
        min_samples_split=4,
        random_state=42,
        class_weight='balanced'
    )
    
    pipeline = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('classifier', classifier)
    ])
    
    print("Training Sanjeevani Diagnostic ML Pipeline...")
    pipeline.fit(X_train, y_train)
    
    # Evaluate
    y_pred = pipeline.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    print(f"Validation Accuracy: {acc * 100:.2f}%")
    print("\nClassification Report:\n", classification_report(y_test, y_pred, target_names=["Low Risk", "Moderate Risk", "High Risk"]))
    
    # Package model metadata
    model_artifact = {
        "pipeline": pipeline,
        "feature_names": FEATURE_NAMES,
        "classes": ["Low Risk", "Moderate Risk", "High Risk"],
        "accuracy": acc
    }
    
    joblib.dump(model_artifact, output_path)
    print(f"Model successfully serialized and saved to: {output_path}")
    return output_path

if __name__ == "__main__":
    train_and_save_pipeline()
