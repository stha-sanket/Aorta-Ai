import streamlit as st
import pandas as pd
import pickle
from sklearn.preprocessing import StandardScaler, LabelEncoder
import altair as alt
import os

def load_model():
    # Use a relative path or environment variable for the model path
    script_dir = os.path.dirname(__file__)
    model_path = os.path.join(script_dir, 'best_heart_disease_model.pkl')
    with open(model_path, 'rb') as f:
        return pickle.load(f)

# Load the model
model = load_model()

# Load encoders and scaler
label_encoders = {
    'Smoking': LabelEncoder().fit(['Yes', 'No']),
    'AlcoholDrinking': LabelEncoder().fit(['Yes', 'No']),
    'Stroke': LabelEncoder().fit(['Yes', 'No']),
    'DiffWalking': LabelEncoder().fit(['Yes', 'No']),
    'Sex': LabelEncoder().fit(['Male', 'Female']),
    'Race': LabelEncoder().fit(['White', 'Black', 'Asian', 'American Indian/Alaskan Native', 'Other']),
    'Diabetic': LabelEncoder().fit(['Yes', 'No']),
    'PhysicalActivity': LabelEncoder().fit(['Yes', 'No']),
    'GenHealth': LabelEncoder().fit(['Poor', 'Fair', 'Good', 'Very good', 'Excellent']),
    'Asthma': LabelEncoder().fit(['Yes', 'No']),
    'AgeCategory': LabelEncoder().fit(['18-24', '25-29', '30-34', '35-39', '40-44', '45-49',
                                       '50-54', '55-59', '60-64', '65-69', '70-74', '75-79', '80 or older'])
}
scaler = StandardScaler()

# Function to get age category
def get_age_category(age):
    if age <= 24:
        return '18-24'
    elif age <= 29:
        return '25-29'
    elif age <= 34:
        return '30-34'
    elif age <= 39:
        return '35-39'
    elif age <= 44:
        return '40-44'
    elif age <= 49:
        return '45-49'
    elif age <= 54:
        return '50-54'
    elif age <= 59:
        return '55-59'
    elif age <= 64:
        return '60-64'
    elif age <= 69:
        return '65-69'
    elif age <= 74:
        return '70-74'
    elif age <= 79:
        return '75-79'
    else:
        return '80 or older'

# Function to generate recommendations based on user input
def generate_recommendations(user_data):
    recommendations = []

    if user_data['Smoking'] == 1:
        recommendations.append("Quitting smoking can significantly lower your risk of heart disease. Consider seeking support from healthcare professionals or smoking cessation programs.")

    if user_data['AlcoholDrinking'] == 1:
        recommendations.append("Reducing alcohol consumption can help lower your risk of heart disease. Aim for moderation and consult a healthcare provider for personalized advice.")

    if user_data['PhysicalHealth'] > 5:
        recommendations.append("If you experienced poor physical health for more than 5 days in the past month, it's important to engage in regular physical activity and consult with a healthcare provider for a comprehensive evaluation.")

    if user_data['MentalHealth'] > 5:
        recommendations.append("Managing stress and mental health is crucial for overall well-being. Consider mindfulness practices, therapy, or counseling to improve your mental health.")

    if user_data['DiffWalking'] == 1:
        recommendations.append("Difficulty walking may indicate underlying health issues. Consult with a healthcare professional to explore suitable exercises and interventions.")

    if user_data['Diabetic'] == 1:
        recommendations.append("If you are diabetic, it is essential to monitor and manage your blood sugar levels carefully. Follow your healthcare provider's advice on diet, medication, and lifestyle changes.")

    if user_data['PhysicalActivity'] == 0:
        recommendations.append("Incorporating regular physical activity into your routine can improve heart health. Aim for at least 150 minutes of moderate exercise or 75 minutes of vigorous exercise per week.")

    if user_data['GenHealth'] in [0, 1]:  # Poor or Fair
        recommendations.append("Improving overall health through a balanced diet, regular exercise, and regular check-ups can enhance your general health status. Consult with a healthcare provider for personalized health strategies.")

    if user_data['SleepTime'] < 7:
        recommendations.append("Aiming for 7-8 hours of quality sleep per night can improve heart health and overall well-being. Consider establishing a regular sleep routine and addressing any sleep issues.")

    if user_data['Asthma'] == 1:
        recommendations.append("If you have asthma, managing your symptoms effectively with proper medication and avoiding known triggers is crucial. Regular follow-ups with your healthcare provider are recommended.")

    # Add general lifestyle recommendations
    recommendations.append("Maintaining a healthy weight, eating a balanced diet rich in fruits, vegetables, and whole grains, and reducing intake of saturated fats, cholesterol, and sodium can support heart health.")

    recommendations.append("Regular health check-ups, including blood pressure and cholesterol screenings, are essential for early detection and prevention of heart disease. Discuss with your healthcare provider about appropriate screening schedules.")

    return recommendations

# Function to display the Streamlit app
def show():
    st.title('Heart Disease Prediction')

    st.header('User Input')
    st.write("Please fill out the following information to get your heart disease risk prediction and personalized recommendations.")

    # Collect user inputs with descriptions
    bmi = st.number_input("Enter your BMI:", min_value=0.0, step=0.1, help="Body Mass Index, a measure of body fat based on height and weight.")
    smoking = st.selectbox("Do you smoke?", options=['Yes', 'No'], help="Select 'Yes' if you currently smoke, 'No' if you don't.")
    alcohol = st.selectbox("Do you drink alcohol?", options=['Yes', 'No'], help="Select 'Yes' if you consume alcohol, 'No' if you don't.")
    stroke = st.selectbox("Have you had a stroke?", options=['Yes', 'No'], help="Select 'Yes' if you have experienced a stroke, 'No' if you haven't.")
    physical_health = st.number_input("Number of days physical health was not good in the past 30 days:", min_value=0, step=1, help="Number of days you felt physically unwell in the past month.")
    mental_health = st.number_input("Number of days mental health was not good in the past 30 days:", min_value=0, step=1, help="Number of days you felt mentally unwell in the past month.")
    diff_walking = st.selectbox("Do you have difficulty walking?", options=['Yes', 'No'], help="Select 'Yes' if you have trouble walking, 'No' if you don't.")
    sex = st.selectbox("Enter your sex:", options=['Male', 'Female'], help="Select your gender.")
    age = st.slider("Enter your age:", min_value=18, max_value=100, help="Slide to select your age.")
    race = st.selectbox("Enter your race:", options=['White', 'Black', 'Asian', 'American Indian/Alaskan Native', 'Other'], help="Select your race.")
    diabetic = st.selectbox("Are you diabetic?", options=['Yes', 'No'], help="Select 'Yes' if you have diabetes, 'No' if you don't.")
    physical_activity = st.selectbox("Do you engage in physical activity?", options=['Yes', 'No'], help="Select 'Yes' if you exercise regularly, 'No' if you don't.")
    gen_health = st.selectbox("General health:", options=['Poor', 'Fair', 'Good', 'Very good', 'Excellent'], help="Select your general health status.")
    sleep_time = st.number_input("Average hours of sleep per night:", min_value=0, step=1, help="Number of hours you sleep on average each night.")
    asthma = st.selectbox("Do you have asthma?", options=['Yes', 'No'], help="Select 'Yes' if you have asthma, 'No' if you don't.")

    if st.button('Submit'):
        # Encode inputs
        user_data = {
            'BMI': bmi,
            'Smoking': label_encoders['Smoking'].transform([smoking])[0],
            'AlcoholDrinking': label_encoders['AlcoholDrinking'].transform([alcohol])[0],
            'Stroke': label_encoders['Stroke'].transform([stroke])[0],
            'PhysicalHealth': physical_health,
            'MentalHealth': mental_health,
            'DiffWalking': label_encoders['DiffWalking'].transform([diff_walking])[0],
            'Sex': label_encoders['Sex'].transform([sex])[0],
            'AgeCategory': label_encoders['AgeCategory'].transform([get_age_category(age)])[0],
            'Race': label_encoders['Race'].transform([race])[0],
            'Diabetic': label_encoders['Diabetic'].transform([diabetic])[0],
            'PhysicalActivity': label_encoders['PhysicalActivity'].transform([physical_activity])[0],
            'GenHealth': label_encoders['GenHealth'].transform([gen_health])[0],
            'SleepTime': sleep_time,
            'Asthma': label_encoders['Asthma'].transform([asthma])[0],
        }

        # Convert to DataFrame
        input_data = pd.DataFrame([user_data])

        # Normalize numerical columns
        numerical_columns = ['BMI', 'PhysicalHealth', 'MentalHealth', 'SleepTime']
        input_data[numerical_columns] = scaler.fit_transform(input_data[numerical_columns])

        # Make prediction
        prediction = model.predict(input_data)
        prediction_prob = model.predict_proba(input_data)[0]

        # Display prediction results
        classes = ['No Heart Disease', 'Heart Disease']
        st.subheader('Prediction Results')
        st.write(f"No Heart Disease: Probability = {prediction_prob[0]:.4f} ({prediction_prob[0] * 100:.2f}%)")
        st.write(f"Heart Disease: Probability = {prediction_prob[1]:.4f} ({prediction_prob[1] * 100:.2f}%)")

        # Plotting prediction probabilities using Altair
        st.subheader('Prediction Visualization')
        prob_df = pd.DataFrame({
            'Condition': classes,
            'Probability': prediction_prob,
            'Color': ['grey', 'red']
        })

        chart = alt.Chart(prob_df).mark_bar().encode(
            x='Condition',
            y='Probability',
            color=alt.Color('Color', scale=None)
        ).properties(width=alt.Step(80))  # controls bar width

        st.altair_chart(chart)

        # Generate recommendations
        recommendations = generate_recommendations(user_data)

        st.subheader('Recommendations for Better Health')
        if recommendations:
            for recommendation in recommendations:
                st.write(f"- {recommendation}")
        else:
            st.write("No specific recommendations based on the provided data.")

# Main function to run Streamlit app
def main():
    show()

if __name__ == "__main__":
    main()
