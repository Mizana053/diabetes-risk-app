# Diabetes Risk Assessment (RCAI classroom project)

A Streamlit web app that estimates diabetes risk from glucose, blood pressure, BMI, age,
pregnancies, family history and (if known) skin thickness and insulin, using four tuned scikit-learn models.

| Model | Test accuracy | Required |
|---|---|---|
| Logistic Regression | 80.5% | 78% |
| K-Nearest Neighbours | 80.5% | 76% |
| Random Forest | 80.5% | 79% |
| Decision Tree | 76.6% | 75% |

## Files
- `app.py` – the Streamlit app
- `train.py` – loads the data, cleans it, tunes and tests the models (run `python train.py`)
- On first start the app trains the four models from `diabetes.csv` (about a minute), then caches them.
  Running `python train.py` locally also saves `models.joblib` and `metrics.json`, which the app uses if present.
- `diabetes.csv` – Pima Indians Diabetes dataset (768 patients)
- `requirements.txt` – libraries for Streamlit Cloud

## Run on your laptop
```
pip install -r requirements.txt
streamlit run app.py
```

## Deploy (Streamlit Community Cloud)
1. Create a free GitHub account, then a new public repository (e.g. `diabetes-risk-app`).
2. Click **Add file → Upload files**, drag in `app.py`, `train.py`, `diabetes.csv`, `requirements.txt` and `README.md`, and **Commit**.
3. Go to share.streamlit.io, **Continue with GitHub**, then **Create app → Deploy a public app from GitHub**.
4. Pick your repository, branch `main`, main file `app.py`.
   Under **Advanced settings**, choose Python **3.13**. Click **Deploy**.
5. Wait 2–5 minutes, open the app, test it, and copy the link.
