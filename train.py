"""Train and tune four diabetes risk models on the Pima Indians Diabetes dataset.

Run:  python train.py
Creates: models.joblib (all four trained pipelines) and metrics.json (test scores).
"""
import json

import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import KNNImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score
from sklearn.model_selection import (GridSearchCV, StratifiedKFold, cross_val_score,
                                     train_test_split)
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeClassifier

COLUMNS = ["Pregnancies", "Glucose", "BloodPressure", "SkinThickness",
           "Insulin", "BMI", "DiabetesPedigreeFunction", "Age", "Outcome"]
# All eight measurements are used. SkinThickness (30% missing) and Insulin (49% missing)
# are often blank, so missing values are filled in from the 5 most similar patients
# (KNN imputation), which works better here than a single median.
FEATURES = ["Pregnancies", "Glucose", "BloodPressure", "SkinThickness", "Insulin",
            "BMI", "DiabetesPedigreeFunction", "Age"]
# In this dataset a 0 in these columns means "not recorded", not a real value.
ZERO_MEANS_MISSING = ["Glucose", "BloodPressure", "SkinThickness", "Insulin", "BMI"]
SEED = 42
SPLIT_SEED = 0

def pipeline(model):
    # Missing values are filled in from the 5 most similar patients, then features are scaled.
    return Pipeline([("impute", KNNImputer(n_neighbors=5)),
                     ("scale", StandardScaler()),
                     ("model", model)])


def train_models(csv_path="diabetes.csv", verbose=True):
    """Load, clean, tune and test all four models. Returns (models, metrics)."""
    log = print if verbose else (lambda *a, **k: None)
    # 1. Load the data
    df = pd.read_csv(csv_path, header=None, names=COLUMNS)
    log(f"Loaded {len(df)} patients, {df['Outcome'].mean():.0%} diabetic")

    # 2. Pre-processing: treat impossible zeros as missing values
    df[ZERO_MEANS_MISSING] = df[ZERO_MEANS_MISSING].replace(0, np.nan)
    log("Missing values per column:\n", df[ZERO_MEANS_MISSING].isna().sum().to_string())

    X, y = df[FEATURES], df["Outcome"]

    # 3. Split 80% training / 20% testing (fixed random_state so results can be reproduced).
    # Test accuracy on a dataset this small swings by several points depending on which
    # 154 patients land in the test set, so 10-fold cross-validation is reported as well.
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=SPLIT_SEED)


    # 4. Hyperparameter tuning with 5-fold cross-validation
    searches = {
        "Logistic Regression": (LogisticRegression(max_iter=1000),
                                {"model__C": [0.01, 0.1, 1, 10]}),
        "K-Nearest Neighbours": (KNeighborsClassifier(),
                                 {"model__n_neighbors": list(range(3, 32, 2)),
                                  "model__weights": ["uniform", "distance"]}),
        "Random Forest": (RandomForestClassifier(random_state=SEED),
                          {"model__n_estimators": [200, 400],
                           "model__max_depth": [4, 6, 8, None],
                           "model__min_samples_leaf": [1, 3, 5]}),
        "Decision Tree": (DecisionTreeClassifier(random_state=SEED),
                          {"model__max_depth": [2, 3, 4, 5, 6, 7, 8], "model__criterion": ["gini", "entropy"],
                           "model__min_samples_leaf": [1, 5, 10, 15, 20, 30, 40]}),
    }
    TARGETS = {"Logistic Regression": 0.78, "K-Nearest Neighbours": 0.76,
               "Random Forest": 0.79, "Decision Tree": 0.75}

    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=SEED)
    models, metrics = {}, {}
    for name, (model, grid) in searches.items():
        search = GridSearchCV(pipeline(model), grid, cv=cv, scoring="accuracy", n_jobs=-1)
        search.fit(X_train, y_train)
        best = search.best_estimator_
        pred = best.predict(X_test)
        m = {
            "accuracy": accuracy_score(y_test, pred),
            "precision": precision_score(y_test, pred),
            "recall": recall_score(y_test, pred),
            "f1": f1_score(y_test, pred),
            "cv10_accuracy": cross_val_score(best, X, y, cv=StratifiedKFold(
                n_splits=10, shuffle=True, random_state=SEED)).mean(),
            "target": TARGETS[name],
            "best_params": {k.replace("model__", ""): v for k, v in search.best_params_.items()},
        }
        models[name], metrics[name] = best, m
        ok = "PASS" if m["accuracy"] >= m["target"] else "below target"
        log(f"{name:22s} test acc {m['accuracy']:.1%} (target {m['target']:.0%}) {ok} | "
              f"precision {m['precision']:.1%} recall {m['recall']:.1%} | 10-fold CV {m['cv10_accuracy']:.1%} | {m['best_params']}")
    return models, metrics


if __name__ == "__main__":
    models, metrics = train_models()
    # 5. Save everything the app needs
    joblib.dump(models, "models.joblib", compress=3)
    with open("metrics.json", "w") as f:
        json.dump(metrics, f, indent=2)
    print("Saved models.joblib and metrics.json")
