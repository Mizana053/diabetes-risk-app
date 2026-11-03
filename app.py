"""Diabetes Risk Assessment - Streamlit app (RCAI classroom project).

Run locally:  streamlit run app.py
"""
import json
import os
from datetime import datetime

import joblib
import numpy as np
import pandas as pd
import streamlit as st

st.set_page_config(page_title="Diabetes Risk Assessment", page_icon="🩺", layout="wide")

FEATURES = ["Pregnancies", "Glucose", "BloodPressure", "SkinThickness", "Insulin",
            "BMI", "DiabetesPedigreeFunction", "Age"]
COLUMNS = ["Pregnancies", "Glucose", "BloodPressure", "SkinThickness",
           "Insulin", "BMI", "DiabetesPedigreeFunction", "Age", "Outcome"]
# Family history choices mapped to typical Diabetes Pedigree Function values
FAMILY_HISTORY = {
    "No known family history": 0.25,
    "One parent or sibling with diabetes": 0.55,
    "Several close relatives with diabetes": 0.90,
}


@st.cache_resource(show_spinner="Training the four models (first start only, about a minute)...")
def load_models_and_metrics():
    # Use saved models if present; otherwise train them from diabetes.csv (train.py).
    if os.path.exists("models.joblib") and os.path.exists("metrics.json"):
        with open("metrics.json") as f:
            return joblib.load("models.joblib"), json.load(f)
    from train import train_models
    return train_models(verbose=False)


@st.cache_data
def load_data():
    df = pd.read_csv("diabetes.csv", header=None, names=COLUMNS)
    return df


models, metrics = load_models_and_metrics()
data = load_data()
best_model = max(metrics, key=lambda m: metrics[m]["cv10_accuracy"])


def risk_band(p):
    if p < 0.30:
        return "Low", "🟢"
    if p < 0.60:
        return "Moderate", "🟡"
    return "High", "🔴"


TIPS = {
    "Low": [
        "Keep up regular activity: at least 150 minutes of moderate exercise a week.",
        "Keep sugary drinks and refined carbohydrates (white rice, kuih, teh tarik) occasional.",
        "Re-check your blood glucose every 1-3 years, or sooner if anything changes.",
    ],
    "Moderate": [
        "Aim to lose 5-7% of body weight if your BMI is above 23 (Asian cut-off for overweight).",
        "Swap to wholegrains and fill half your plate with vegetables (the Suku-Suku Separuh plate).",
        "Walk 30 minutes a day, 5 days a week.",
        "Ask a clinic for a fasting glucose or HbA1c test within the next few months.",
    ],
    "High": [
        "See a doctor soon for a proper test (fasting glucose, HbA1c or OGTT).",
        "Cut sugary drinks completely and reduce portion sizes of rice and noodles.",
        "Start daily light exercise and track your weight weekly.",
        "If you have symptoms (constant thirst, frequent urination, blurred vision), seek care promptly.",
    ],
}

# ---------------------------------------------------------------- header
st.title("🩺 Diabetes Risk Assessment")
st.caption("An AI risk-screening tool trained on the Pima Indians Diabetes dataset (768 patients). "
           "It estimates risk only and is not a medical diagnosis.")

tab_check, tab_models, tab_data, tab_about = st.tabs(
    ["Risk check", "Model performance", "Data insights", "About"])

# ---------------------------------------------------------------- risk check
with tab_check:
    left, right = st.columns([1, 1.2], gap="large")

    with left:
        st.subheader("Your details")
        bmi_mode = st.radio("Body size", ["Height and weight", "I know my BMI"], horizontal=True)
        errors = []

        def num(label, lo, hi, value, step=1, help=None, optional=False, unit=""):
            """Number box that records an error if the value is outside a realistic range."""
            v = st.number_input(label, value=value, step=step, help=help,
                                placeholder="Not known" if optional else None)
            if v is not None and not lo <= v <= hi:
                errors.append(f"**{label}** must be between {lo} and {hi}{unit} (you entered {v:g}).")
            return v

        with st.form("inputs"):
            age = num("Age (years)", 21, 100, 35,
                      help="The model was trained on adults aged 21 and over.", unit=" years")
            pregnancies = num("Number of pregnancies (0 if none / male)", 0, 17, 0)
            glucose = num("Blood glucose (mg/dL)", 40, 400, 110, unit=" mg/dL",
                          help="2-hour glucose from an oral glucose tolerance test. "
                               "To convert from mmol/L, multiply by 18.")
            bp = num("Diastolic blood pressure (mmHg) - the lower number", 40, 130, 75, unit=" mmHg",
                     help="For a reading of 120/80, enter 80.")

            if bmi_mode == "Height and weight":
                h = num("Height (cm)", 120, 220, 160, unit=" cm")
                w = num("Weight (kg)", 30, 250, 60, unit=" kg")
                bmi = round(w / (h / 100) ** 2, 1) if h and w else 0.0
                if bmi and not 15 <= bmi <= 70:
                    errors.append(f"Your height and weight give a BMI of {bmi}, which is outside 15-70.")
            else:
                bmi = num("BMI (kg/m²)", 15.0, 70.0, 24.0, step=0.1, unit=" kg/m²")

            family = st.selectbox("Family history of diabetes", list(FAMILY_HISTORY))

            with st.expander("Optional: skin thickness and insulin (if known)"):
                st.caption("Leave blank if you don't know them. Missing values are filled in "
                           "from the most similar patients in the training data.")
                skin = num("Triceps skin fold thickness (mm)", 5, 100, None, optional=True, unit=" mm")
                insulin = num("2-hour serum insulin (μU/mL)", 10, 900, None, optional=True, unit=" μU/mL")

            model_name = st.selectbox("Prediction model", list(models),
                                      index=list(models).index(best_model),
                                      help=f"Default: {best_model}, which had the best "
                                           "10-fold cross-validation accuracy.")
            submitted = st.form_submit_button("Check my risk", type="primary",
                                              width="stretch")

    with right:
        st.subheader("Your result")
        if not submitted:
            st.info("Fill in your details and press **Check my risk**.")
        elif errors:
            st.error("Please correct these values first. They are outside realistic medical ranges:")
            for e in errors:
                st.markdown(f"- {e}")
        else:
            if bmi_mode == "Height and weight":
                st.caption(f"Your BMI from height and weight: **{bmi}**")
            row = pd.DataFrame([[pregnancies, glucose, bp,
                                 np.nan if skin is None else skin,
                                 np.nan if insulin is None else insulin,
                                 bmi, FAMILY_HISTORY[family], age]], columns=FEATURES)
            prob = float(models[model_name].predict_proba(row)[0, 1])
            band, icon = risk_band(prob)

            # Clinical override: a 2-hour glucose of 200 mg/dL or more is in the
            # diagnostic range for diabetes, and the training data stops at 199.
            override = glucose >= 200
            if override:
                band, icon = "High", "🔴"
                st.error("Your glucose is **200 mg/dL or higher**, which is in the diabetic range "
                         "on a glucose tolerance test. Please see a doctor.")
            elif glucose >= 140:
                st.warning("A 2-hour glucose of 140-199 mg/dL is in the pre-diabetes range.")

            st.metric("Estimated risk", f"{icon} {band}")
            st.caption(f"{prob:.0%} probability of diabetes ({model_name})")
            st.progress(min(max(prob, 0.0), 1.0))

            st.markdown("**All four models**")
            comp = pd.DataFrame({
                "Model": list(models),
                "Probability": [float(m.predict_proba(row)[0, 1]) for m in models.values()],
                "Test accuracy": [metrics[m]["accuracy"] for m in models],
            })
            comp["Risk"] = comp["Probability"].map(lambda p: risk_band(p)[0])
            st.dataframe(comp.style.format({"Probability": "{:.0%}", "Test accuracy": "{:.1%}"}),
                         hide_index=True, width="stretch")

            st.markdown("**What you can do**")
            for tip in TIPS[band]:
                st.markdown(f"- {tip}")

            report = pd.DataFrame({
                "Field": ["Date", "Age", "Pregnancies", "Glucose (mg/dL)", "Diastolic BP (mmHg)",
                          "BMI", "Family history", "Skin thickness (mm)", "Insulin (μU/mL)",
                          "Model", "Probability", "Risk level"],
                "Value": [datetime.now().strftime("%Y-%m-%d %H:%M"), age, pregnancies, glucose,
                          bp, bmi, family, "not given" if skin is None else skin, "not given" if insulin is None else insulin,
                          model_name, f"{prob:.0%}",
                          band + (" (glucose in diabetic range)" if override else "")],
            })
            st.download_button("Download my report (CSV)", report.to_csv(index=False),
                                file_name="diabetes_risk_report.csv", mime="text/csv")

    st.caption("⚠️ This tool is for education and screening only. It does not replace a "
               "blood test or a doctor's advice.")

# ---------------------------------------------------------------- model performance
with tab_models:
    st.subheader("How the models performed")
    st.write("Each model was tuned with 5-fold cross-validation (GridSearchCV) on 80% of the data "
             "and tested on the remaining 20% (154 patients). Because one 20% test set can be lucky "
             "or unlucky, the 10-fold cross-validation accuracy on all 768 patients is shown too.")
    table = pd.DataFrame([{
        "Model": name,
        "Test accuracy": m["accuracy"],
        "Required": m["target"],
        "Precision": m["precision"],
        "Recall": m["recall"],
        "F1": m["f1"],
        "10-fold CV accuracy": m["cv10_accuracy"],
        "Best settings": ", ".join(f"{k}={v}" for k, v in m["best_params"].items()),
    } for name, m in metrics.items()])
    pct = {c: "{:.1%}" for c in ["Test accuracy", "Required", "Precision", "Recall", "F1",
                                 "10-fold CV accuracy"]}
    st.dataframe(table.style.format(pct), hide_index=True, width="stretch")
    st.bar_chart(table.set_index("Model")[["Test accuracy", "Required"]])
    st.markdown(
        f"""
**Why {best_model} is the default:** it has the highest 10-fold cross-validation accuracy,
which is the most reliable measure on a dataset this small.

**Pre-processing**
- In this dataset a 0 for glucose, blood pressure, skin thickness, insulin or BMI means
  "not recorded", so those zeros were turned into missing values.
- Missing values (common for skin thickness, 30%, and insulin, 49%) were filled in from the
  5 most similar patients (KNN imputation), and all eight features were scaled.
"""
    )

# ---------------------------------------------------------------- data insights
with tab_data:
    st.subheader("About the training data")
    c1, c2, c3 = st.columns(3)
    c1.metric("Patients", len(data))
    c2.metric("Diabetic", f"{data['Outcome'].mean():.0%}")
    c3.metric("Average age", f"{data['Age'].mean():.0f}")

    clean = data.copy()
    zero_cols = ["Glucose", "BloodPressure", "SkinThickness", "Insulin", "BMI"]
    clean[zero_cols] = clean[zero_cols].replace(0, np.nan)

    st.markdown("**Missing values (recorded as 0 in the raw data)**")
    st.bar_chart(clean[zero_cols].isna().mean().rename("Share missing"))

    st.markdown("**Average values: diabetic vs not diabetic**")
    avg = clean.groupby("Outcome")[["Glucose", "BloodPressure", "BMI", "Age"]].mean()
    avg.index = ["Not diabetic", "Diabetic"]
    st.dataframe(avg.round(1), width="stretch")

    feature = st.selectbox("Compare a measure", ["Glucose", "BMI", "Age", "BloodPressure"])
    bins = pd.cut(clean[feature], 10)
    dist = clean.groupby([bins, "Outcome"], observed=True).size().unstack(fill_value=0)
    dist.columns = ["Not diabetic", "Diabetic"]
    dist.index = dist.index.astype(str)
    st.bar_chart(dist)

# ---------------------------------------------------------------- about
with tab_about:
    st.subheader("About this project")
    st.markdown(
        """
Built for the **Rocheston Certified AI Engineer (RCAI) classroom project**, APU Certified AI
Engineer programme 2026.

- **Data:** Pima Indians Diabetes dataset (National Institute of Diabetes and Digestive and
  Kidney Diseases), 768 adult female patients.
- **Models:** Logistic Regression, K-Nearest Neighbours, Random Forest, Decision Tree
  (scikit-learn), each tuned with GridSearchCV.
- **App:** Streamlit.

**Limitations:** the data comes from one population (Pima women aged 21+), so results may be
less accurate for other groups. Glucose values here are 2-hour oral glucose tolerance test
readings. Always confirm with a proper medical test.
"""
    )
