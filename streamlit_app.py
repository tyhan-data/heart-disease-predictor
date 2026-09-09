import streamlit as st
import requests


# ═════════════════════════════════════════════════════════════════════════════
# PAGE CONFIG
# ═════════════════════════════════════════════════════════════════════════════

st.set_page_config(
    page_title="Heart Disease Predictor",
    page_icon="🫀",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# ═════════════════════════════════════════════════════════════════════════════
# CUSTOM CSS

# Palette:
#   background   #F4F6F5  (cool, clinical off-white — chart-paper, not cream)
#   ink          #1C2422  (near-black with a green undertone)
#   panel        #FFFFFF  (cards / inputs)
#   line         #DCE2E0  (hairline borders)
#   accent-teal  #1F5C55  (primary — trust, clinical calm)
#   accent-amber #B8862B  (secondary — used for muted labels/eyebrows)
#   risk-high    #B3392E
#   risk-low     #2E7D4F

# Type:
#   Display  "Source Serif 4" — headline, result numbers (journal / chart feel)
#   Body     "Inter"          — labels, inputs, body copy
# ═════════════════════════════════════════════════════════════════════════════

st.markdown(
    """
    <style>

    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Source+Serif+4:opsz,wght@8..60,600;8..60,700;8..60,800&display=swap');

    /* ---------------------------------------------------------------------
       Global
       --------------------------------------------------------------------- */

    .stApp {
        background: #F4F6F5;
        color: #1C2422;
        font-family: 'Inter', sans-serif;
    }

    #MainMenu, footer, header { visibility: hidden; }

    h1, h2, h3 { font-family: 'Source Serif 4', serif; }

    /* ---------------------------------------------------------------------
       Hero
       --------------------------------------------------------------------- */

    .hero {
        padding: 8px 4px 28px;
        border-bottom: 1px solid #DCE2E0;
        margin-bottom: 28px;
    }

    .hero-kicker {
        color: #1F5C55;
        font-size: 13px;
        font-weight: 600;
        letter-spacing: 0.4px;
    }

    .hero-title {
        font-family: 'Source Serif 4', serif;
        font-size: 42px;
        font-weight: 700;
        line-height: 1.15;
        color: #1C2422;
        margin: 6px 0 10px;
    }

    .hero-title em {
        font-style: italic;
        color: #1F5C55;
    }

    .hero-subtitle {
        color: #5B6663;
        font-size: 16px;
        max-width: 640px;
        line-height: 1.5;
    }

    /* ---------------------------------------------------------------------
       Section titles
       --------------------------------------------------------------------- */

    .section-title {
        font-family: 'Source Serif 4', serif;
        color: #1C2422;
        font-size: 19px;
        font-weight: 700;
        margin-top: 6px;
        margin-bottom: 14px;
        padding-bottom: 8px;
        border-bottom: 2px solid #1F5C55;
        display: inline-block;
    }

    /* ---------------------------------------------------------------------
       Inputs
       --------------------------------------------------------------------- */

    label {
        color: #3D4744 !important;
        font-weight: 500 !important;
        font-size: 14px !important;
    }

    [data-baseweb="select"] > div {
        background-color: #FFFFFF !important;
        border-color: #DCE2E0 !important;
        border-radius: 8px !important;
    }

    input {
        background-color: #FFFFFF !important;
        color: #1C2422 !important;
    }

    [data-testid="stSlider"] { padding-bottom: 6px; }

    [data-testid="stSlider"] div[role="slider"] {
        background-color: #1F5C55 !important;
    }

    /* ---------------------------------------------------------------------
       Predict button
       --------------------------------------------------------------------- */

    div.stButton > button {
        width: 100%;
        background: #1F5C55;
        color: #FFFFFF;
        border: none;
        border-radius: 10px;
        padding: 14px;
        font-size: 15px;
        font-weight: 600;
        letter-spacing: 0.3px;
        margin-top: 14px;
        transition: 0.15s ease;
    }

    div.stButton > button:hover {
        background: #163F3A;
        color: #FFFFFF;
    }

    /* ---------------------------------------------------------------------
       Patient summary pills
       --------------------------------------------------------------------- */

    .summary-box {
        background: #FFFFFF;
        border: 1px solid #DCE2E0;
        border-radius: 12px;
        padding: 18px;
    }

    .summary-item {
        display: inline-flex;
        align-items: baseline;
        gap: 5px;
        background: #F4F6F5;
        border: 1px solid #DCE2E0;
        border-radius: 20px;
        padding: 6px 12px;
        margin: 4px;
        font-size: 13px;
        color: #5B6663;
    }

    .summary-item strong {
        color: #1C2422;
        font-weight: 600;
    }

    /* ---------------------------------------------------------------------
       Result panel
       --------------------------------------------------------------------- */

    .result-card {
        border-radius: 14px;
        padding: 28px;
        text-align: center;
        margin-top: 20px;
        border: 1px solid;
    }

    .result-card.high-risk {
        background: #FBF1EF;
        border-color: #E3B4AC;
    }

    .result-card.low-risk {
        background: #EFF6F1;
        border-color: #AFD9BE;
    }

    .result-icon { font-size: 34px; }

    .result-title {
        font-family: 'Source Serif 4', serif;
        font-size: 24px;
        font-weight: 700;
        margin-top: 6px;
    }

    .result-subtitle {
        color: #5B6663;
        font-size: 14px;
        margin-top: 4px;
    }

    .result-probability {
        font-family: 'Source Serif 4', serif;
        font-size: 44px;
        font-weight: 800;
        margin: 14px 0 2px;
    }

    .result-probability-label {
        font-size: 12px;
        letter-spacing: 0.4px;
        color: #5B6663;
        margin-bottom: 14px;
    }

    .result-description {
        color: #5B6663;
        font-size: 13.5px;
        line-height: 1.7;
        max-width: 420px;
        margin: 12px auto 0;
    }

    .progress-background {
        width: 100%;
        max-width: 360px;
        height: 8px;
        background: #E4E9E7;
        border-radius: 20px;
        margin: 0 auto;
        overflow: hidden;
    }

    .progress-fill {
        height: 100%;
        border-radius: 20px;
    }

    /* ---------------------------------------------------------------------
       Footer
       --------------------------------------------------------------------- */

    .footer {
        text-align: center;
        color: #8A928F;
        font-size: 12px;
        margin-top: 44px;
        padding: 18px;
        border-top: 1px solid #DCE2E0;
        line-height: 1.7;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ═════════════════════════════════════════════════════════════════════════════
# HERO
# ═════════════════════════════════════════════════════════════════════════════

st.markdown("""
<div class="hero">
    <div class="hero-kicker">AI-ASSISTED CLINICAL SCREENING TOOL</div>
    <div class="hero-title">Heart Disease <em>Risk Predictor</em></div>
    <div class="hero-subtitle">
        Enter a patient's clinical measurements below to estimate their
        cardiovascular risk profile.
    </div>
</div>
""", unsafe_allow_html=True)


# ═════════════════════════════════════════════════════════════════════════════
# API CONFIGURATION
# ═════════════════════════════════════════════════════════════════════════════

API_URL = "https://heart-disease-predictor-1-z6d6.onrender.com/predict"

# ═════════════════════════════════════════════════════════════════════════════
# MAIN LAYOUT
# ═════════════════════════════════════════════════════════════════════════════

left, right = st.columns([1, 1], gap="large")


# ═════════════════════════════════════════════════════════════════════════════
# LEFT SIDE — INPUTS
# ═════════════════════════════════════════════════════════════════════════════

with left:

    # -------------------------------------------------------------------
    # Demographics
    # -------------------------------------------------------------------

    st.markdown('<div class="section-title">Patient Demographics</div>', unsafe_allow_html=True)

    age = st.slider("Age", min_value=18, max_value=100, value=40)

    sex = st.selectbox("Biological Sex", options=["Male", "Female"])

    # -------------------------------------------------------------------
    # Cardiac Measurements
    # -------------------------------------------------------------------

    st.markdown('<div class="section-title">Cardiac Measurements</div>', unsafe_allow_html=True)

    chest_pain = st.selectbox(
        "Chest Pain Type",
        options=[
            "ATA – Atypical Angina",
            "NAP – Non-Anginal Pain",
            "TA – Typical Angina",
            "ASY – Asymptomatic",
        ]
    )

    resting_bp = st.slider("Resting Blood Pressure (mmHg)", min_value=80, max_value=200, value=120)

    cholesterol = st.slider("Cholesterol (mg/dL)", min_value=85, max_value=600, value=200)

    max_hr = st.slider("Maximum Heart Rate (bpm)", min_value=60, max_value=220, value=150)

    # -------------------------------------------------------------------
    # Additional Indicators
    # -------------------------------------------------------------------

    st.markdown('<div class="section-title">Additional Indicators</div>', unsafe_allow_html=True)

    fasting_bs = st.selectbox("Fasting Blood Sugar > 120 mg/dL", options=["No", "Yes"])

    resting_ecg = st.selectbox(
        "Resting ECG",
        options=[
            "Normal",
            "ST – ST-T wave abnormality",
            "LVH – Left Ventricular Hypertrophy",
        ]
    )

    exercise_angina = st.selectbox("Exercise-Induced Angina", options=["No", "Yes"])

    old_peak = st.slider("Oldpeak – ST Depression", min_value=0.0, max_value=6.0, value=1.0, step=0.1)

    st_slope = st.selectbox("ST Slope", options=["Up", "Flat", "Down"])

    # -------------------------------------------------------------------
    # Prediction Button
    # -------------------------------------------------------------------

    predict = st.button("Analyse Heart Disease Risk")


# ═════════════════════════════════════════════════════════════════════════════
# RIGHT SIDE — SUMMARY + RESULT
# ═════════════════════════════════════════════════════════════════════════════

with right:

    st.markdown('<div class="section-title">Patient Summary</div>', unsafe_allow_html=True)

    # Helper: strip the code prefix for display
    cp_display = chest_pain.split("–")[0].strip()
    ecg_display = resting_ecg.split("–")[0].strip()

    st.markdown(f"""
    <div class="summary-box">
        <span class="summary-item">Age <strong>{age} yrs</strong></span>
        <span class="summary-item">Sex <strong>{sex}</strong></span>
        <span class="summary-item">BP <strong>{resting_bp} mmHg</strong></span>
        <span class="summary-item">Cholesterol <strong>{cholesterol} mg/dL</strong></span>
        <span class="summary-item">Max HR <strong>{max_hr} bpm</strong></span>
        <span class="summary-item">Oldpeak <strong>{old_peak}</strong></span>
        <span class="summary-item">Fasting BS <strong>{fasting_bs}</strong></span>
        <span class="summary-item">Angina <strong>{exercise_angina}</strong></span>
        <span class="summary-item">ST Slope <strong>{st_slope}</strong></span>
        <span class="summary-item">Chest Pain <strong>{cp_display}</strong></span>
        <span class="summary-item">ECG <strong>{ecg_display}</strong></span>
    </div>
    """, unsafe_allow_html=True)

    # ═════════════════════════════════════════════════════════════════════
    # API REQUEST
    # ═════════════════════════════════════════════════════════════════════

    if predict:

        # -------------------------------------------------------------------
        # Convert UI values to FastAPI values
        # -------------------------------------------------------------------

        sex_api = {"Male": "M", "Female": "F"}[sex]

        chest_pain_api = {
            "ATA – Atypical Angina": "ATA",
            "NAP – Non-Anginal Pain": "NAP",
            "TA – Typical Angina": "TA",
            "ASY – Asymptomatic": "ASY"
        }[chest_pain]

        fasting_bs_api = {"No": '0', "Yes": '1'}[fasting_bs]

        resting_ecg_api = {
            "Normal": "Normal",
            "ST – ST-T wave abnormality": "ST",
            "LVH – Left Ventricular Hypertrophy": "LVH"
        }[resting_ecg]

        exercise_angina_api = {"No": "N", "Yes": "Y"}[exercise_angina]

        # -------------------------------------------------------------------
        # EXACT FastAPI Request Body
        # -------------------------------------------------------------------

        payload = {
            "Age": age,
            "Sex": sex_api,
            "ChestPainType": chest_pain_api,
            "RestingBP": resting_bp,
            "Cholesterol": cholesterol,
            "FastingBS": fasting_bs_api,
            "RestingECG": resting_ecg_api,
            "MaxHR": max_hr,
            "ExerciseAngina": exercise_angina_api,
            "Oldpeak": old_peak,
            "ST_Slope": st_slope
        }

        # -------------------------------------------------------------------
        # Call FastAPI
        # -------------------------------------------------------------------

        with st.spinner("Analysing patient data..."):

            try:

                response = requests.post(API_URL, json=payload, timeout=15)

                # ═════════════════════════════════════════════════════════
                # SUCCESS
                # ═════════════════════════════════════════════════════════

                if response.status_code == 200:

                    result = response.json()
                    prediction = result["HeartDisease"]
                    probability = result["probability"]
                    percentage = probability * 100

                    if prediction == 1:
                        risk_class = "high-risk"
                        bar_color = "#B3392E"
                        text_color = "#B3392E"
                        icon = "⚠️"
                        title = "Elevated Risk Detected"
                        subtitle = "Heart disease risk indicators present"
                        description = (
                            "This result suggests a higher-than-normal likelihood "
                            "of heart disease.<br>Please consult a qualified "
                            "cardiologist for a full clinical evaluation."
                        )
                    else:
                        risk_class = "low-risk"
                        bar_color = "#2E7D4F"
                        text_color = "#2E7D4F"
                        icon = "✅"
                        title = "Low Risk Profile"
                        subtitle = "No significant heart disease indicators detected"
                        description = (
                            "Your current profile appears to be within a healthy "
                            "range.<br>Maintain regular check-ups and a "
                            "heart-healthy lifestyle."
                        )

                    st.markdown(f"""
                    <div class="result-card {risk_class}">
                        <div class="result-icon">{icon}</div>
                        <div class="result-title" style="color:{text_color};">{title}</div>
                        <div class="result-subtitle">{subtitle}</div>
                        <div class="result-probability" style="color:{text_color};">{percentage:.1f}%</div>
                        <div class="result-probability-label">RISK PROBABILITY</div>
                        <div class="progress-background">
                            <div class="progress-fill" style="width:{percentage}%;background:{bar_color};"></div>
                        </div>
                        <p class="result-description">{description}</p>
                    </div>
                    """, unsafe_allow_html=True)


                # ═════════════════════════════════════════════════════════
                # VALIDATION ERROR
                # ═════════════════════════════════════════════════════════

                elif response.status_code == 422:

                    st.error("FastAPI rejected the input data.")
                    st.write("Validation details:")

                    try:
                        st.json(response.json())
                    except Exception:
                        st.code(response.text)

                # ═════════════════════════════════════════════════════════
                # SERVER ERROR
                # ═════════════════════════════════════════════════════════

                elif response.status_code >= 500:

                    st.error("FastAPI encountered an internal server error.")

                    try:
                        st.json(response.json())
                    except Exception:
                        st.code(response.text)

                # ═════════════════════════════════════════════════════════
                # OTHER ERROR
                # ═════════════════════════════════════════════════════════

                else:

                    st.error(f"API request failed (Status Code: {response.status_code})")

                    try:
                        st.json(response.json())
                    except Exception:
                        st.code(response.text)

            # ═════════════════════════════════════════════════════════════
            # CONNECTION ERROR
            # ═════════════════════════════════════════════════════════════

            except requests.exceptions.ConnectionError:

                st.error("❌ Could not connect to FastAPI.")
                st.info("Make sure your FastAPI server is running on http://127.0.0.1:8000")

            # ═════════════════════════════════════════════════════════════
            # TIMEOUT
            # ═════════════════════════════════════════════════════════════

            except requests.exceptions.Timeout:

                st.error("⏱️ The API request timed out.")

            # ═════════════════════════════════════════════════════════════
            # OTHER REQUEST ERROR
            # ═════════════════════════════════════════════════════════════

            except requests.exceptions.RequestException as e:

                st.error(f"❌ Request failed: {e}")

            # ═════════════════════════════════════════════════════════════
            # UNEXPECTED ERROR
            # ═════════════════════════════════════════════════════════════

            except Exception as e:

                st.error(f"Unexpected error: {e}")


# ═════════════════════════════════════════════════════════════════════════════
# FOOTER
# ═════════════════════════════════════════════════════════════════════════════

st.markdown("""
<div class="footer">
    ⚕️ This tool is for <strong>educational purposes only</strong> and does not constitute medical advice.<br>
    Always consult a licensed physician for clinical decisions. · Built by <strong>M.A.T</strong>
</div>
""", unsafe_allow_html=True)