import streamlit as st
import requests
import plotly.graph_objects as go

st.title("Heart Disease Prediction")


st.sidebar.header("Enter Patient Information")


age = st.sidebar.number_input("Age", min_value=10, max_value=80, step=1)
sex = st.sidebar.radio("Sex", options=["Female", "Male"])
resting_bp = st.sidebar.number_input("Resting Blood Pressure", min_value=80, max_value=200, step=1)
cholesterol = st.sidebar.number_input("Cholesterol Level", min_value=100, max_value=400, step=1)
fasting_bs = st.sidebar.radio("Fasting Blood Sugar > 120 mg/dl", options=["False", "True"])
resting_ecg = st.sidebar.radio(
    "Resting ECG",
    options=["Normal", "ST-T Wave Abnormality", "Left Ventricular Hypertrophy"]
)
max_heart_rate = st.sidebar.number_input("Maximum Heart Rate Achieved", min_value=60, max_value=220, step=1)
exercise_angina = st.sidebar.radio("Exercise-Induced Angina", options=["False", "True"])
oldpeak = st.sidebar.number_input("Old Peak (ST depression induced by exercise)", min_value=0.0, max_value=6.0, step=0.1, format="%.1f")
slope = st.sidebar.radio(
    "Slope of the Peak Exercise ST Segment",
    options=["Upsloping", "Flat", "Downsloping"]
)
major_vessels = st.sidebar.number_input("Number of Major Vessels (colored by fluoroscopy)", min_value=0, max_value=4, step=1)
thalassemia = st.sidebar.radio(
    "Thalassemia",
    options=["Normal", "Fixed Defect", "Reversible Defect"]
)
chest_pain_type = st.sidebar.number_input("Chest Pain Type (0=Asymptomatic, 1=Atypical Angina, etc.)", min_value=0, max_value=3, step=1)


if st.sidebar.button("Predict"):
    input_data = {
        "age": age,
        "sex": 1 if sex == "Male" else 0,
        "resting_bp": resting_bp,
        "cholesterol": cholesterol,
        "fasting_bs": 1 if fasting_bs == "True" else 0,
        "resting_ecg": ["Normal", "ST-T Wave Abnormality", "Left Ventricular Hypertrophy"].index(resting_ecg),
        "max_heart_rate": max_heart_rate,
        "exercise_angina": 1 if exercise_angina == "True" else 0,
        "oldpeak": oldpeak,
        "slope": ["Upsloping", "Flat", "Downsloping"].index(slope),
        "major_vessels": major_vessels,
        "thalassemia": ["Normal", "Fixed Defect", "Reversible Defect"].index(thalassemia),
        "chest_pain_type": chest_pain_type,
    }

    backend_url = "https://heart-disease-prediction-backend.onrender.com/predict"  
    response = requests.post(backend_url, json=input_data)

    if response.status_code == 200:
        result = response.json()
        st.success(f"Prediction: {result['result']}")

        st.header("The Analysis of Patient info")

        features = ["Age", "Resting BP", "Cholesterol", "Max Heart Rate", "Old Peak", "Major Vessels"]
        input_values = [age, resting_bp, cholesterol, max_heart_rate, oldpeak, major_vessels]
        good_ranges = [50, 120, 200, 180, 1.0, 2]
        max_ranges = [80, 200, 400, 220, 6.0, 4]

        fig = go.Figure()

       
        fig.add_trace(go.Scatter(
            x=features,
            y=good_ranges,
            mode='lines+markers',
            line=dict(color='green'),
            marker=dict(size=8),
            name='Good Range'
        ))


        fig.add_trace(go.Scatter(
            x=features,
            y=max_ranges,
            mode='lines+markers',
            line=dict(color='red'),
            marker=dict(size=8),
            name='Max Range'
        ))

        fig.add_trace(go.Scatter(
            x=features,
            y=input_values,
            mode='lines+markers',
            line=dict(color='black'),
            marker=dict(size=10),
            name='Your Input'
        ))

        
        fig.update_layout(
            title="Patient Info",
            xaxis_title="Features",
            yaxis_title="Values",
            legend_title="Legend",
            template="plotly_white"
        )

        
        st.plotly_chart(fig)

    else:
        st.error("Error: Unable to process the prediction.")
