"""Text content for the app in English and Bahasa Melayu: labels, tips, weekly plans and notes.

Internal option keys stay in English; only what the user sees is translated.
"""

LANGS = {"en": "English", "ms": "Bahasa Melayu"}

# ---------------------------------------------------------------- interface text
UI = {
    "title": {"en": "Diabetes Risk Assessment", "ms": "Penilaian Risiko Diabetes"},
    "subtitle": {
        "en": "An AI risk-screening tool for women aged 21+, trained on the Pima Indians Diabetes "
              "dataset (768 women). It estimates risk only and is not a medical diagnosis.",
        "ms": "Alat saringan risiko berasaskan AI untuk wanita berumur 21 tahun ke atas, dilatih "
              "dengan set data Pima Indians Diabetes (768 wanita). Ia hanya menganggar risiko dan "
              "bukan diagnosis perubatan."},
    "tab_check": {"en": "Risk check", "ms": "Semakan risiko"},
    "tab_models": {"en": "Model performance", "ms": "Prestasi model"},
    "tab_data": {"en": "Data insights", "ms": "Analisis data"},
    "tab_about": {"en": "About", "ms": "Tentang"},
    "your_details": {"en": "Your details", "ms": "Maklumat anda"},
    "women_only": {"en": "This tool is for **women aged 21 and over**, the group the models were "
                         "trained on.",
                   "ms": "Alat ini untuk **wanita berumur 21 tahun ke atas**, iaitu kumpulan yang "
                         "digunakan untuk melatih model."},
    "body_size": {"en": "Body size", "ms": "Saiz badan"},
    "glucose_unit": {"en": "Glucose unit", "ms": "Unit glukosa"},
    "age": {"en": "Age (years)", "ms": "Umur (tahun)"},
    "age_help": {"en": "The model was trained on adults aged 21 and over.",
                 "ms": "Model dilatih dengan orang dewasa berumur 21 tahun ke atas."},
    "pregnancies": {"en": "Number of pregnancies (0 if none)",
                    "ms": "Bilangan kehamilan (0 jika tiada)"},
    "glucose_mgdl": {"en": "Blood glucose (mg/dL)", "ms": "Glukosa darah (mg/dL)"},
    "glucose_mmol": {"en": "Blood glucose (mmol/L)", "ms": "Glukosa darah (mmol/L)"},
    "glucose_help": {"en": "2-hour glucose from an oral glucose tolerance test (OGTT). Malaysian "
                           "clinics and glucometers usually report mmol/L.",
                     "ms": "Glukosa 2 jam daripada ujian toleransi glukosa oral (OGTT). Klinik "
                           "dan glukometer di Malaysia biasanya menggunakan mmol/L."},
    "bp": {"en": "Diastolic blood pressure (mmHg) - the lower number",
           "ms": "Tekanan darah diastolik (mmHg) - nombor bawah"},
    "bp_help": {"en": "For a reading of 120/80, enter 80.",
                "ms": "Untuk bacaan 120/80, masukkan 80."},
    "height": {"en": "Height (cm)", "ms": "Tinggi (cm)"},
    "weight": {"en": "Weight (kg)", "ms": "Berat (kg)"},
    "bmi": {"en": "BMI (kg/m²)", "ms": "BMI (kg/m²)"},
    "family": {"en": "Family history of diabetes", "ms": "Sejarah keluarga menghidap diabetes"},
    "diet": {"en": "Food allergies or diet (optional)", "ms": "Alahan makanan atau diet (pilihan)"},
    "diet_help": {"en": "The food guide will avoid these foods.",
                  "ms": "Panduan makanan akan mengelakkan makanan ini."},
    "conditions": {"en": "Other health conditions (optional)",
                   "ms": "Masalah kesihatan lain (pilihan)"},
    "conditions_help": {"en": "Adjusts the exercise plan and adds safety notes. A gentle plan is "
                              "used automatically from age 65.",
                        "ms": "Menyesuaikan pelan senaman dan menambah nota keselamatan. Pelan "
                              "ringan digunakan secara automatik dari umur 65 tahun."},
    "none": {"en": "None", "ms": "Tiada"},
    "optional_lab": {"en": "Optional: skin thickness and insulin (if known)",
                     "ms": "Pilihan: ketebalan kulit dan insulin (jika diketahui)"},
    "optional_lab_note": {"en": "Leave blank if you don't know them. Missing values are filled in "
                                "from the most similar patients in the training data.",
                          "ms": "Biarkan kosong jika tidak tahu. Nilai yang tiada akan diisi "
                                "berdasarkan pesakit yang paling serupa dalam data latihan."},
    "skin": {"en": "Triceps skin fold thickness (mm)", "ms": "Ketebalan lipatan kulit trisep (mm)"},
    "insulin": {"en": "2-hour serum insulin (μU/mL)", "ms": "Insulin serum 2 jam (μU/mL)"},
    "not_known": {"en": "Not known", "ms": "Tidak diketahui"},
    "model": {"en": "Prediction model", "ms": "Model ramalan"},
    "model_help": {"en": "Default: {m}, which had the best 10-fold cross-validation accuracy.",
                   "ms": "Lalai: {m}, yang mempunyai ketepatan pengesahan silang 10 lipatan "
                         "terbaik."},
    "check": {"en": "Check my risk", "ms": "Semak risiko saya"},
    "your_result": {"en": "Your result", "ms": "Keputusan anda"},
    "fill_in": {"en": "Fill in your details and press **Check my risk**.",
                "ms": "Isi maklumat anda dan tekan **Semak risiko saya**."},
    "recheck": {"en": "You changed a setting. Press **Check my risk** again to update your result.",
                "ms": "Anda telah menukar tetapan. Tekan **Semak risiko saya** sekali lagi untuk "
                      "mengemas kini keputusan."},
    "fix_errors": {"en": "Please correct these values first. They are outside realistic medical "
                         "ranges:",
                   "ms": "Sila betulkan nilai ini dahulu. Nilai ini di luar julat perubatan yang "
                         "munasabah:"},
    "range_err": {"en": "**{label}** must be between {lo} and {hi}{unit} (you entered {v:g}).",
                  "ms": "**{label}** mesti antara {lo} dan {hi}{unit} (anda masukkan {v:g})."},
    "bmi_err": {"en": "Your height and weight give a BMI of {bmi}, which is outside 15-70.",
                "ms": "Tinggi dan berat anda memberi BMI {bmi}, iaitu di luar julat 15-70."},
    "bmi_from_hw": {"en": "Your BMI from height and weight: **{bmi}**",
                    "ms": "BMI anda daripada tinggi dan berat: **{bmi}**"},
    "glucose_conv": {"en": "Glucose {mmol} mmol/L = {mgdl} mg/dL (the unit the model uses).",
                     "ms": "Glukosa {mmol} mmol/L = {mgdl} mg/dL (unit yang digunakan model)."},
    "diabetic_range": {
        "en": "Your glucose is **{g}** or higher, which is in the diabetic range on a glucose "
              "tolerance test. Please see a doctor.",
        "ms": "Glukosa anda **{g}** atau lebih, iaitu dalam julat diabetes bagi ujian toleransi "
              "glukosa. Sila jumpa doktor."},
    "prediabetic_range": {"en": "A 2-hour glucose of {lo}-{hi} is in the pre-diabetes range.",
                          "ms": "Glukosa 2 jam {lo}-{hi} berada dalam julat pra-diabetes."},
    "est_risk": {"en": "Estimated risk", "ms": "Anggaran risiko"},
    "prob_line": {"en": "{p} probability of diabetes ({m})",
                  "ms": "Kebarangkalian diabetes {p} ({m})"},
    "model_scores": {"en": "{m} on the 154-patient test set: accuracy {a}, precision {pr}, "
                           "recall {r}.",
                     "ms": "{m} pada set ujian 154 pesakit: ketepatan {a}, kejituan {pr}, "
                           "dapatan semula {r}."},
    "why_title": {"en": "Why this result?", "ms": "Mengapa keputusan ini?"},
    "why_intro": {"en": "How each of your values moved the risk, compared with a typical woman in "
                        "the data (median: glucose {g}, BMI {bmi}, age {age}). Red raised your "
                        "risk, green lowered it.",
                  "ms": "Bagaimana setiap nilai anda mengubah risiko, berbanding wanita biasa "
                        "dalam data (median: glukosa {g}, BMI {bmi}, umur {age}). Merah menaikkan "
                        "risiko, hijau menurunkannya."},
    "why_up": {"en": "**{f}** raised your risk the most (+{d} points).",
               "ms": "**{f}** paling banyak menaikkan risiko anda (+{d} mata)."},
    "why_down": {"en": "**{f}** lowered your risk the most ({d} points).",
                 "ms": "**{f}** paling banyak menurunkan risiko anda ({d} mata)."},
    "effect": {"en": "Effect on risk (percentage points)",
               "ms": "Kesan pada risiko (mata peratusan)"},
    "factor": {"en": "Factor", "ms": "Faktor"},
    "whatif_title": {"en": "What if? Try changing your numbers",
                     "ms": "Bagaimana jika? Cuba ubah nombor anda"},
    "whatif_intro": {"en": "Move the sliders to see how your risk could change, for example after "
                           "losing weight or improving your glucose.",
                     "ms": "Gerakkan peluncur untuk melihat bagaimana risiko anda boleh berubah, "
                           "contohnya selepas menurunkan berat badan atau memperbaiki glukosa."},
    "whatif_result": {"en": "New estimated risk: **{band}** ({p}), {diff} points compared with now.",
                      "ms": "Anggaran risiko baharu: **{band}** ({p}), {diff} mata berbanding "
                            "sekarang."},
    "all_models": {"en": "All four models", "ms": "Keempat-empat model"},
    "col_model": {"en": "Model", "ms": "Model"},
    "col_prob": {"en": "Probability", "ms": "Kebarangkalian"},
    "col_acc": {"en": "Test accuracy", "ms": "Ketepatan ujian"},
    "col_risk": {"en": "Risk", "ms": "Risiko"},
    "what_you_can_do": {"en": "What you can do", "ms": "Apa yang anda boleh lakukan"},
    "weekly_plan": {"en": "Your weekly plan", "ms": "Pelan mingguan anda"},
    "exercise": {"en": "Exercise", "ms": "Senaman"},
    "food_guide": {"en": "Food guide", "ms": "Panduan makanan"},
    "day": {"en": "Day", "ms": "Hari"},
    "health_notes": {"en": "Health notes", "ms": "Nota kesihatan"},
    "download": {"en": "Download your report", "ms": "Muat turun laporan anda"},
    "dl_pdf": {"en": "PDF (easy to open and print)", "ms": "PDF (mudah dibuka dan dicetak)"},
    "dl_csv": {"en": "CSV (for Excel)", "ms": "CSV (untuk Excel)"},
    "disclaimer": {"en": "⚠️ This tool is for education and screening only. It does not replace a "
                         "blood test or a doctor's advice.",
                   "ms": "⚠️ Alat ini untuk pendidikan dan saringan sahaja. Ia tidak menggantikan "
                         "ujian darah atau nasihat doktor."},
    # model performance tab
    "perf_title": {"en": "How the models performed", "ms": "Prestasi model"},
    "perf_intro": {
        "en": "Each model was tuned with 5-fold cross-validation (GridSearchCV) on 80% of the data "
              "and tested on the remaining 20% (154 patients). Because one 20% test set can be "
              "lucky or unlucky, the 10-fold cross-validation accuracy on all 768 patients is "
              "shown too.",
        "ms": "Setiap model ditala dengan pengesahan silang 5 lipatan (GridSearchCV) pada 80% "
              "data dan diuji pada baki 20% (154 pesakit). Oleh kerana satu set ujian 20% boleh "
              "bernasib baik atau tidak, ketepatan pengesahan silang 10 lipatan pada kesemua 768 "
              "pesakit turut ditunjukkan."},
    "col_required": {"en": "Required", "ms": "Sasaran"},
    "col_precision": {"en": "Precision", "ms": "Kejituan"},
    "col_recall": {"en": "Recall", "ms": "Dapatan semula"},
    "col_cv": {"en": "10-fold CV accuracy", "ms": "Ketepatan CV 10 lipatan"},
    "col_settings": {"en": "Best settings", "ms": "Tetapan terbaik"},
    "why_default": {"en": "**Why {m} is the default:** it has the highest 10-fold cross-validation "
                          "accuracy, which is the most reliable measure on a dataset this small.",
                    "ms": "**Mengapa {m} dipilih sebagai lalai:** ia mempunyai ketepatan "
                          "pengesahan silang 10 lipatan tertinggi, ukuran paling boleh dipercayai "
                          "untuk set data sekecil ini."},
    "preproc": {
        "en": "**Pre-processing**\n- In this dataset a 0 for glucose, blood pressure, skin "
              "thickness, insulin or BMI means \"not recorded\", so those zeros were turned into "
              "missing values.\n- Missing values (common for skin thickness, 30%, and insulin, "
              "49%) were filled in from the 5 most similar patients (KNN imputation), and all "
              "eight features were scaled.",
        "ms": "**Pra-pemprosesan**\n- Dalam set data ini, nilai 0 bagi glukosa, tekanan darah, "
              "ketebalan kulit, insulin atau BMI bermaksud \"tidak direkod\", jadi nilai 0 itu "
              "ditukar kepada nilai hilang.\n- Nilai hilang (kerap bagi ketebalan kulit, 30%, dan "
              "insulin, 49%) diisi berdasarkan 5 pesakit paling serupa (imputasi KNN), dan "
              "kesemua lapan ciri diskalakan."},
    "roc_title": {"en": "ROC curves (test set)", "ms": "Lengkung ROC (set ujian)"},
    "roc_note": {"en": "The further a curve bends towards the top-left, the better the model "
                       "separates diabetic from non-diabetic patients. AUC 1.0 is perfect; 0.5 "
                       "is guessing.",
                 "ms": "Semakin lengkung melengkung ke kiri atas, semakin baik model membezakan "
                       "pesakit diabetes daripada bukan diabetes. AUC 1.0 adalah sempurna; 0.5 "
                       "sama seperti meneka."},
    "fpr": {"en": "False positive rate", "ms": "Kadar positif palsu"},
    "tpr": {"en": "True positive rate (recall)", "ms": "Kadar positif benar (dapatan semula)"},
    "cm_title": {"en": "Confusion matrix (test set)", "ms": "Matriks kekeliruan (set ujian)"},
    "cm_model": {"en": "Show model", "ms": "Tunjuk model"},
    "cm_note": {"en": "Diagonal boxes are correct predictions. \"Missed\" diabetic patients "
                      "(bottom-left) matter most in screening.",
                "ms": "Kotak pepenjuru ialah ramalan yang betul. Pesakit diabetes yang "
                      "\"terlepas\" (kiri bawah) paling penting dalam saringan."},
    "actual": {"en": "Actual", "ms": "Sebenar"},
    "predicted": {"en": "Predicted", "ms": "Ramalan"},
    "count": {"en": "Patients", "ms": "Pesakit"},
    "fi_title": {"en": "Which factors matter most (Random Forest)",
                 "ms": "Faktor yang paling penting (Random Forest)"},
    "importance": {"en": "Importance", "ms": "Kepentingan"},
    # data tab
    "data_title": {"en": "About the training data", "ms": "Tentang data latihan"},
    "patients": {"en": "Patients", "ms": "Pesakit"},
    "diabetic": {"en": "Diabetic", "ms": "Menghidap diabetes"},
    "not_diabetic": {"en": "Not diabetic", "ms": "Bukan diabetes"},
    "avg_age": {"en": "Average age", "ms": "Purata umur"},
    "missing_title": {"en": "Missing values (recorded as 0 in the raw data)",
                      "ms": "Nilai hilang (direkod sebagai 0 dalam data mentah)"},
    "share_missing": {"en": "Share missing", "ms": "Peratus hilang"},
    "avg_title": {"en": "Average values: diabetic vs not diabetic",
                  "ms": "Nilai purata: diabetes berbanding bukan diabetes"},
    "compare": {"en": "Compare a measure", "ms": "Bandingkan satu ukuran"},
    # about tab
    "about_title": {"en": "About this project", "ms": "Tentang projek ini"},
    "about_body": {
        "en": "Built for the **Rocheston Certified AI Engineer (RCAI) classroom project**, APU "
              "Certified AI Engineer programme 2026.\n\n- **Data:** Pima Indians Diabetes dataset "
              "(National Institute of Diabetes and Digestive and Kidney Diseases), 768 adult "
              "female patients.\n- **Models:** Logistic Regression, K-Nearest Neighbours, Random "
              "Forest, Decision Tree (scikit-learn), each tuned with GridSearchCV.\n- **App:** "
              "Streamlit.\n\n**Limitations:** the data comes from one population (Pima women aged "
              "21+), so results may be less accurate for other groups. Glucose values here are "
              "2-hour oral glucose tolerance test readings. Always confirm with a proper medical "
              "test.\n\n**Privacy:** nothing you enter is saved or sent anywhere; your details are "
              "only used to calculate the result on this page.",
        "ms": "Dibina untuk **projek kelas Rocheston Certified AI Engineer (RCAI)**, program APU "
              "Certified AI Engineer 2026.\n\n- **Data:** set data Pima Indians Diabetes "
              "(National Institute of Diabetes and Digestive and Kidney Diseases), 768 pesakit "
              "wanita dewasa.\n- **Model:** Logistic Regression, K-Nearest Neighbours, Random "
              "Forest, Decision Tree (scikit-learn), setiap satu ditala dengan GridSearchCV.\n- "
              "**Aplikasi:** Streamlit.\n\n**Had:** data diperoleh daripada satu populasi (wanita "
              "Pima berumur 21 tahun ke atas), jadi keputusan mungkin kurang tepat untuk kumpulan "
              "lain. Nilai glukosa di sini ialah bacaan ujian toleransi glukosa oral 2 jam. Sentiasa "
              "sahkan dengan ujian perubatan yang betul.\n\n**Privasi:** apa yang anda masukkan "
              "tidak disimpan atau dihantar ke mana-mana; maklumat anda hanya digunakan untuk "
              "mengira keputusan di halaman ini."},
    # report
    "rep_title": {"en": "Diabetes Risk Assessment Report", "ms": "Laporan Penilaian Risiko Diabetes"},
    "rep_generated": {"en": "Generated {t}", "ms": "Dijana {t}"},
    "rep_risk": {"en": "Estimated risk: {band} ({p} probability)",
                 "ms": "Anggaran risiko: {band} (kebarangkalian {p})"},
    "rep_model": {"en": "Model used: {m}", "ms": "Model yang digunakan: {m}"},
    "rep_details": {"en": "Your details", "ms": "Maklumat anda"},
    "rep_measure": {"en": "Measurement", "ms": "Ukuran"},
    "rep_value": {"en": "Your value", "ms": "Nilai anda"},
    "rep_why": {"en": "Main factors in your result", "ms": "Faktor utama dalam keputusan anda"},
    "rep_footer": {"en": "This report is for education and screening only. It is not a medical "
                         "diagnosis and does not replace a blood test or a doctor's advice. Model "
                         "trained on the Pima Indians Diabetes dataset (women aged 21+).",
                   "ms": "Laporan ini untuk pendidikan dan saringan sahaja. Ia bukan diagnosis "
                         "perubatan dan tidak menggantikan ujian darah atau nasihat doktor. Model "
                         "dilatih dengan set data Pima Indians Diabetes (wanita berumur 21 tahun "
                         "ke atas)."},
    "f_date": {"en": "Date", "ms": "Tarikh"},
    "f_glucose": {"en": "Glucose", "ms": "Glukosa"},
    "f_bp": {"en": "Diastolic BP (mmHg)", "ms": "Tekanan darah diastolik (mmHg)"},
    "f_skin": {"en": "Skin thickness (mm)", "ms": "Ketebalan kulit (mm)"},
    "f_insulin": {"en": "Insulin (μU/mL)", "ms": "Insulin (μU/mL)"},
    "f_prob": {"en": "Probability", "ms": "Kebarangkalian"},
    "f_level": {"en": "Risk level", "ms": "Tahap risiko"},
    "not_given": {"en": "not given", "ms": "tidak diberi"},
    "in_diabetic_range": {"en": " (glucose in diabetic range)",
                          "ms": " (glukosa dalam julat diabetes)"},
}

# Display names for option keys, factor names and risk bands
LABELS = {
    "Height and weight": {"ms": "Tinggi dan berat"},
    "I know my BMI": {"ms": "Saya tahu BMI saya"},
    "No known family history": {"ms": "Tiada sejarah keluarga yang diketahui"},
    "One parent or sibling with diabetes": {"ms": "Seorang ibu/bapa atau adik-beradik menghidap "
                                                  "diabetes"},
    "Several close relatives with diabetes": {"ms": "Beberapa saudara terdekat menghidap "
                                                    "diabetes"},
    "Vegetarian": {"ms": "Vegetarian"},
    "Vegan": {"ms": "Vegan"},
    "No eggs": {"ms": "Tanpa telur"},
    "No nuts": {"ms": "Tanpa kekacang"},
    "No fish or seafood": {"ms": "Tanpa ikan atau makanan laut"},
    "No soy": {"ms": "Tanpa soya"},
    "No gluten / wheat": {"ms": "Tanpa gluten / gandum"},
    "No dairy": {"ms": "Tanpa tenusu"},
    "Joint pain / limited mobility": {"ms": "Sakit sendi / pergerakan terhad"},
    "Asthma": {"ms": "Asma"},
    "Heart condition": {"ms": "Penyakit jantung"},
    "High blood pressure": {"ms": "Darah tinggi"},
    "Pregnant": {"ms": "Hamil"},
    "Kidney disease": {"ms": "Penyakit buah pinggang"},
    "Other long-term condition": {"ms": "Penyakit jangka panjang lain"},
    "Low": {"ms": "Rendah"},
    "Moderate": {"ms": "Sederhana"},
    "High": {"ms": "Tinggi"},
    "Glucose": {"ms": "Glukosa"},
    "BloodPressure": {"en": "Blood pressure", "ms": "Tekanan darah"},
    "BMI": {"ms": "BMI"},
    "Age": {"en": "Age", "ms": "Umur"},
    "Pregnancies": {"ms": "Kehamilan"},
    "DiabetesPedigreeFunction": {"en": "Family history", "ms": "Sejarah keluarga"},
    "SkinThickness": {"en": "Skin thickness", "ms": "Ketebalan kulit"},
    "Insulin": {"ms": "Insulin"},
    "Logistic Regression": {"ms": "Logistic Regression"},
    "Not diabetic": {"ms": "Bukan diabetes"},
    "Diabetic": {"ms": "Diabetes"},
}

DAYS = {"en": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
        "ms": ["Isnin", "Selasa", "Rabu", "Khamis", "Jumaat", "Sabtu", "Ahad"]}


def t(key, lang, **kw):
    """Interface text in the chosen language, with {placeholders} filled in."""
    text = UI[key].get(lang) or UI[key]["en"]
    return text.format(**kw) if kw else text


def label(key, lang):
    """Display name of an option, factor or risk band in the chosen language."""
    entry = LABELS.get(key, {})
    return entry.get(lang) or entry.get("en") or key


# ---------------------------------------------------------------- tips
TIPS = {
    "en": {
        "Low": [
            "Keep up regular activity: at least 150 minutes of moderate exercise a week.",
            "Keep sugary drinks and refined carbohydrates (white rice, kuih, teh tarik) occasional.",
            "Re-check your blood glucose every 1-3 years, or sooner if anything changes.",
        ],
        "Moderate": [
            "Aim to lose 5-7% of body weight if your BMI is above 23 (Asian cut-off for "
            "overweight).",
            "Swap to wholegrains and fill half your plate with vegetables (the Suku-Suku Separuh "
            "plate).",
            "Be active for about 30 minutes a day, 5 days a week.",
            "Ask a clinic for a fasting glucose or HbA1c test within the next few months.",
        ],
        "High": [
            "See a doctor soon for a proper test (fasting glucose, HbA1c or OGTT).",
            "Cut sugary drinks completely and reduce portion sizes of rice and noodles.",
            "Start daily light exercise and track your weight weekly.",
            "If you have symptoms (constant thirst, frequent urination, blurred vision), seek care "
            "promptly.",
        ],
    },
    "ms": {
        "Low": [
            "Kekalkan aktiviti fizikal: sekurang-kurangnya 150 minit senaman sederhana seminggu.",
            "Hadkan minuman manis dan karbohidrat bertapis (nasi putih, kuih, teh tarik).",
            "Periksa semula glukosa darah setiap 1-3 tahun, atau lebih awal jika ada perubahan.",
        ],
        "Moderate": [
            "Sasarkan penurunan 5-7% berat badan jika BMI anda melebihi 23 (had berat berlebihan "
            "bagi orang Asia).",
            "Tukar kepada bijirin penuh dan isi separuh pinggan dengan sayur (pinggan Suku-Suku "
            "Separuh).",
            "Bergerak aktif kira-kira 30 minit sehari, 5 hari seminggu.",
            "Minta ujian glukosa berpuasa atau HbA1c di klinik dalam tempoh beberapa bulan akan datang.",
        ],
        "High": [
            "Jumpa doktor segera untuk ujian yang betul (glukosa berpuasa, HbA1c atau OGTT).",
            "Berhenti minum minuman manis dan kurangkan saiz hidangan nasi dan mi.",
            "Mula bersenam ringan setiap hari dan pantau berat badan setiap minggu.",
            "Jika ada simptom (sentiasa dahaga, kerap kencing, penglihatan kabur), dapatkan rawatan "
            "segera.",
        ],
    },
}

# ---------------------------------------------------------------- food guide
DIET_OPTIONS = ["Vegetarian", "Vegan", "No eggs", "No nuts", "No fish or seafood", "No soy",
                "No gluten / wheat", "No dairy"]

FOOD_WORDS = {
    "fish": {"ms": "ikan"}, "chicken": {"ms": "ayam"}, "tofu or tempeh": {"ms": "tauhu atau tempe"},
    "eggs": {"ms": "telur"}, "dhal or lentils": {"ms": "dhal atau kacang lentil"},
    "chickpeas": {"ms": "kacang kuda"},
    "brown rice porridge or rice thosai/idli": {"ms": "bubur beras perang atau tosai/idli beras"},
    "oats or wholemeal bread": {"ms": "oat atau roti mil penuh"},
    "an egg": {"ms": "sebiji telur"}, "tofu scramble": {"ms": "tauhu hancur goreng"},
    "peanut butter": {"ms": "mentega kacang"}, "a banana or fruit": {"ms": "pisang atau buah"},
    "guava": {"ms": "jambu batu"}, "apple": {"ms": "epal"},
    "a handful of nuts": {"ms": "segenggam kekacang"},
    "plain unsweetened yoghurt": {"ms": "yogurt kosong tanpa gula"},
    "roasted chickpeas": {"ms": "kacang kuda panggang"},
}


def fw(word, lang):
    return FOOD_WORDS.get(word, {}).get(lang, word) if lang != "en" else word


def join_or(items, lang):
    word = " atau " if lang == "ms" else " or "
    return items[0] if len(items) == 1 else ", ".join(items[:-1]) + word + items[-1]


def food_guide(diet, lang="en"):
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
    protein = ", ".join(fw(p, lang) for p in protein)

    base = fw("brown rice porridge or rice thosai/idli" if no_gluten else "oats or wholemeal bread",
              lang)
    if not no_egg:
        topping = "an egg"
    elif not no_soy:
        topping = "tofu scramble"
    elif not no_nuts:
        topping = "peanut butter"
    else:
        topping = "a banana or fruit"
    topping = fw(topping, lang)

    snacks = ["guava", "apple"]
    if not no_nuts:
        snacks.append("a handful of nuts")
    if not no_dairy:
        snacks.append("plain unsweetened yoghurt")
    snacks.append("roasted chickpeas")
    snacks = join_or([fw(s, lang) for s in snacks], lang)

    if lang == "ms":
        carbs = "nasi atau bihun/kuey teow" if no_gluten else "nasi atau mi"
        food = [
            "Gunakan Pinggan Sihat Malaysia (Suku-Suku Separuh): separuh sayur dan buah, suku "
            f"protein ({protein}), suku {carbs}.",
            "Minum air kosong; pesan teh O atau kopi O kosong / kurang manis dan bukannya teh "
            "tarik atau sirap.",
            f"Sarapan: {base} dengan {topping} dan bukannya roti canai atau nasi lemak.",
            f"Snek: {snacks} dan bukannya kuih, biskut atau makanan bergoreng.",
            "Pilih masakan bakar, kukus atau sup berbanding masakan bergoreng dan bersantan.",
        ]
        if diet:
            food.append("Disesuaikan dengan diet anda: " + ", ".join(label(x, lang) for x in diet)
                        + ". Sentiasa semak label makanan dan ikut nasihat doktor atau pakar "
                          "diet anda tentang alahan.")
    else:
        carbs = "rice or rice noodles (bihun, kuey teow)" if no_gluten else "rice or noodles"
        food = [
            "Use the Malaysian Healthy Plate (Suku-Suku Separuh): half vegetables and fruit, "
            f"a quarter protein ({protein}), a quarter {carbs}.",
            "Drink plain water; order teh O or kopi O kosong / kurang manis instead of teh tarik "
            "or sirap.",
            f"Breakfast: {base} with {topping} instead of roti canai or nasi lemak.",
            f"Snacks: {snacks} instead of kuih, biscuits or fried snacks.",
            "Choose grilled, steamed or soup dishes over fried and santan (coconut milk) dishes.",
        ]
        if diet:
            food.append("Adjusted for your diet: " + ", ".join(diet) + ". Always check food "
                        "labels and follow your doctor's or dietitian's advice for allergies.")
    return food


# ---------------------------------------------------------------- health conditions
CONDITION_OPTIONS = ["Joint pain / limited mobility", "Asthma", "Heart condition",
                     "High blood pressure", "Pregnant", "Kidney disease",
                     "Other long-term condition"]
# Conditions that switch the exercise plan to the gentle, low-impact version
GENTLE_CONDITIONS = {"Joint pain / limited mobility", "Heart condition", "Pregnant"}
HEALTH_NOTES = {
    "Asthma": {
        "en": "Asthma: keep your reliever inhaler with you, warm up for 10 minutes, and avoid "
              "exercising outdoors on hazy days (API above 100) or in very cold air. Indoor "
              "swimming is often well tolerated. Stop if you start wheezing.",
        "ms": "Asma: bawa inhaler pelega anda, panaskan badan selama 10 minit, dan elakkan "
              "bersenam di luar ketika jerebu (IPU melebihi 100) atau dalam udara yang sangat "
              "sejuk. Berenang di kolam tertutup biasanya sesuai. Berhenti jika mula berdehit."},
    "Heart condition": {
        "en": "Heart condition: get your doctor's clearance first and keep exercise light, so you "
              "can still talk comfortably. Stop at once if you have chest pain, palpitations or "
              "severe breathlessness.",
        "ms": "Penyakit jantung: dapatkan kebenaran doktor dahulu dan pastikan senaman ringan, "
              "sehingga anda masih boleh bercakap dengan selesa. Berhenti serta-merta jika sakit "
              "dada, berdebar-debar atau sangat sesak nafas."},
    "High blood pressure": {
        "en": "High blood pressure: avoid heavy lifting and holding your breath while exercising, "
              "check your blood pressure regularly and keep taking any prescribed medicine.",
        "ms": "Darah tinggi: elakkan mengangkat beban berat dan menahan nafas semasa bersenam, "
              "periksa tekanan darah dengan kerap dan teruskan ubat yang dipreskripsi."},
    "Pregnant": {
        "en": "Pregnancy: this tool does not check for gestational diabetes; your clinic tests for "
              "it (usually a glucose tolerance test at 24-28 weeks). Gentle walking or prenatal "
              "yoga is usually fine; avoid contact sports and lying flat on your back after the "
              "first trimester.",
        "ms": "Kehamilan: alat ini tidak memeriksa diabetes semasa hamil; klinik anda akan "
              "mengujinya (biasanya ujian toleransi glukosa pada minggu ke-24 hingga 28). Berjalan "
              "santai atau yoga pranatal biasanya sesuai; elakkan sukan yang melibatkan sentuhan badan dan berbaring "
              "terlentang selepas trimester pertama."},
    "Kidney disease": {
        "en": "Kidney disease: protein, salt and potassium needs differ, so follow your renal "
              "dietitian rather than the general food guide.",
        "ms": "Penyakit buah pinggang: keperluan protein, garam dan kalium berbeza, jadi ikut "
              "nasihat pakar diet buah pinggang anda dan bukan panduan makanan umum ini."},
    "Other long-term condition": {
        "en": "Other long-term condition: check with your doctor that this plan suits you before "
              "starting.",
        "ms": "Penyakit jangka panjang lain: tanya doktor anda sama ada pelan ini sesuai sebelum "
              "bermula."},
}

# ---------------------------------------------------------------- weekly exercise plans
PLANS = {
    "gentle": {
        "en": ["10-15 min easy walk, twice a day (indoors or with support if needed)",
               "15 min chair exercises: seated leg raises, arm circles, sit-to-stand",
               "15-20 min easy walk or water walking in a pool",
               "10 min balance practice holding a chair (heel raises, side leg lifts) + gentle "
               "stretching",
               "10-15 min easy walk, twice a day",
               "20-30 min tai chi, gentle yoga or water exercise",
               "Rest"],
        "ms": ["10-15 minit berjalan santai, dua kali sehari (di dalam rumah atau berpaut jika "
               "perlu)",
               "15 minit senaman kerusi: angkat kaki sambil duduk, putar lengan, duduk-bangun",
               "15-20 minit berjalan santai atau berjalan di dalam kolam",
               "10 minit latihan imbangan sambil berpaut pada kerusi (jengket, angkat kaki ke sisi) "
               "+ regangan ringan",
               "10-15 minit berjalan santai, dua kali sehari",
               "20-30 minit tai chi, yoga ringan atau senaman dalam air",
               "Rehat"]},
    "Low": {
        "en": ["30 min {cardio}",
               "20-30 min strength exercises (squats, wall push-ups, resistance band)",
               "30 min brisk walking",
               "Rest or 15 min stretching",
               "30 min {cardio}",
               "45 min active outing: badminton, hiking or a park walk",
               "Rest"],
        "ms": ["30 minit {cardio}",
               "20-30 minit senaman kekuatan (cangkung, tekan tubi dinding, tali rintangan)",
               "30 minit berjalan pantas",
               "Rehat atau 15 minit regangan",
               "30 minit {cardio}",
               "45 minit aktiviti luar: badminton, mendaki atau berjalan di taman",
               "Rehat"]},
    "Moderate": {
        "en": ["30 min {cardio} + 10 min walk after dinner",
               "30 min strength exercises (squats, lunges, resistance band)",
               "40 min {cardio}",
               "20 min yoga or stretching + 10 min walk after dinner",
               "30 min {cardio} + 10 min walk after dinner",
               "45-60 min active outing: badminton, hiking or cycling",
               "20 min light walk"],
        "ms": ["30 minit {cardio} + 10 minit berjalan selepas makan malam",
               "30 minit senaman kekuatan (cangkung, lunge, tali rintangan)",
               "40 minit {cardio}",
               "20 minit yoga atau regangan + 10 minit berjalan selepas makan malam",
               "30 minit {cardio} + 10 minit berjalan selepas makan malam",
               "45-60 minit aktiviti luar: badminton, mendaki atau berbasikal",
               "20 minit berjalan ringan"]},
    "High": {
        "en": ["20-30 min easy walk, ideally after a meal",
               "20 min light strength exercises (chair squats, wall push-ups)",
               "30 min easy walk",
               "15 min stretching + 10 min walk after dinner",
               "30 min easy walk",
               "30-40 min light {cardio}",
               "Rest"],
        "ms": ["20-30 minit berjalan santai, sebaik-baiknya selepas makan",
               "20 minit senaman kekuatan ringan (cangkung kerusi, tekan tubi dinding)",
               "30 minit berjalan santai",
               "15 minit regangan + 10 minit berjalan selepas makan malam",
               "30 minit berjalan santai",
               "30-40 minit {cardio} ringan",
               "Rehat"]},
}
CARDIO = {"low_impact": {"en": "swimming or cycling", "ms": "berenang atau berbasikal"},
          "normal": {"en": "brisk walking", "ms": "berjalan pantas"}}

PLAN_TEXT = {
    "rice": {"en": "Keep rice to about 1 cup per meal and switch to brown rice or mixed rice when "
                   "you can.",
             "ms": "Hadkan nasi kepada kira-kira 1 cawan setiap hidangan dan tukar kepada beras perang "
                   "atau nasi campur apabila boleh."},
    "salt": {"en": "Cut down on salt: less soy sauce (kicap), ikan bilis, salted fish, instant "
                   "noodles and processed food.",
             "ms": "Kurangkan garam: kurangkan kicap, ikan bilis, ikan masin, mi segera dan "
                   "makanan diproses."},
    "weight_kg": {"en": "Weight goal: losing 5-7% of your weight ({a}-{b} kg) over 6 months lowers "
                        "diabetes risk.",
                  "ms": "Sasaran berat: menurunkan 5-7% berat badan ({a}-{b} kg) dalam 6 bulan "
                        "mengurangkan risiko diabetes."},
    "weight": {"en": "Weight goal: losing 5-7% of your body weight over 6 months lowers diabetes "
                     "risk.",
               "ms": "Sasaran berat: menurunkan 5-7% berat badan dalam 6 bulan mengurangkan risiko "
                     "diabetes."},
    "note": {"en": "Start slowly and build up. Check with a doctor before starting exercise, "
                   "especially with high risk or other health conditions.",
             "ms": "Mula perlahan-lahan dan tingkatkan secara beransur-ansur. Berjumpa doktor "
                   "sebelum mula bersenam, terutamanya jika risiko tinggi atau ada masalah "
                   "kesihatan lain."},
    "gentle_note": {"en": "Gentle plan for age 65+, limited mobility, a heart condition or "
                          "pregnancy. Do only what feels comfortable, use a chair or rail for "
                          "support, and have someone nearby. Stop and seek help if you feel pain, "
                          "dizziness, chest pain or shortness of breath. Check with a doctor or "
                          "physiotherapist before starting.",
                    "ms": "Pelan ringan untuk umur 65 tahun ke atas, pergerakan terhad, penyakit "
                          "jantung atau kehamilan. Lakukan hanya yang selesa, gunakan kerusi atau "
                          "pemegang untuk sokongan, dan pastikan ada orang berdekatan. Berhenti "
                          "dan dapatkan bantuan jika sakit, pening, sakit dada atau sesak nafas. "
                          "Berjumpa doktor atau ahli fisioterapi sebelum bermula."},
}


def weekly_plan(band, bmi, glucose, weight=None, gentle=False, diet=(), conditions=(), lang="en"):
    """Personalised 7-day exercise plan, food guide and health notes, based on risk level, BMI,
    glucose (mg/dL), diet and health conditions. gentle=True gives a low-impact plan."""
    cardio = CARDIO["low_impact" if bmi >= 27.5 else "normal"][lang]  # 27.5 = Asian obesity cut-off
    activities = PLANS["gentle" if gentle else band][lang]
    days = [(day, act.format(cardio=cardio)) for day, act in zip(DAYS[lang], activities)]

    food = food_guide(diet, lang)
    if glucose >= 140 or band != "Low":
        food.insert(1, PLAN_TEXT["rice"][lang])
    if "High blood pressure" in conditions or "Kidney disease" in conditions:
        food.insert(2, PLAN_TEXT["salt"][lang])
    if bmi >= 23 and weight:
        food.append(PLAN_TEXT["weight_kg"][lang].format(a=f"{weight * 0.05:.1f}",
                                                        b=f"{weight * 0.07:.1f}"))
    elif bmi >= 23:
        food.append(PLAN_TEXT["weight"][lang])

    note = PLAN_TEXT["gentle_note" if gentle else "note"][lang]
    health = [HEALTH_NOTES[c][lang] for c in conditions if c in HEALTH_NOTES]
    return days, food, note, health
