"""Diabetes Risk Assessment - Streamlit app (RCAI classroom project).

Run locally:  streamlit run app.py
"""
import json
import os
from datetime import datetime, timedelta, timezone

import joblib
import numpy as np
import pandas as pd
import streamlit as st
from fpdf import FPDF

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


@st.cache_resource(show_spinner="Preparing the four models (first start only)...")
def load_models_and_metrics():
    # 1. Saved models (after running train.py locally), 2. rebuild the tuned models from the
    # grid-search results in metrics.json (a few seconds), 3. full grid search (about a minute).
    from train import fit_best, train_models
    if os.path.exists("metrics.json"):
        with open("metrics.json") as f:
            metrics = json.load(f)
        if os.path.exists("models.joblib"):
            return joblib.load("models.joblib"), metrics
        return fit_best(metrics), metrics
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

DIET_OPTIONS = ["Vegetarian", "Vegan", "No eggs", "No nuts", "No fish or seafood", "No soy",
                "No gluten / wheat", "No dairy"]


def food_guide(diet):
    """Food tips that avoid the user's allergies and diet restrictions."""
    d = set(diet)
    vegan = "Vegan" in d
    veg = vegan or "Vegetarian" in d
    no_egg = vegan or "No eggs" in d
    no_fish = veg or "No fish or seafood" in d
    no_soy = "No soy" in d
    no_nuts = "No nuts" in d
    no_gluten = "No gluten / wheat" in d
    no_dairy = vegan or "No dairy" in d

    protein = []
    if not no_fish:
        protein.append("fish")
    if not veg:
        protein.append("chicken")
    if not no_soy:
        protein.append("tofu or tempeh")
    if not no_egg:
        protein.append("eggs")
    protein += ["dhal or lentils", "chickpeas"]

    base = "brown rice porridge or rice thosai/idli" if no_gluten else "oats or wholemeal bread"
    if not no_egg:
        topping = "an egg"
    elif not no_soy:
        topping = "tofu scramble"
    elif not no_nuts:
        topping = "peanut butter"
    else:
        topping = "a banana or fruit"

    snacks = ["guava", "apple"]
    if not no_nuts:
        snacks.append("a handful of nuts")
    if not no_dairy:
        snacks.append("plain unsweetened yoghurt")
    snacks.append("roasted chickpeas")

    food = [
        "Use the Malaysian Healthy Plate (Suku-Suku Separuh): half vegetables and fruit, "
        f"a quarter protein ({', '.join(protein)}), a quarter "
        + ("rice or rice noodles (bihun, kuey teow)." if no_gluten else "rice or noodles."),
        "Drink plain water; order teh O or kopi O kosong / kurang manis instead of teh tarik or sirap.",
        f"Breakfast: {base} with {topping} instead of roti canai or nasi lemak.",
        f"Snacks: {', '.join(snacks[:-1])} or {snacks[-1]} instead of kuih, biscuits or fried snacks.",
        "Choose grilled, steamed or soup dishes over fried and santan (coconut milk) dishes.",
    ]
    if diet:
        food.append("Adjusted for your diet: " + ", ".join(diet) + ". Always check food labels "
                    "and follow your doctor's or dietitian's advice for allergies.")
    return food


def weekly_plan(band, bmi, glucose, weight=None, gentle=False, diet=()):
    """Personalised 7-day exercise plan and food guide, based on risk level, BMI and glucose.
    gentle=True (age 65+ or limited mobility) gives a low-impact plan."""
    heavy = bmi >= 27.5  # Asian cut-off for obesity: prefer low-impact exercise
    cardio = "swimming or cycling" if heavy else "brisk walking"
    if gentle:
        days = [
            ("Monday", "10-15 min easy walk, twice a day (indoors or with support if needed)"),
            ("Tuesday", "15 min chair exercises: seated leg raises, arm circles, sit-to-stand"),
            ("Wednesday", "15-20 min easy walk or water walking in a pool"),
            ("Thursday", "10 min balance practice holding a chair (heel raises, side leg lifts) "
                         "+ gentle stretching"),
            ("Friday", "10-15 min easy walk, twice a day"),
            ("Saturday", "20-30 min tai chi, gentle yoga or water exercise"),
            ("Sunday", "Rest"),
        ]
    elif band == "Low":
        days = [
            ("Monday", f"30 min {cardio}"),
            ("Tuesday", "20-30 min strength exercises (squats, wall push-ups, resistance band)"),
            ("Wednesday", "30 min brisk walking"),
            ("Thursday", "Rest or 15 min stretching"),
            ("Friday", f"30 min {cardio}"),
            ("Saturday", "45 min active outing: badminton, hiking or a park walk"),
            ("Sunday", "Rest"),
        ]
    elif band == "Moderate":
        days = [
            ("Monday", f"30 min {cardio} + 10 min walk after dinner"),
            ("Tuesday", "30 min strength exercises (squats, lunges, resistance band)"),
            ("Wednesday", f"40 min {cardio}"),
            ("Thursday", "20 min yoga or stretching + 10 min walk after dinner"),
            ("Friday", f"30 min {cardio} + 10 min walk after dinner"),
            ("Saturday", "45-60 min active outing: badminton, hiking or cycling"),
            ("Sunday", "20 min light walk"),
        ]
    else:
        days = [
            ("Monday", "20-30 min easy walk, ideally after a meal"),
            ("Tuesday", "20 min light strength exercises (chair squats, wall push-ups)"),
            ("Wednesday", "30 min easy walk"),
            ("Thursday", "15 min stretching + 10 min walk after dinner"),
            ("Friday", "30 min easy walk"),
            ("Saturday", f"30-40 min light {cardio}"),
            ("Sunday", "Rest"),
        ]
    food = food_guide(diet)
    if glucose >= 140 or band != "Low":
        food.insert(1, "Keep rice to about 1 cup per meal and switch to brown rice or "
                       "mixed rice when you can.")
    if bmi >= 23 and weight:
        food.append(f"Weight goal: losing 5-7% of your weight ({weight * 0.05:.1f}-"
                    f"{weight * 0.07:.1f} kg) over 6 months lowers diabetes risk.")
    elif bmi >= 23:
        food.append("Weight goal: losing 5-7% of your body weight over 6 months lowers diabetes risk.")
    note = ("Start slowly and build up. Check with a doctor before starting exercise, "
            "especially with high risk or other health conditions.")
    if gentle:
        note = ("Gentle plan for age 65+ or limited mobility. Do only what feels comfortable, "
                "use a chair or rail for support, and have someone nearby. Stop and seek help if "
                "you feel pain, dizziness, chest pain or shortness of breath. Check with a doctor "
                "or physiotherapist before starting.")
    return days, food, note


def malaysia_now():
    # The cloud server runs on UTC; reports show Malaysia time (UTC+8).
    return datetime.now(timezone(timedelta(hours=8))).strftime("%d %b %Y, %I:%M %p (MYT)")


def pdf_safe(text):
    # The built-in PDF font covers Latin-1 only, so swap the few symbols outside it.
    text = str(text).replace("μ", "u").replace("–", "-").replace("’", "'")
    return text.encode("latin-1", "replace").decode("latin-1")


def make_pdf(rows, band, prob, model_name, tips, warning, plan=None):
    """Build the PDF report and return its bytes."""
    pdf = FPDF()
    pdf.add_page()
    pdf.set_margins(18, 18, 18)
    pdf.set_font("Helvetica", "B", 18)
    pdf.cell(0, 10, "Diabetes Risk Assessment Report", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(90, 90, 90)
    pdf.cell(0, 6, pdf_safe(f"Generated {malaysia_now()}"), new_x="LMARGIN", new_y="NEXT")
    pdf.ln(4)

    colour = {"Low": (34, 139, 34), "Moderate": (204, 153, 0), "High": (200, 30, 30)}[band]
    pdf.set_text_color(*colour)
    pdf.set_font("Helvetica", "B", 15)
    pdf.cell(0, 9, pdf_safe(f"Estimated risk: {band} ({prob:.0%} probability)"),
             new_x="LMARGIN", new_y="NEXT")
    pdf.set_text_color(0, 0, 0)
    pdf.set_font("Helvetica", "", 10)
    pdf.cell(0, 6, pdf_safe(f"Model used: {model_name}"), new_x="LMARGIN", new_y="NEXT")
    if warning:
        pdf.set_font("Helvetica", "B", 10)
        pdf.multi_cell(0, 6, pdf_safe(warning), new_x="LMARGIN", new_y="NEXT")
    pdf.ln(4)

    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(0, 8, "Your details", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "", 10)
    with pdf.table(col_widths=(45, 55), text_align=("LEFT", "LEFT"), line_height=7) as table:
        head = table.row()
        head.cell("Measurement")
        head.cell("Your value")
        for field, value in rows:
            r = table.row()
            r.cell(pdf_safe(field))
            r.cell(pdf_safe(value))
    pdf.ln(4)

    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(0, 8, "What you can do", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "", 10)
    for tip in tips:
        pdf.multi_cell(0, 6, pdf_safe(f"- {tip}"), new_x="LMARGIN", new_y="NEXT")
    pdf.ln(4)

    if plan:
        days, food, note = plan
        pdf.set_font("Helvetica", "B", 12)
        pdf.cell(0, 8, "Your weekly plan", new_x="LMARGIN", new_y="NEXT")
        pdf.set_font("Helvetica", "", 10)
        with pdf.table(col_widths=(25, 75), text_align=("LEFT", "LEFT"), line_height=7) as table:
            head = table.row()
            head.cell("Day")
            head.cell("Exercise")
            for day, activity in days:
                r = table.row()
                r.cell(day)
                r.cell(pdf_safe(activity))
        pdf.ln(3)
        pdf.set_font("Helvetica", "B", 10)
        pdf.cell(0, 7, "Food guide", new_x="LMARGIN", new_y="NEXT")
        pdf.set_font("Helvetica", "", 10)
        for item in food:
            pdf.multi_cell(0, 6, pdf_safe(f"- {item}"), new_x="LMARGIN", new_y="NEXT")
        pdf.set_font("Helvetica", "I", 9)
        pdf.multi_cell(0, 5, pdf_safe(note), new_x="LMARGIN", new_y="NEXT")
        pdf.ln(4)

    pdf.set_font("Helvetica", "I", 9)
    pdf.set_text_color(90, 90, 90)
    pdf.multi_cell(0, 5, "This report is for education and screening only. It is not a medical "
                         "diagnosis and does not replace a blood test or a doctor's advice. "
                         "Model trained on the Pima Indians Diabetes dataset (women aged 21+).")
    return bytes(pdf.output())


# ---------------------------------------------------------------- header
st.title("🩺 Diabetes Risk Assessment")
st.caption("An AI risk-screening tool for women aged 21+, trained on the Pima Indians Diabetes "
           "dataset (768 women). It estimates risk only and is not a medical diagnosis.")

tab_check, tab_models, tab_data, tab_about = st.tabs(
    ["Risk check", "Model performance", "Data insights", "About"])

# ---------------------------------------------------------------- risk check
with tab_check:
    left, right = st.columns([1, 1.2], gap="large")

    with left:
        st.subheader("Your details")
        st.info("This tool is for **women aged 21 and over**, the group the models were "
                "trained on.")
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
            pregnancies = num("Number of pregnancies (0 if none)", 0, 17, 0)
            glucose = num("Blood glucose (mg/dL)", 40, 400, 110, unit=" mg/dL",
                          help="2-hour glucose from an oral glucose tolerance test. "
                               "To convert from mmol/L, multiply by 18.")
            bp = num("Diastolic blood pressure (mmHg) - the lower number", 40, 130, 75, unit=" mmHg",
                     help="For a reading of 120/80, enter 80.")

            if bmi_mode == "Height and weight":
                h = num("Height (cm)", 120.0, 220.0, 160.0, step=0.1, unit=" cm")
                w = num("Weight (kg)", 30.0, 250.0, 60.0, step=0.1, unit=" kg")
                bmi = round(w / (h / 100) ** 2, 1) if h and w else 0.0
                if bmi and not 15 <= bmi <= 70:
                    errors.append(f"Your height and weight give a BMI of {bmi}, which is outside 15-70.")
            else:
                bmi = num("BMI (kg/m²)", 15.0, 70.0, 24.0, step=0.1, unit=" kg/m²")

            family = st.selectbox("Family history of diabetes", list(FAMILY_HISTORY))
            diet = st.multiselect("Food allergies or diet (optional)", DIET_OPTIONS,
                                  placeholder="None",
                                  help="The food guide will avoid these foods.")
            limited = st.checkbox("I have joint pain or limited mobility",
                                  help="Gives a gentle, low-impact exercise plan. "
                                       "This is applied automatically from age 65.")

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
            mm = metrics[model_name]
            st.caption(f"{model_name} on the 154-patient test set: accuracy {mm['accuracy']:.1%}, "
                       f"precision {mm['precision']:.1%}, recall {mm['recall']:.1%}.")
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

            gentle = limited or age >= 65
            plan = weekly_plan(band, bmi, glucose, w if bmi_mode == "Height and weight" else None,
                               gentle=gentle, diet=diet)
            st.markdown("**Your weekly plan**")
            p_ex, p_food = st.tabs(["Exercise", "Food guide"])
            with p_ex:
                st.dataframe(pd.DataFrame(plan[0], columns=["Day", "Exercise"]),
                             hide_index=True, width="stretch")
            with p_food:
                for item in plan[1]:
                    st.markdown(f"- {item}")
            st.caption(plan[2])

            report = pd.DataFrame({
                "Field": ["Date", "Age", "Pregnancies", "Glucose (mg/dL)", "Diastolic BP (mmHg)",
                          "BMI", "Family history", "Skin thickness (mm)", "Insulin (μU/mL)",
                          "Joint pain / limited mobility", "Food allergies or diet", "Model", "Probability", "Risk level"],
                "Value": [malaysia_now(), age, pregnancies, glucose,
                          bp, bmi, family, "not given" if skin is None else skin, "not given" if insulin is None else insulin,
                          "Yes" if limited else "No", ", ".join(diet) or "None", model_name, f"{prob:.0%}",
                          band + (" (glucose in diabetic range)" if override else "")],
            })
            details = [(f, v) for f, v in zip(report["Field"], report["Value"])
                       if f not in ("Date", "Model", "Probability", "Risk level")]
            if override:
                warning = "Glucose is 200 mg/dL or higher, which is in the diabetic range. Please see a doctor."
            elif glucose >= 140:
                warning = "Glucose of 140-199 mg/dL is in the pre-diabetes range."
            else:
                warning = ""
            st.markdown("**Download your report**")
            d1, d2 = st.columns(2)
            d1.download_button("PDF (easy to open and print)",
                               make_pdf(details, band, prob, model_name, TIPS[band], warning, plan),
                               file_name="diabetes_risk_report.pdf", mime="application/pdf",
                               width="stretch")
            d2.download_button("CSV (for Excel)", report.to_csv(index=False).encode("utf-8-sig"),
                               file_name="diabetes_risk_report.csv", mime="text/csv",
                               width="stretch")

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
