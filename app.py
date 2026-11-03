"""Diabetes Risk Assessment - Streamlit app (RCAI classroom project).

Run locally:  streamlit run app.py
Files: content.py (English / Bahasa Melayu text, tips and weekly plans), report.py (PDF report),
train.py (data cleaning, model training and tuning).
"""
import json
import os

import altair as alt
import joblib
import numpy as np
import pandas as pd
import streamlit as st
from sklearn.metrics import auc, confusion_matrix, roc_curve

from content import (CONDITION_OPTIONS, DIET_OPTIONS, GENTLE_CONDITIONS, LANGS, TIPS, label, t,
                     weekly_plan)
from report import make_pdf, malaysia_now

st.set_page_config(page_title="Diabetes Risk Assessment", page_icon="🩺", layout="wide")

FEATURES = ["Pregnancies", "Glucose", "BloodPressure", "SkinThickness", "Insulin",
            "BMI", "DiabetesPedigreeFunction", "Age"]
COLUMNS = FEATURES + ["Outcome"]
ZERO_MEANS_MISSING = ["Glucose", "BloodPressure", "SkinThickness", "Insulin", "BMI"]
# Family history choices mapped to typical Diabetes Pedigree Function values
FAMILY_HISTORY = {
    "No known family history": 0.25,
    "One parent or sibling with diabetes": 0.55,
    "Several close relatives with diabetes": 0.90,
}
MMOL = 18.0  # 1 mmol/L of glucose = 18 mg/dL
SS = st.session_state


# ---------------------------------------------------------------- data and models
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
    clean = df.copy()
    clean[ZERO_MEANS_MISSING] = clean[ZERO_MEANS_MISSING].replace(0, np.nan)
    return df, clean


@st.cache_resource
def test_set_results():
    """Probabilities, ROC curves and confusion matrices of each model on the 20% test set."""
    from train import load_split
    _, X_test, _, y_test = load_split()
    out = {}
    for name, model in models.items():
        p = model.predict_proba(X_test)[:, 1]
        fpr, tpr, _ = roc_curve(y_test, p)
        out[name] = {"fpr": fpr, "tpr": tpr, "auc": auc(fpr, tpr),
                     "cm": confusion_matrix(y_test, (p >= 0.5).astype(int))}
    return out


models, metrics = load_models_and_metrics()
data, clean = load_data()
best_model = max(metrics, key=lambda m: metrics[m]["cv10_accuracy"])
BASELINE = clean[FEATURES].median()  # a "typical woman" in the data, used to explain results


def risk_band(p):
    if p < 0.30:
        return "Low", "🟢"
    if p < 0.60:
        return "Moderate", "🟡"
    return "High", "🔴"


def predict(model_name, values):
    return float(models[model_name].predict_proba(pd.DataFrame([values], columns=FEATURES))[0, 1])


def explain(model_name, values, given):
    """How much each given input moves the probability, compared with the median woman."""
    base = predict(model_name, values)
    effects = {}
    for f in given:
        swapped = dict(values)
        swapped[f] = BASELINE[f]
        effects[f] = (base - predict(model_name, swapped)) * 100
    return pd.Series(effects).sort_values()


def plain(text):
    # Field names for the report, without "(optional)"
    return text.replace(" (optional)", "").replace(" (pilihan)", "")


def reset_result():
    # Switching body-size or glucose unit changes the inputs, so ask for a fresh check.
    if SS.get("checked"):
        SS.checked = False
        SS.changed = True


# ---------------------------------------------------------------- header
head_l, head_r = st.columns([4, 1.3])
with head_r:
    lang = st.radio("Language / Bahasa", list(LANGS), format_func=LANGS.get, horizontal=True,
                    key="lang", label_visibility="collapsed")
with head_l:
    st.title("🩺 " + t("title", lang))
st.caption(t("subtitle", lang))

tab_check, tab_models, tab_data, tab_about = st.tabs(
    [t("tab_check", lang), t("tab_models", lang), t("tab_data", lang), t("tab_about", lang)])

# ---------------------------------------------------------------- risk check
with tab_check:
    left, right = st.columns([1, 1.2], gap="large")

    with left:
        st.subheader(t("your_details", lang))
        st.info(t("women_only", lang))
        c_unit, c_body = st.columns(2)
        g_unit = c_unit.radio(t("glucose_unit", lang), ["mmol/L", "mg/dL"], horizontal=True,
                              key="g_unit", on_change=reset_result)
        bmi_mode = c_body.radio(t("body_size", lang), ["Height and weight", "I know my BMI"],
                                format_func=lambda k: label(k, lang), horizontal=True,
                                key="bmi_mode", on_change=reset_result)
        errors = []

        def num(key, lo, hi, value, step=1, help=None, optional=False, unit="", text=None):
            """Number box that records an error if the value is outside a realistic range."""
            name = text or t(key, lang)
            v = st.number_input(name, value=value, step=step, help=help, key=f"in_{key}",
                                placeholder=t("not_known", lang) if optional else None)
            if v is not None and not lo <= v <= hi:
                errors.append(t("range_err", lang, label=name, lo=lo, hi=hi, unit=unit, v=v))
            return v

        with st.form("inputs"):
            age = num("age", 21, 100, 35, help=t("age_help", lang), unit=" " + (
                "years" if lang == "en" else "tahun"))
            pregnancies = num("pregnancies", 0, 17, 0)
            if g_unit == "mmol/L":
                g_in = num("glucose_mmol", 2.2, 22.2, 6.1, step=0.1, unit=" mmol/L",
                           help=t("glucose_help", lang))
                glucose = round(g_in * MMOL) if g_in is not None else 0
            else:
                g_in = num("glucose_mgdl", 40, 400, 110, unit=" mg/dL",
                           help=t("glucose_help", lang))
                glucose = g_in
            bp = num("bp", 40, 130, 75, unit=" mmHg", help=t("bp_help", lang))

            w = None
            if bmi_mode == "Height and weight":
                h = num("height", 120.0, 220.0, 160.0, step=0.1, unit=" cm")
                w = num("weight", 30.0, 250.0, 60.0, step=0.1, unit=" kg")
                bmi = round(w / (h / 100) ** 2, 1) if h and w else 0.0
                if bmi and not 15 <= bmi <= 70:
                    errors.append(t("bmi_err", lang, bmi=bmi))
            else:
                bmi = num("bmi", 15.0, 70.0, 24.0, step=0.1, unit=" kg/m²")

            family = st.selectbox(t("family", lang), list(FAMILY_HISTORY), key="in_family",
                                  format_func=lambda k: label(k, lang))
            diet = st.multiselect(t("diet", lang), DIET_OPTIONS, key="in_diet",
                                  format_func=lambda k: label(k, lang),
                                  placeholder=t("none", lang), help=t("diet_help", lang))
            conditions = st.multiselect(t("conditions", lang), CONDITION_OPTIONS,
                                        key="in_conditions", format_func=lambda k: label(k, lang),
                                        placeholder=t("none", lang),
                                        help=t("conditions_help", lang))

            with st.expander(t("optional_lab", lang)):
                st.caption(t("optional_lab_note", lang))
                skin = num("skin", 5, 100, None, optional=True, unit=" mm")
                insulin = num("insulin", 10, 900, None, optional=True, unit=" μU/mL")

            model_name = st.selectbox(t("model", lang), list(models), key="in_model",
                                      index=list(models).index(best_model),
                                      help=t("model_help", lang, m=best_model))
            submitted = st.form_submit_button(t("check", lang), type="primary", width="stretch")

    if submitted:
        SS.checked = True
        SS.changed = False
        SS.rid = SS.get("rid", 0) + 1  # new result: reset the what-if sliders

    with right:
        st.subheader(t("your_result", lang))
        if not SS.get("checked"):
            st.info(t("recheck" if SS.get("changed") else "fill_in", lang))
        elif errors:
            st.error(t("fix_errors", lang))
            for e in errors:
                st.markdown(f"- {e}")
        else:
            mmol = g_unit == "mmol/L"
            if bmi_mode == "Height and weight":
                st.caption(t("bmi_from_hw", lang, bmi=bmi))
            if mmol:
                st.caption(t("glucose_conv", lang, mmol=g_in, mgdl=glucose))
            values = {"Pregnancies": pregnancies, "Glucose": glucose, "BloodPressure": bp,
                      "SkinThickness": np.nan if skin is None else skin,
                      "Insulin": np.nan if insulin is None else insulin,
                      "BMI": bmi, "DiabetesPedigreeFunction": FAMILY_HISTORY[family], "Age": age}
            prob = predict(model_name, values)
            band, icon = risk_band(prob)

            # Clinical override: a 2-hour glucose of 200 mg/dL (11.1 mmol/L) or more is in the
            # diagnostic range for diabetes, and the training data stops at 199.
            override = glucose >= 200
            g200 = "11.1 mmol/L" if mmol else "200 mg/dL"
            g_pre = ("7.8", "11.0 mmol/L") if mmol else ("140", "199 mg/dL")
            warning = ""
            if override:
                band, icon = "High", "🔴"
                warning = t("diabetic_range", lang, g=g200).replace("**", "")
                st.error(t("diabetic_range", lang, g=g200))
            elif glucose >= 140:
                warning = t("prediabetic_range", lang, lo=g_pre[0], hi=g_pre[1])
                st.warning(warning)

            st.metric(t("est_risk", lang), f"{icon} {label(band, lang)}")
            st.caption(t("prob_line", lang, p=f"{prob:.0%}", m=model_name))
            mm = metrics[model_name]
            st.caption(t("model_scores", lang, m=model_name, a=f"{mm['accuracy']:.1%}",
                         pr=f"{mm['precision']:.1%}", r=f"{mm['recall']:.1%}"))
            st.progress(min(max(prob, 0.0), 1.0))

            # --- why this result
            given = [f for f in FEATURES
                     if not (f == "SkinThickness" and skin is None)
                     and not (f == "Insulin" and insulin is None)]
            eff = explain(model_name, values, given)
            factor_lines = []
            with st.expander(t("why_title", lang), expanded=True):
                st.caption(t("why_intro", lang))
                chart_df = pd.DataFrame({
                    t("factor", lang): [label(f, lang) for f in eff.index],
                    t("effect", lang): eff.values.round(1),
                    "dir": np.where(eff.values >= 0, "up", "down")})
                chart = alt.Chart(chart_df).mark_bar().encode(
                    x=alt.X(f"{t('effect', lang)}:Q"),
                    y=alt.Y(f"{t('factor', lang)}:N", sort=None, title=None),
                    color=alt.Color("dir:N", scale=alt.Scale(domain=["up", "down"],
                                                             range=["#d64545", "#2e9e5b"]),
                                    legend=None),
                    tooltip=[t("factor", lang), t("effect", lang)])
                st.altair_chart(chart, width="stretch")
                top_up, top_down = eff.idxmax(), eff.idxmin()
                if eff[top_up] >= 1:
                    line = t("why_up", lang, f=label(top_up, lang), d=f"{eff[top_up]:.0f}")
                    st.markdown(line)
                    factor_lines.append(line.replace("**", ""))
                if eff[top_down] <= -1:
                    line = t("why_down", lang, f=label(top_down, lang), d=f"{eff[top_down]:.0f}")
                    st.markdown(line)
                    factor_lines.append(line.replace("**", ""))

            # --- what if
            rid = SS.get("rid", 0)
            with st.expander(t("whatif_title", lang)):
                st.caption(t("whatif_intro", lang))
                if mmol:
                    wg = st.slider(t("glucose_mmol", lang), 2.2, 11.0, float(min(g_in, 11.0)), 0.1,
                                   key=f"wi_g_{rid}")
                    wg_mg = round(wg * MMOL)
                else:
                    wg_mg = st.slider(t("glucose_mgdl", lang), 40, 199, int(min(glucose, 199)),
                                      key=f"wi_g_{rid}")
                wb = st.slider("BMI", 15.0, 70.0, float(bmi), 0.1, key=f"wi_b_{rid}")
                wbp = st.slider(t("bp", lang), 40, 130, int(bp), key=f"wi_bp_{rid}")
                new = predict(model_name, {**values, "Glucose": wg_mg, "BMI": wb,
                                           "BloodPressure": wbp})
                diff = (new - prob) * 100
                st.markdown(t("whatif_result", lang, band=label(risk_band(new)[0], lang),
                              p=f"{new:.0%}", diff=f"{diff:+.0f}"))

            st.markdown(f"**{t('all_models', lang)}**")
            comp = pd.DataFrame({
                t("col_model", lang): list(models),
                t("col_prob", lang): [predict(m, values) for m in models],
                t("col_acc", lang): [metrics[m]["accuracy"] for m in models],
            })
            comp[t("col_risk", lang)] = comp[t("col_prob", lang)].map(
                lambda p: label(risk_band(p)[0], lang))
            st.dataframe(comp.style.format({t("col_prob", lang): "{:.0%}",
                                            t("col_acc", lang): "{:.1%}"}),
                         hide_index=True, width="stretch")

            st.markdown(f"**{t('what_you_can_do', lang)}**")
            for tip in TIPS[lang][band]:
                st.markdown(f"- {tip}")

            gentle = age >= 65 or bool(GENTLE_CONDITIONS & set(conditions))
            plan = weekly_plan(band, bmi, glucose, w, gentle=gentle, diet=diet,
                               conditions=conditions, lang=lang)
            st.markdown(f"**{t('weekly_plan', lang)}**")
            p_ex, p_food = st.tabs([t("exercise", lang), t("food_guide", lang)])
            with p_ex:
                st.dataframe(pd.DataFrame(plan[0], columns=[t("day", lang), t("exercise", lang)]),
                             hide_index=True, width="stretch")
            with p_food:
                for item in plan[1]:
                    st.markdown(f"- {item}")
            st.caption(plan[2])
            if plan[3]:
                st.warning(f"**{t('health_notes', lang)}**\n\n"
                           + "\n".join(f"- {n}" for n in plan[3]))

            glucose_txt = f"{g_in} mmol/L ({glucose} mg/dL)" if mmol else f"{glucose} mg/dL"
            none = t("none", lang)
            rows = [
                (t("age", lang), age), (t("pregnancies", lang), pregnancies),
                (t("f_glucose", lang), glucose_txt), (t("f_bp", lang), bp), ("BMI", bmi),
                (t("family", lang), label(family, lang)),
                (t("f_skin", lang), t("not_given", lang) if skin is None else skin),
                (t("f_insulin", lang), t("not_given", lang) if insulin is None else insulin),
                (plain(t("conditions", lang)), ", ".join(label(c, lang) for c in conditions) or none),
                (plain(t("diet", lang)), ", ".join(label(d, lang) for d in diet) or none),
            ]
            level = label(band, lang) + (t("in_diabetic_range", lang) if override else "")
            report = pd.DataFrame(
                [(t("f_date", lang), malaysia_now())] + rows
                + [(t("model", lang), model_name), (t("f_prob", lang), f"{prob:.0%}"),
                   (t("f_level", lang), level)],
                columns=[t("rep_measure", lang), t("rep_value", lang)])

            st.markdown(f"**{t('download', lang)}**")
            d1, d2 = st.columns(2)
            d1.download_button(t("dl_pdf", lang),
                               make_pdf(rows, band, prob, model_name, TIPS[lang][band], warning,
                                        plan, factor_lines, lang),
                               file_name="diabetes_risk_report.pdf", mime="application/pdf",
                               width="stretch", on_click="ignore")
            d2.download_button(t("dl_csv", lang), report.to_csv(index=False).encode("utf-8-sig"),
                               file_name="diabetes_risk_report.csv", mime="text/csv",
                               width="stretch", on_click="ignore")

    st.caption(t("disclaimer", lang))

# ---------------------------------------------------------------- model performance
with tab_models:
    st.subheader(t("perf_title", lang))
    st.write(t("perf_intro", lang))
    res = test_set_results()
    table = pd.DataFrame([{
        t("col_model", lang): name,
        t("col_acc", lang): m["accuracy"],
        t("col_required", lang): m["target"],
        t("col_precision", lang): m["precision"],
        t("col_recall", lang): m["recall"],
        "F1": m["f1"],
        "AUC": res[name]["auc"],
        t("col_cv", lang): m["cv10_accuracy"],
        t("col_settings", lang): ", ".join(f"{k}={v}" for k, v in m["best_params"].items()),
    } for name, m in metrics.items()])
    pct = {c: "{:.1%}" for c in [t("col_acc", lang), t("col_required", lang),
                                 t("col_precision", lang), t("col_recall", lang), "F1",
                                 t("col_cv", lang)]}
    st.dataframe(table.style.format({**pct, "AUC": "{:.2f}"}), hide_index=True, width="stretch")
    st.bar_chart(table.set_index(t("col_model", lang))[[t("col_acc", lang),
                                                        t("col_required", lang)]])
    st.markdown(t("why_default", lang, m=best_model))
    st.markdown(t("preproc", lang))

    c_roc, c_cm = st.columns(2, gap="large")
    with c_roc:
        st.markdown(f"**{t('roc_title', lang)}**")
        roc_df = pd.concat([pd.DataFrame({"fpr": r["fpr"], "tpr": r["tpr"],
                                          "model": f"{n} (AUC {r['auc']:.2f})"})
                            for n, r in res.items()])
        lines = alt.Chart(roc_df).mark_line().encode(
            x=alt.X("fpr:Q", title=t("fpr", lang)), y=alt.Y("tpr:Q", title=t("tpr", lang)),
            color=alt.Color("model:N", title=None,
                            legend=alt.Legend(orient="bottom", columns=1, labelLimit=0)))
        diag = alt.Chart(pd.DataFrame({"fpr": [0, 1], "tpr": [0, 1]})).mark_line(
            strokeDash=[4, 4], color="grey").encode(x="fpr:Q", y="tpr:Q")
        st.altair_chart(lines + diag, width="stretch")
        st.caption(t("roc_note", lang))
    with c_cm:
        st.markdown(f"**{t('cm_title', lang)}**")
        cm_model = st.selectbox(t("cm_model", lang), list(models), key="cm_model",
                                index=list(models).index(best_model))
        cm = res[cm_model]["cm"]
        names = [label("Not diabetic", lang), label("Diabetic", lang)]
        cm_df = pd.DataFrame([(names[i], names[j], int(cm[i, j])) for i in range(2)
                              for j in range(2)],
                             columns=[t("actual", lang), t("predicted", lang), t("count", lang)])
        base = alt.Chart(cm_df).encode(x=alt.X(f"{t('predicted', lang)}:N", sort=names),
                                       y=alt.Y(f"{t('actual', lang)}:N", sort=names))
        heat = base.mark_rect().encode(color=alt.Color(f"{t('count', lang)}:Q", legend=None,
                                                       scale=alt.Scale(scheme="blues")))
        text = base.mark_text(fontSize=18).encode(text=f"{t('count', lang)}:Q")
        st.altair_chart((heat + text).properties(height=240), width="stretch")
        st.caption(t("cm_note", lang))

    st.markdown(f"**{t('fi_title', lang)}**")
    rf = models["Random Forest"].named_steps["model"]
    fi = pd.DataFrame({t("factor", lang): [label(f, lang) for f in FEATURES],
                       t("importance", lang): rf.feature_importances_})
    st.altair_chart(alt.Chart(fi).mark_bar(color="#4c78a8").encode(
        x=f"{t('importance', lang)}:Q",
        y=alt.Y(f"{t('factor', lang)}:N", sort="-x", title=None)), width="stretch")

# ---------------------------------------------------------------- data insights
with tab_data:
    st.subheader(t("data_title", lang))
    c1, c2, c3 = st.columns(3)
    c1.metric(t("patients", lang), len(data))
    c2.metric(t("diabetic", lang), f"{data['Outcome'].mean():.0%}")
    c3.metric(t("avg_age", lang), f"{data['Age'].mean():.0f}")

    st.markdown(f"**{t('missing_title', lang)}**")
    miss = clean[ZERO_MEANS_MISSING].isna().mean()
    miss.index = [label(c, lang) for c in miss.index]
    st.bar_chart(miss.rename(t("share_missing", lang)))

    st.markdown(f"**{t('avg_title', lang)}**")
    avg = clean.groupby("Outcome")[["Glucose", "BloodPressure", "BMI", "Age"]].mean()
    avg.index = [label("Not diabetic", lang), label("Diabetic", lang)]
    avg.columns = [label(c, lang) for c in avg.columns]
    st.dataframe(avg.round(1), width="stretch")

    feature = st.selectbox(t("compare", lang), ["Glucose", "BMI", "Age", "BloodPressure"],
                           format_func=lambda k: label(k, lang), key="compare")
    bins = pd.cut(clean[feature], 10)
    dist = clean.groupby([bins, "Outcome"], observed=True).size().unstack(fill_value=0)
    dist.columns = [label("Not diabetic", lang), label("Diabetic", lang)]
    dist.index = dist.index.astype(str)
    st.bar_chart(dist)

# ---------------------------------------------------------------- about
with tab_about:
    st.subheader(t("about_title", lang))
    st.markdown(t("about_body", lang))
