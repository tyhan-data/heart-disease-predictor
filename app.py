import streamlit as st
import pandas as pd
import numpy as np
import joblib

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Heart Disease Risk Predictor",
    page_icon="🫀",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;900&family=DM+Sans:wght@300;400;500;600&display=swap');

:root {
    --red:    #e63946;
    --dark:   #0d0d0d;
    --card:   #161616;
    --border: #2a2a2a;
    --muted:  #888;
    --white:  #f5f5f0;
}

html, body, [data-testid="stAppViewContainer"] {
    background: var(--dark) !important;
    color: var(--white) !important;
    font-family: 'DM Sans', sans-serif;
}

/* Hide Streamlit chrome */
#MainMenu, footer, header { visibility: hidden; }
[data-testid="stToolbar"] { display: none; }

/* ── Hero ── */
.hero {
    text-align: center;
    padding: 3rem 1rem 2rem;
    position: relative;
}
.hero-icon {
    font-size: 4rem;
    display: block;
    margin-bottom: .5rem;
    animation: pulse 2s infinite ease-in-out;
}
@keyframes pulse {
    0%, 100% { transform: scale(1); }
    50%       { transform: scale(1.12); }
}
.hero h1 {
    font-family: 'Playfair Display', serif;
    font-size: clamp(2rem, 5vw, 3.5rem);
    font-weight: 900;
    color: var(--white);
    margin: 0;
    letter-spacing: -1px;
}
.hero h1 span { color: var(--red); }
.hero p {
    color: var(--muted);
    font-size: 1.05rem;
    font-weight: 300;
    margin-top: .6rem;
    letter-spacing: .5px;
}
.badge {
    display: inline-block;
    background: #1e0608;
    color: var(--red);
    border: 1px solid #3d0c10;
    border-radius: 999px;
    font-size: .72rem;
    font-weight: 600;
    letter-spacing: 2px;
    text-transform: uppercase;
    padding: .3rem .9rem;
    margin-bottom: 1rem;
}

/* ── Divider ── */
.divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, var(--border), transparent);
    margin: 1.5rem 0;
}

/* ── Section headers ── */
.section-label {
    font-size: .68rem;
    font-weight: 600;
    letter-spacing: 3px;
    text-transform: uppercase;
    color: var(--red);
    margin-bottom: 1rem;
    display: flex;
    align-items: center;
    gap: .5rem;
}
.section-label::after {
    content: '';
    flex: 1;
    height: 1px;
    background: var(--border);
}

/* ── Cards ── */
.card {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 1.6rem 1.8rem;
    margin-bottom: 1.2rem;
}

/* ── Streamlit widget overrides ── */
[data-testid="stSlider"] label,
[data-testid="stSelectbox"] label,
[data-testid="stNumberInput"] label {
    color: #ccc !important;
    font-size: .85rem !important;
    font-weight: 500 !important;
    letter-spacing: .3px;
}

[data-baseweb="select"] > div {
    background: #1f1f1f !important;
    border-color: var(--border) !important;
    border-radius: 10px !important;
    color: var(--white) !important;
}

[data-testid="stNumberInput"] input {
    background: #1f1f1f !important;
    border-color: var(--border) !important;
    border-radius: 10px !important;
    color: var(--white) !important;
}

[data-testid="stSlider"] [data-baseweb="slider"] div[role="slider"] {
    background: var(--red) !important;
}

/* ── Predict button ── */
div[data-testid="stButton"] > button {
    width: 100%;
    background: var(--red) !important;
    color: #fff !important;
    border: none !important;
    border-radius: 12px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 1rem !important;
    font-weight: 600 !important;
    letter-spacing: 1px !important;
    padding: .85rem 2rem !important;
    margin-top: .5rem;
    cursor: pointer;
    transition: opacity .2s, transform .15s;
}
div[data-testid="stButton"] > button:hover {
    opacity: .88;
    transform: translateY(-1px);
}

/* ── Result box ── */
.result-high {
    background: linear-gradient(135deg, #1a0406 0%, #2d0608 100%);
    border: 2px solid var(--red);
    border-radius: 20px;
    padding: 2.2rem;
    text-align: center;
}
.result-low {
    background: linear-gradient(135deg, #011a0a 0%, #032d12 100%);
    border: 2px solid #2ecc71;
    border-radius: 20px;
    padding: 2.2rem;
    text-align: center;
}
.result-icon { font-size: 3.5rem; margin-bottom: .5rem; }
.result-title {
    font-family: 'Playfair Display', serif;
    font-size: 1.8rem;
    font-weight: 700;
    margin: .4rem 0;
}
.result-subtitle { color: var(--muted); font-size: .9rem; font-weight: 400; }
.prob-bar-bg {
    background: #222;
    border-radius: 999px;
    height: 10px;
    margin: 1.2rem auto;
    max-width: 320px;
    overflow: hidden;
}
.prob-bar-fill {
    height: 100%;
    border-radius: 999px;
    transition: width 1s ease;
}
.risk-label {
    font-size: .78rem;
    letter-spacing: 2px;
    text-transform: uppercase;
    font-weight: 600;
    margin-top: .3rem;
}

/* ── Info pills ── */
.pill-row {
    display: flex;
    flex-wrap: wrap;
    gap: .5rem;
    margin-top: .8rem;
}
.pill {
    background: #1f1f1f;
    border: 1px solid var(--border);
    border-radius: 999px;
    padding: .3rem .85rem;
    font-size: .78rem;
    color: #bbb;
}
.pill span { color: var(--white); font-weight: 600; }

/* ── Footer ── */
.footer {
    text-align: center;
    color: #444;
    font-size: .75rem;
    padding: 2rem 0 1rem;
    letter-spacing: .5px;
}
.footer strong { color: #666; }
</style>
""", unsafe_allow_html=True)

# ── Load model artifacts ──────────────────────────────────────────────────────
@st.cache_resource
def load_artifacts():
    model   = joblib.load('HeartDisease.pkl')
    scaler  = joblib.load('Scaler.pkl')
    columns = joblib.load('Columns.pkl')
    return model, scaler, columns

model, scaler, columns = load_artifacts()

# ── Hero section ──────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <span class="badge">AI-Powered Clinical Tool</span>
    <span class="hero-icon">🫀</span>
    <h1>Heart Disease <span>Risk Predictor</span></h1>
    <p>Enter your clinical measurements below to assess cardiovascular risk</p>
</div>
<div class="divider"></div>
""", unsafe_allow_html=True)

# ── Layout: two columns ───────────────────────────────────────────────────────
col_left, col_right = st.columns([1.05, 1], gap="large")

with col_left:
    # ── Section 1: Demographics ──
    st.markdown('<div class="section-label">👤 &nbsp;Patient Demographics</div>', unsafe_allow_html=True)
    with st.container():
        c1, c2 = st.columns(2)
        with c1:
            age = st.slider("Age (years)", 18, 100, 45)
        with c2:
            sex = st.selectbox("Biological Sex", ["Male", "Female"])

    st.markdown('<div style="margin-top:1.4rem;"></div>', unsafe_allow_html=True)

    # ── Section 2: Cardiac Measurements ──
    st.markdown('<div class="section-label">🩺 &nbsp;Cardiac Measurements</div>', unsafe_allow_html=True)

    c3, c4 = st.columns(2)
    with c3:
        chest_pain = st.selectbox(
            "Chest Pain Type",
            ["ATA – Atypical Angina", "NAP – Non-Anginal Pain",
             "TA – Typical Angina",   "ASY – Asymptomatic"],
        )
    with c4:
        resting_bp = st.slider("Resting Blood Pressure (mmHg)", 80, 200, 120)

    c5, c6 = st.columns(2)
    with c5:
        cholesterol = st.slider("Cholesterol (mg/dL)", 100, 600, 200)
    with c6:
        max_hr = st.slider("Max Heart Rate (bpm)", 60, 220, 150)

    st.markdown('<div style="margin-top:1.4rem;"></div>', unsafe_allow_html=True)

    # ── Section 3: Additional Indicators ──
    st.markdown('<div class="section-label">📊 &nbsp;Additional Indicators</div>', unsafe_allow_html=True)

    c7, c8 = st.columns(2)
    with c7:
        fasting_bs = st.selectbox("Fasting Blood Sugar > 120 mg/dL", ["No", "Yes"])
    with c8:
        exercise_angina = st.selectbox("Exercise-Induced Angina", ["No", "Yes"])

    c9, c10 = st.columns(2)
    with c9:
        old_peak = st.slider("Oldpeak – ST Depression", 0.0, 6.0, 1.0, step=0.1)
    with c10:
        st_slope = st.selectbox("ST Slope", ["Up", "Flat", "Down"])

    resting_ecg = st.selectbox(
        "Resting ECG",
        ["Normal", "ST – ST-T wave abnormality", "LVH – Left Ventricular Hypertrophy"],
    )

# ── Right column: summary + prediction ───────────────────────────────────────
with col_right:
    st.markdown('<div class="section-label">📋 &nbsp;Patient Summary</div>', unsafe_allow_html=True)

    # Helper: strip the code prefix for display
    cp_display  = chest_pain.split("–")[0].strip()
    ecg_display = resting_ecg.split("–")[0].strip()

    st.markdown(f"""
    <div class="pill-row">
        <div class="pill">Age <span>{age} yrs</span></div>
        <div class="pill">Sex <span>{sex}</span></div>
        <div class="pill">BP <span>{resting_bp} mmHg</span></div>
        <div class="pill">Cholesterol <span>{cholesterol} mg/dL</span></div>
        <div class="pill">Max HR <span>{max_hr} bpm</span></div>
        <div class="pill">Oldpeak <span>{old_peak}</span></div>
        <div class="pill">Fasting BS <span>{fasting_bs}</span></div>
        <div class="pill">Angina <span>{exercise_angina}</span></div>
        <div class="pill">ST Slope <span>{st_slope}</span></div>
        <div class="pill">Chest Pain <span>{cp_display}</span></div>
        <div class="pill">ECG <span>{ecg_display}</span></div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div style="margin-top:1.6rem;"></div>', unsafe_allow_html=True)
    predict_clicked = st.button("🫀  Analyse Risk Now")

    st.markdown('<div class="divider" style="margin:1.4rem 0;"></div>', unsafe_allow_html=True)

    # ── Prediction logic ──────────────────────────────────────────────────────
    if predict_clicked:
        # Encode inputs
        sex_m           = 1 if sex == "Male" else 0
        cp_code         = cp_display  # already 'ATA', 'NAP', 'TA', or 'ASY'
        cp_ata          = 1 if cp_code == "ATA" else 0
        cp_nap          = 1 if cp_code == "NAP" else 0
        cp_ta           = 1 if cp_code == "TA"  else 0

        fasting_bs_val  = 1 if fasting_bs == "Yes" else 0
        ex_angina_y     = 1 if exercise_angina == "Yes" else 0

        ecg_code        = ecg_display  # 'Normal', 'ST', 'LVH'
        ecg_normal      = 1 if ecg_code == "Normal" else 0
        ecg_st          = 1 if ecg_code == "ST"     else 0

        slope_flat      = 1 if st_slope == "Flat" else 0
        slope_up        = 1 if st_slope == "Up"   else 0

        row = {
            'Age':               age,
            'RestingBP':         resting_bp,
            'Cholesterol':       cholesterol,
            'FastingBS':         fasting_bs_val,
            'MaxHR':             max_hr,
            'Oldpeak':           old_peak,
            'Sex_M':             sex_m,
            'ChestPainType_ATA': cp_ata,
            'ChestPainType_NAP': cp_nap,
            'ChestPainType_TA':  cp_ta,
            'RestingECG_Normal': ecg_normal,
            'RestingECG_ST':     ecg_st,
            'ExerciseAngina_Y':  ex_angina_y,
            'ST_Slope_Flat':     slope_flat,
            'ST_Slope_Up':       slope_up,
        }

        df_input = pd.DataFrame([row])[columns]
        df_scaled = scaler.transform(df_input)

        prediction = model.predict(df_scaled)[0]
        probability = model.predict_proba(df_scaled)[0][1]
        pct = round(probability * 100, 1)

        if prediction == 1:
            bar_color = "#e63946"
            st.markdown(f"""
            <div class="result-high">
                <div class="result-icon">⚠️</div>
                <div class="result-title" style="color:#e63946;">Elevated Risk Detected</div>
                <div class="result-subtitle">Heart disease risk indicators present</div>
                <div class="prob-bar-bg">
                    <div class="prob-bar-fill" style="width:{pct}%;background:{bar_color};"></div>
                </div>
                <div style="font-size:2rem;font-weight:700;color:#e63946;">{pct}%</div>
                <div class="risk-label" style="color:#e63946;">Risk Probability</div>
                <p style="color:#888;font-size:.82rem;margin-top:1rem;line-height:1.6;">
                    This result suggests a higher-than-normal likelihood of heart disease.<br>
                    Please consult a qualified cardiologist for a full clinical evaluation.
                </p>
            </div>
            """, unsafe_allow_html=True)
        else:
            bar_color = "#2ecc71"
            st.markdown(f"""
            <div class="result-low">
                <div class="result-icon">✅</div>
                <div class="result-title" style="color:#2ecc71;">Low Risk Profile</div>
                <div class="result-subtitle">No significant heart disease indicators detected</div>
                <div class="prob-bar-bg">
                    <div class="prob-bar-fill" style="width:{pct}%;background:{bar_color};"></div>
                </div>
                <div style="font-size:2rem;font-weight:700;color:#2ecc71;">{pct}%</div>
                <div class="risk-label" style="color:#2ecc71;">Risk Probability</div>
                <p style="color:#888;font-size:.82rem;margin-top:1rem;line-height:1.6;">
                    Your current profile appears to be within a healthy range.<br>
                    Maintain regular check-ups and a heart-healthy lifestyle.
                </p>
            </div>
            """, unsafe_allow_html=True)

    else:
        st.markdown("""
        <div style="background:#111;border:1px dashed #2a2a2a;border-radius:20px;
                    padding:3rem 2rem;text-align:center;color:#444;">
            <div style="font-size:3rem;margin-bottom:.8rem;opacity:.4;">🫀</div>
            <div style="font-size:.9rem;letter-spacing:1px;font-weight:500;">
                Fill in the form and click<br><strong style="color:#666;">Analyse Risk Now</strong>
            </div>
        </div>
        """, unsafe_allow_html=True)

# ── Disclaimer ────────────────────────────────────────────────────────────────
st.markdown('<div class="divider" style="margin-top:2rem;"></div>', unsafe_allow_html=True)
st.markdown("""
<div class="footer">
    ⚕️ &nbsp;This tool is for <strong>educational purposes only</strong> and does not constitute medical advice.<br>
    Always consult a licensed physician for clinical decisions. &nbsp;·&nbsp; Built by <strong>M.A.T</strong>
</div>
""", unsafe_allow_html=True)






