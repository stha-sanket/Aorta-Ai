import streamlit as st
import pickle
import numpy as np
import matplotlib.pyplot as plt
def show():
    # Load the pre-trained model
    with open('model_and_scaler.pkl', 'rb') as file:
        content = pickle.load(file)

    model = content['model']

    # Title of the web app
    st.title("Heart Disease Prediction")

    # Collect user input features
    st.header("Enter the following details:")

    age = st.number_input("Age", min_value=1, max_value=120, value=50, help="Enter your age.")
    sex = st.selectbox("Sex", options=["Male", "Female"], help="Select your sex.")
    cp = st.selectbox("Chest Pain Type", options=[
        "Typical Angina",
        "Atypical Angina",
        "Non-anginal Pain",
        "Asymptomatic"
    ], help="Select the type of chest pain you experience.")
    trestbps = st.number_input("Resting Blood Pressure (mm Hg)", min_value=80, max_value=200, value=120, help="Enter your resting blood pressure.")
    chol = st.number_input("Serum Cholesterol (mg/dl)", min_value=100, max_value=600, value=200, help="Enter your serum cholesterol level.")
    fbs_input = st.number_input("Fasting Blood Sugar (mg/dl)", min_value=50, max_value=300, value=100, help="Enter your fasting blood sugar level.")
    restecg = st.selectbox("Resting Electrocardiographic Results", options=[
        "Normal",
        "Having ST-T wave abnormality",
        "Showing probable or definite left ventricular hypertrophy"
    ], help="Select your resting electrocardiographic results.")
    thalach = st.number_input("Maximum Heart Rate Achieved", min_value=60, max_value=220, value=150, help="Enter your maximum heart rate achieved.")
    exang = st.selectbox("Exercise Induced Angina", options=["No", "Yes"], help="Do you experience exercise induced angina?")
    oldpeak = st.number_input("ST Depression Induced by Exercise", min_value=0.0, max_value=6.0, value=1.0, step=0.1, help="Enter your ST depression induced by exercise relative to rest.")
    slope = st.selectbox("Slope of the Peak Exercise ST Segment", options=[
        "Upsloping",
        "Flat",
        "Downsloping"
    ], help="Select the slope of the peak exercise ST segment.")

    # Convert categorical options to their respective values
    sex = 1 if sex == "Male" else 0
    cp_dict = {
        "Typical Angina": 0,
        "Atypical Angina": 1,
        "Non-anginal Pain": 2,
        "Asymptomatic": 3
    }
    cp = cp_dict[cp]

    fbs = 1 if fbs_input >= 120 else 0

    restecg_dict = {
        "Normal": 0,
        "Having ST-T wave abnormality": 1,
        "Showing probable or definite left ventricular hypertrophy": 2
    }
    restecg = restecg_dict[restecg]

    exang = 1 if exang == "Yes" else 0

    slope_dict = {
        "Upsloping": 0,
        "Flat": 1,
        "Downsloping": 2
    }
    slope = slope_dict[slope]

    # Create a feature array with only the necessary features
    features = np.array([[age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope]])

    # Initialize session state variables
    if 'prediction_done' not in st.session_state:
        st.session_state.prediction_done = False

    # Add a submit button
    if st.button("Submit"):
        # Predict using the model
        prediction = model.predict(features)
        prediction_proba = model.predict_proba(features)
        
        # Update session state
        st.session_state.prediction_done = True
        
        # Display the prediction
        if prediction[0] == 1:
            st.subheader("High Risk of Heart Disease")
            st.write("The model predicts that you have a high risk of heart disease.")
        else:
            st.subheader("Low Risk of Heart Disease")
            st.write("The model predicts that you have a low risk of heart disease.")
        
        st.write(f"Prediction probability: {prediction_proba[0][1]*100:.2f}% for high risk, {prediction_proba[0][0]*100:.2f}% for low risk.")
        
        # Plot the prediction probabilities
        labels = ['High Risk', 'Low Risk']
        sizes = [prediction_proba[0][1], prediction_proba[0][0]]
        
        fig, ax = plt.subplots()
        ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140, colors=['#ff9999','#66b3ff'])
        ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        
        st.pyplot(fig)

    # Display recommendations if prediction is done
    if st.session_state.prediction_done:
        st.header("Recommendation for Better Health")
        
        recommendations = []
        
        # Recommendations based on input values
        if cp == 0:
            recommendations.append("Typical Angina may indicate a more serious heart condition. Consult a healthcare professional for further evaluation.")
        elif cp == 1:
            recommendations.append("Atypical Angina could be a sign of coronary artery disease. Consider getting a thorough checkup.")
        elif cp == 2:
            recommendations.append("Non-anginal Pain might still require evaluation to rule out heart disease. Consult with your doctor.")
        elif cp == 3:
            recommendations.append("Asymptomatic conditions can still pose risks. Regular checkups are recommended to ensure heart health.")

        if trestbps > 140:
            recommendations.append("High resting blood pressure increases heart disease risk. Consider lifestyle changes such as reducing salt intake and increasing physical activity.")
        
        if chol > 240:
            recommendations.append("High serum cholesterol levels can lead to heart disease. Focus on a diet low in saturated fats and high in fiber.")
        
        if fbs_input >= 120:
            recommendations.append("Elevated fasting blood sugar levels can indicate a risk of diabetes. Consider dietary adjustments and regular monitoring.")
        
        if restecg == 1:
            recommendations.append("ST-T wave abnormalities can suggest heart strain. Further evaluation by a healthcare provider may be necessary.")
        elif restecg == 2:
            recommendations.append("Showing probable or definite left ventricular hypertrophy may indicate heart muscle issues. A specialist consultation is advised.")
        
        if thalach < 120:
            recommendations.append("A low maximum heart rate achieved may be due to poor cardiovascular fitness. Incorporate regular aerobic exercise into your routine.")
        
        if exang == 1:
            recommendations.append("Exercise-induced angina can be a sign of underlying heart disease. Discuss with a healthcare provider for appropriate management.")
        
        if oldpeak > 1.0:
            recommendations.append("ST depression induced by exercise might indicate a significant heart issue. Consider a detailed cardiac assessment.")
        
        if slope == 0:
            recommendations.append("Upsloping ST segment can be associated with exercise-induced angina. Monitor your symptoms and consult your doctor if necessary.")
        elif slope == 1:
            recommendations.append("Flat ST segment may indicate a less pronounced cardiac issue, but should still be evaluated by a healthcare provider.")
        elif slope == 2:
            recommendations.append("Downsloping ST segment during exercise can be a sign of significant heart disease. Seek medical advice for a comprehensive evaluation.")

        if recommendations:
            for rec in recommendations:
                st.write(f"- {rec}")
        else:
            st.write("No specific recommendations based on the provided input.")

if __name__ == '__main__':
    show()