import streamlit as st
import requests

# Page config
st.set_page_config(page_title="Sleep Quality Predictor", layout="wide")

# Custom CSS for background and styling
st.markdown(
    """
    <style>
    .stApp {
        background-color: #f0f8ff;  /* light blue background */
    }
    .title {
        color: #003366;  /* dark blue title */
        font-size:40px;
        font-weight:bold;
    }
    .result {
        color: #ff6600; /* orange color for prediction */
        font-size:24px;
        font-weight:bold;
        background-color:#fff3e0;
        padding:10px;
        border-radius:10px;
        text-align:center;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown('<div class="title">🛌 Sleep Quality Prediction</div>', unsafe_allow_html=True)
st.markdown("Fill in your information below to predict your sleep quality.")

# Split inputs into two columns
col1, col2 = st.columns(2)

with col1:
    Age = st.slider("Age", 0, 120, 28)
    Gender = st.selectbox("Gender", ["Male", "Female", "Other"])
    Coffee_Intake = st.slider("Coffee Intake (cups/day)", 0.0, 10.0, 3.0)
    Caffeine_mg = st.slider("Caffeine (mg/day)", 0.0, 1000.0, 200.0)
    Sleep_Hours = st.slider("Sleep Hours", 0.0, 24.0, 7.0)
    BMI = st.slider("BMI", 10.0, 50.0, 25.0)
    Heart_Rate = st.slider("Heart Rate (bpm)", 40, 150, 70)

with col2:
    Stress_Level = st.selectbox("Stress Level", ["Low", "Medium", "High"])
    Physical_Activity_Hours = st.slider("Physical Activity Hours/day", 0.0, 24.0, 1.0)
    Health_Issues = st.selectbox("Health Issues", ["None", "Mild", "Moderate", "Severe"])
    Occupation = st.selectbox("Occupation", ["Other", "Healthcare", "Student", "Office", "Service"])
    Smoking = st.slider("Smoking (cigarettes/day)", 0, 50, 0)
    Alcohol_Consumption = st.slider("Alcohol Consumption (drinks/week)", 0, 50, 0)

st.markdown("---")

# Predict button
if st.button("Predict Sleep Quality"):
    data = {
        "Age": Age,
        "Gender": Gender,
        "Coffee_Intake": Coffee_Intake,
        "Caffeine_mg": Caffeine_mg,
        "Sleep_Hours": Sleep_Hours,
        "BMI": BMI,
        "Heart_Rate": Heart_Rate,
        "Stress_Level": Stress_Level,
        "Physical_Activity_Hours": Physical_Activity_Hours,
        "Health_Issues": Health_Issues,
        "Occupation": Occupation,
        "Smoking": Smoking,
        "Alcohol_Consumption": Alcohol_Consumption
    }

    # Send POST request to FastAPI
    try:
        response = requests.post("http://127.0.0.1:8000/predict", json=data)
        result = response.json()
        
        if "prediction" in result:
            pred = result['prediction']
            # Map numeric class to label
            mapping = {0:"Excellent", 1:"Fair", 2:"Good", 3:"Poor"}
            res = mapping.get(pred, "Unknown")
            
            st.markdown(f'<div class="result">🌙 Predicted Sleep Quality: {res}</div>', unsafe_allow_html=True)
        else:
            st.error(f"❌ Error: {result.get('message', 'Unknown error')}")
    except Exception as e:
        st.error(f"⚠️ Request failed: {str(e)}")
