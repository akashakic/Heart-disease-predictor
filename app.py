import streamlit as st
import pandas as pd
import joblib
from pathlib import Path

# ---------- Page config ----------
st.set_page_config(
    page_title="CardioScan | Heart Risk Predictor",
    page_icon="🫀",
    layout="wide",
)

# ---------- Custom CSS ----------
st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

:root {
    --bg: #070d14;
    --panel: rgba(15, 25, 35, 0.72);
    --line: rgba(120, 255, 225, 0.14);
    --teal: #2ef2c0;
    --teal-dim: rgba(46, 242, 192, 0.12);
    --coral: #ff5d73;
    --coral-dim: rgba(255, 93, 115, 0.12);
    --text: #e6f1ef;
    --muted: #8aa3a0;
}

html, body, [class*="css"], .stApp {
    font-family: 'Space Grotesk', sans-serif;
}

.stApp {
    background:
        radial-gradient(900px 500px at 8% -5%, rgba(46, 242, 192, 0.13), transparent 60%),
        radial-gradient(800px 500px at 100% 10%, rgba(255, 93, 115, 0.10), transparent 60%),
        linear-gradient(rgba(255,255,255,0.025) 1px, transparent 1px),
        linear-gradient(90deg, rgba(255,255,255,0.025) 1px, transparent 1px),
        var(--bg);
    background-size: auto, auto, 38px 38px, 38px 38px, auto;
    color: var(--text);
}

header[data-testid="stHeader"] { background: transparent; }
.block-container { padding-top: 2rem; max-width: 1250px; }
footer {visibility: hidden;}
#MainMenu {visibility: hidden;}

/* ---------- Hero ---------- */
.hero {
    position: relative;
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 24px;
    padding: 30px 36px;
    border-radius: 22px;
    background: linear-gradient(135deg, rgba(15,25,35,0.95), rgba(10,18,26,0.85));
    border: 1px solid var(--line);
    box-shadow: 0 0 0 1px rgba(46,242,192,0.04), 0 20px 60px rgba(0,0,0,0.45);
    overflow: hidden;
    margin-bottom: 26px;
}
.hero::before {
    content: "";
    position: absolute; inset: 0;
    background: radial-gradient(500px 220px at 85% 50%, rgba(46,242,192,0.12), transparent 70%);
    pointer-events: none;
}
.eyebrow {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.72rem;
    letter-spacing: 0.28em;
    color: var(--teal);
    display: flex; align-items: center; gap: 10px;
}
.dot {
    width: 8px; height: 8px; border-radius: 50%;
    background: var(--teal);
    box-shadow: 0 0 0 0 rgba(46,242,192,0.7);
    animation: ping 1.8s infinite;
}
@keyframes ping {
    0%   { box-shadow: 0 0 0 0 rgba(46,242,192,0.6); }
    70%  { box-shadow: 0 0 0 12px rgba(46,242,192,0); }
    100% { box-shadow: 0 0 0 0 rgba(46,242,192,0); }
}
.hero h1 {
    margin: 10px 0 6px 0;
    font-size: 2.7rem;
    font-weight: 700;
    letter-spacing: -0.02em;
    color: #fff;
    line-height: 1.05;
}
.hero h1 span { color: var(--teal); }
.hero p { margin: 0; color: var(--muted); font-size: 1rem; max-width: 520px; }
.ecg { flex: 0 0 340px; max-width: 45%; }
.ecg path.base { stroke: rgba(46,242,192,0.18); }
.ecg path.live {
    stroke: var(--teal);
    stroke-dasharray: 520;
    stroke-dashoffset: 520;
    filter: drop-shadow(0 0 6px rgba(46,242,192,0.9));
    animation: trace 3.2s linear infinite;
}
@keyframes trace {
    0%   { stroke-dashoffset: 520; opacity: 1; }
    80%  { stroke-dashoffset: 0;   opacity: 1; }
    100% { stroke-dashoffset: 0;   opacity: 0; }
}

/* ---------- Tabs ---------- */
.stTabs [data-baseweb="tab-list"] {
    gap: 8px;
    background: rgba(255,255,255,0.03);
    padding: 6px;
    border-radius: 14px;
    border: 1px solid var(--line);
}
.stTabs [data-baseweb="tab"] {
    height: 44px;
    border-radius: 10px;
    padding: 0 18px;
    color: var(--muted);
    font-weight: 500;
}
.stTabs [aria-selected="true"] {
    background: var(--teal-dim);
    color: var(--teal) !important;
}
.stTabs [data-baseweb="tab-highlight"],
.stTabs [data-baseweb="tab-border"] { display: none; }
.stTabs [data-baseweb="tab-panel"] {
    margin-top: 14px;
    padding: 22px 24px 14px 24px;
    background: var(--panel);
    border: 1px solid var(--line);
    border-radius: 18px;
    backdrop-filter: blur(8px);
}

.sec {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.72rem;
    letter-spacing: 0.22em;
    text-transform: uppercase;
    color: var(--teal);
    margin: 0 0 14px 0;
    padding-bottom: 10px;
    border-bottom: 1px dashed var(--line);
}

/* ---------- Inputs ---------- */
label, .stMarkdown p { color: var(--text); }
div[data-baseweb="input"], div[data-baseweb="select"] > div, div[data-baseweb="base-input"] {
    background-color: rgba(255,255,255,0.04) !important;
    border-radius: 10px !important;
    border-color: var(--line) !important;
}
div[data-testid="stNumberInput"] button { background: transparent; color: var(--teal); }

/* ---------- Analyze button ---------- */
div.stButton > button {
    width: 100%;
    background: linear-gradient(90deg, #2ef2c0, #19b8e0);
    color: #04100d;
    border: none;
    border-radius: 14px;
    padding: 0.85rem 1rem;
    font-size: 1.05rem;
    font-weight: 700;
    letter-spacing: 0.04em;
    transition: transform .15s ease, box-shadow .15s ease;
}
div.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 10px 30px rgba(46,242,192,0.35);
    color: #04100d;
    border: none;
}
div.stButton > button:active { color: #04100d; }

/* ---------- Result side ---------- */
.console-title {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.78rem;
    letter-spacing: 0.24em;
    color: var(--muted);
    margin-bottom: 10px;
}
.idle {
    padding: 34px 26px;
    text-align: center;
    border-radius: 18px;
    background: var(--panel);
    border: 1px dashed rgba(46,242,192,0.28);
    margin-top: 14px;
}
.idle svg { width: 100%; max-width: 260px; opacity: 0.8; }
.idle h3 { margin: 10px 0 6px 0; font-size: 1.1rem; color: #fff; }
.idle p  { margin: 0; color: var(--muted); font-size: 0.92rem; }

.verdict {
    margin-top: 14px;
    padding: 22px 24px;
    border-radius: 18px;
    background: var(--panel);
    border: 1px solid var(--line);
    border-left: 5px solid var(--c);
    box-shadow: 0 0 40px var(--glow);
}
.chip {
    display: inline-block;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.7rem;
    letter-spacing: 0.2em;
    padding: 5px 12px;
    border-radius: 999px;
    color: var(--c);
    background: var(--glow);
    border: 1px solid var(--c);
}
.verdict h2 { margin: 12px 0 6px 0; font-size: 1.6rem; color: #fff; }
.verdict p  { margin: 0; color: var(--muted); font-size: 0.95rem; }
.verdict.high { --c: var(--coral); --glow: var(--coral-dim); }
.verdict.low  { --c: var(--teal);  --glow: var(--teal-dim); }

.gauge-wrap { display: flex; justify-content: center; margin: 22px 0 8px 0; }
.gauge {
    width: 178px; height: 178px; border-radius: 50%;
    display: grid; place-items: center;
    background: conic-gradient(var(--c) calc(var(--p) * 1%), rgba(255,255,255,0.08) 0);
    box-shadow: 0 0 46px var(--glow);
}
.gauge-in {
    width: 136px; height: 136px; border-radius: 50%;
    background: #0a131b;
    display: flex; flex-direction: column; align-items: center; justify-content: center;
}
.gauge-in b { font-size: 2.3rem; color: #fff; line-height: 1; }
.gauge-in small {
    margin-top: 6px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.58rem; letter-spacing: 0.18em; color: var(--muted);
}
.gauge.high { --c: var(--coral); --glow: var(--coral-dim); }
.gauge.low  { --c: var(--teal);  --glow: var(--teal-dim); }

.tiles { display: grid; grid-template-columns: repeat(4, 1fr); gap: 10px; margin-top: 14px; }
.tile {
    padding: 12px 8px;
    text-align: center;
    border-radius: 12px;
    background: rgba(255,255,255,0.04);
    border: 1px solid var(--line);
}
.tile b { display: block; font-size: 1.15rem; color: #fff; }
.tile span {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.6rem; letter-spacing: 0.14em; color: var(--muted);
}

.disclaimer {
    margin-top: 18px;
    font-size: 0.8rem;
    color: var(--muted);
    text-align: center;
}

/* ---------- Sidebar ---------- */
section[data-testid="stSidebar"] {
    background: rgba(8, 15, 22, 0.97);
    border-right: 1px solid var(--line);
}
.brand { font-size: 1.5rem; font-weight: 700; color: #fff; letter-spacing: -0.01em; }
.brand span { color: var(--teal); }
.steps { list-style: none; padding: 0; margin: 8px 0 0 0; }
.steps li {
    display: flex; gap: 12px; align-items: flex-start;
    padding: 10px 0; color: var(--text); font-size: 0.92rem;
    border-bottom: 1px dashed var(--line);
}
.steps li i {
    flex: 0 0 24px; height: 24px; border-radius: 50%;
    display: grid; place-items: center;
    font-style: normal; font-size: 0.75rem; font-weight: 700;
    color: #04100d; background: var(--teal);
}
.note {
    margin-top: 6px; padding: 12px 14px; border-radius: 12px;
    background: var(--coral-dim); border: 1px solid rgba(255,93,115,0.35);
    color: #ffd5db; font-size: 0.85rem;
}

@media (max-width: 900px) {
    .hero { flex-direction: column; align-items: flex-start; }
    .ecg { max-width: 100%; flex-basis: auto; }
    .tiles { grid-template-columns: repeat(2, 1fr); }
}
</style>
    """,
    unsafe_allow_html=True,
)


# ---------- Load saved model, scaler, and expected columns ----------
BASE_DIR = Path(__file__).parent
if not (BASE_DIR / "LR_heart.pkl").exists():
    for _p in BASE_DIR.rglob("LR_heart.pkl"):
        BASE_DIR = _p.parent
        break

if not (BASE_DIR / "LR_heart.pkl").exists():
    _root = Path(__file__).parent
    _files = sorted(str(p.relative_to(_root)) for p in _root.rglob("*") if ".git" not in p.parts)
    st.error("LR_heart.pkl nahi mili. Repo mein yeh files hain: " + ", ".join(_files[:40]))
    st.stop()


@st.cache_resource
def load_artifacts():
    model = joblib.load(BASE_DIR / "LR_heart.pkl")
    scaler = joblib.load(BASE_DIR / "heart_scaler.pkl")
    expected_columns = joblib.load(BASE_DIR / "heart_columns.pkl")
    return model, scaler, expected_columns


model, scaler, expected_columns = load_artifacts()

# ---------- Sidebar ----------
with st.sidebar:
    st.markdown(
        """
<div class="brand">🫀 Cardio<span>Scan</span></div>
<div style="color:#8aa3a0;font-size:0.85rem;margin-top:4px;">Logistic Regression based heart disease risk checker</div>
        """,
        unsafe_allow_html=True,
    )
    st.divider()
    st.markdown(
        """
<div class="console-title">HOW IT WORKS</div>
<ul class="steps">
<li><i>1</i><span>Fill in the patient details across the three tabs</span></li>
<li><i>2</i><span>Press <b>Analyze Risk</b></span></li>
<li><i>3</i><span>The result appears on the right side</span></li>
</ul>
        """,
        unsafe_allow_html=True,
    )
    st.divider()
    st.markdown(
        '<div class="note">⚕️ This is an educational tool, not a substitute for medical advice.</div>',
        unsafe_allow_html=True,
    )
    st.caption("Built by Aakash")

# ---------- Header ----------
st.markdown(
    """
<div class="hero">
<div>
<div class="eyebrow"><span class="dot"></span>AI · HEART HEALTH SCREENING</div>
<h1>Cardio<span>Scan</span></h1>
<p>Enter the health details and get an instant heart disease risk assessment from a machine learning model.</p>
</div>
<svg class="ecg" viewBox="0 0 340 90" fill="none" xmlns="http://www.w3.org/2000/svg">
<path class="base" stroke-width="2" d="M0 45 H50 L62 45 L72 18 L84 78 L94 45 H150 L162 45 L172 18 L184 78 L194 45 H250 L262 45 L272 18 L284 78 L294 45 H340"/>
<path class="live" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round" d="M0 45 H50 L62 45 L72 18 L84 78 L94 45 H150 L162 45 L172 18 L184 78 L194 45 H250 L262 45 L272 18 L284 78 L294 45 H340"/>
</svg>
</div>
    """,
    unsafe_allow_html=True,
)

left, right = st.columns([1.35, 1], gap="large")

# ---------- Inputs ----------
with left:
    tab1, tab2, tab3 = st.tabs(["👤 Personal", "🩺 Vitals", "📈 ECG & Exercise"])

    with tab1:
        st.markdown('<div class="sec">01 · Basic Info</div>', unsafe_allow_html=True)
        age = st.slider("Age", 18, 100, 40)
        sex = st.radio("Sex", ["M", "F"], horizontal=True)
        chest_pain = st.selectbox(
            "Chest Pain Type",
            ["ATA", "NAP", "TA", "ASY"],
            help="ATA: Atypical Angina | NAP: Non-Anginal Pain | TA: Typical Angina | ASY: Asymptomatic",
        )

    with tab2:
        st.markdown('<div class="sec">02 · Blood Parameters</div>', unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1:
            resting_bp = st.number_input("Resting BP (mm Hg)", 80, 200, 120)
        with c2:
            cholesterol = st.number_input("Cholesterol (mg/dL)", 100, 600, 200)
        fasting_bs = st.radio(
            "Fasting Blood Sugar > 120 mg/dL",
            [0, 1],
            format_func=lambda x: "Yes" if x == 1 else "No",
            horizontal=True,
        )

    with tab3:
        st.markdown('<div class="sec">03 · Heart Activity</div>', unsafe_allow_html=True)
        resting_ecg = st.selectbox("Resting ECG", ["Normal", "ST", "LVH"])
        max_hr = st.slider("Max Heart Rate", 60, 220, 150)
        exercise_angina = st.radio(
            "Exercise-Induced Angina",
            ["Y", "N"],
            format_func=lambda x: "Yes" if x == "Y" else "No",
            horizontal=True,
        )
        oldpeak = st.slider("Oldpeak (ST Depression)", 0.0, 6.0, 1.0)
        st_slope = st.selectbox("ST Slope", ["Up", "Flat", "Down"])

# ---------- Result panel ----------
with right:
    st.markdown('<div class="console-title">▍ ANALYSIS CONSOLE</div>', unsafe_allow_html=True)
    predict_clicked = st.button("Analyze Risk")

    if predict_clicked:
        # Raw input dictionary (same logic as before)
        raw_input = {
            "Age": age,
            "RestingBP": resting_bp,
            "Cholesterol": cholesterol,
            "FastingBS": fasting_bs,
            "MaxHR": max_hr,
            "Oldpeak": oldpeak,
            "Sex_" + sex: 1,
            "ChestPainType_" + chest_pain: 1,
            "RestingECG_" + resting_ecg: 1,
            "ExerciseAngina_" + exercise_angina: 1,
            "ST_Slope_" + st_slope: 1,
        }

        input_df = pd.DataFrame([raw_input])

        # Fill missing columns with 0
        for col in expected_columns:
            if col not in input_df.columns:
                input_df[col] = 0

        # Reorder columns
        input_df = input_df[expected_columns]

        # Scale + predict
        scaled_input = scaler.transform(input_df)
        prediction = model.predict(scaled_input)[0]

        # Probability (KNN supports predict_proba)
        try:
            risk_prob = float(model.predict_proba(scaled_input)[0][1])
        except Exception:
            risk_prob = None

        level = "high" if prediction == 1 else "low"

        if prediction == 1:
            st.markdown(
                """
<div class="verdict high">
<span class="chip">HIGH RISK</span>
<h2>⚠️ High Risk</h2>
<p>According to the model, your heart disease risk is high. Please consult a doctor.</p>
</div>
                """,
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                """
<div class="verdict low">
<span class="chip">LOW RISK</span>
<h2>✅ Low Risk</h2>
<p>According to the model, your risk is low. Maintain a healthy lifestyle.</p>
</div>
                """,
                unsafe_allow_html=True,
            )

        if risk_prob is not None:
            pct = int(round(min(max(risk_prob, 0.0), 1.0) * 100))
            st.markdown(
                f"""
<div class="gauge-wrap">
<div class="gauge {level}" style="--p:{pct};">
<div class="gauge-in"><b>{pct}%</b><small>RISK PROBABILITY</small></div>
</div>
</div>
                """,
                unsafe_allow_html=True,
            )

        st.markdown(
            f"""
<div class="tiles">
<div class="tile"><b>{age}</b><span>AGE</span></div>
<div class="tile"><b>{resting_bp}</b><span>BP</span></div>
<div class="tile"><b>{cholesterol}</b><span>CHOL.</span></div>
<div class="tile"><b>{max_hr}</b><span>MAX HR</span></div>
</div>
            """,
            unsafe_allow_html=True,
        )

        st.write("")
        with st.expander("📋 Input summary"):
            st.dataframe(input_df.T.rename(columns={0: "Value"}), use_container_width=True)
    else:
        st.markdown(
            """
<div class="idle">
<svg viewBox="0 0 260 60" fill="none" xmlns="http://www.w3.org/2000/svg">
<path stroke="#2ef2c0" stroke-opacity="0.5" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" d="M0 30 H90 L98 30 L106 10 L116 52 L124 30 H260"/>
</svg>
<h3>Awaiting patient data</h3>
<p>Fill in the details on the left, then press <b>Analyze Risk</b>.</p>
</div>
            """,
            unsafe_allow_html=True,
        )

st.markdown(
    '<div class="disclaimer">CardioScan is an educational project and does not provide medical diagnosis.</div>',
    unsafe_allow_html=True,
)
