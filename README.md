# Diabetes Risk Assessment (RCAI classroom project)

A Streamlit web app for women aged 21+ that estimates diabetes risk from glucose (mmol/L or
mg/dL), blood pressure, BMI (or height and weight), age, pregnancies, family history and (if known)
skin thickness and insulin, using four tuned scikit-learn models. Available in English and
Bahasa Melayu.

Features: risk level with a "Why this result?" chart, a what-if simulator, a personalised weekly
exercise plan and food guide (with a gentle plan for age 65+ or health conditions, and options for
food allergies and diets), PDF and CSV report downloads, and model performance and data tabs.

| Model | Test accuracy | Required |
|---|---|---|
| Logistic Regression | 80.5% | 78% |
| K-Nearest Neighbours | 80.5% | 76% |
| Random Forest | 80.5% | 79% |
| Decision Tree | 76.6% | 75% |

## Files
- `app.py` – the Streamlit app
- `content.py` – English and Bahasa Melayu text, tips, weekly plans and health notes
- `report.py` – builds the PDF report
- `train.py` – loads the data, cleans it, tunes and tests the models (run `python train.py`)
- `metrics.json` – test results and best settings from tuning; the app rebuilds the tuned models
  from it in a few seconds on first start
- `diabetes.csv` – Pima Indians Diabetes dataset (768 patients)
- `requirements.txt` – libraries for Streamlit Cloud

## Run on your laptop
```
pip install -r requirements.txt
streamlit run app.py
```

## Deploy (Streamlit Community Cloud)
1. Create a free GitHub account, then a new public repository (e.g. `diabetes-risk-app`).
2. Click **Add file → Upload files**, drag in all the files listed above, and **Commit**.
3. Go to share.streamlit.io, **Continue with GitHub**, then **Create app → Deploy a public app from GitHub**.
4. Pick your repository, branch `main`, main file `app.py`.
   Under **Advanced settings**, choose Python **3.13**. Click **Deploy**.
5. Wait 2–5 minutes, open the app, test it, and copy the link.
