import streamlit as st
from PIL import Image
import base64
import requests

def show():
    # Function to create circular images
    def get_image_with_circle(image_path):
        with open(image_path, "rb") as image_file:
            base64_image = base64.b64encode(image_file.read()).decode()
        return f"""
            <div style="display: flex; justify-content: center; align-items: center; margin-bottom: 20px;">
                <img src="data:image/jpeg;base64,{base64_image}" style="border-radius: 50%; width: 150px; height: 150px; object-fit: cover;"/>
            </div>
        """

    # Load the project image
    project_image = Image.open("aorta.png")

    # App title and description
    st.title("Aorta-AI")
    st.write("###### An AI Based Heart Disease Prediction")

    # Project Section
    st.header("Our Project")
    col1, col2 = st.columns([1, 2])

    with col1:
        st.image(project_image, use_column_width=True)

    with col2:
        st.subheader("An AI Based Heart Disease Prediction")
        st.write("""
            Are you concerned about your heart but lack access to a doctor? Our AI-Powered platform offers accessible heart prediction, using ML to analyze data and assess your risk. While not a replacement for professional medical advice, we provide a valuable first step towards understanding your heart health, empowering you with knowledge and early detection possibilities. Take control of your well-being and explore the potential of AI in preventative heart care today.
        """)

    st.write("\n\n\n")
    st.write("\n\n\n")
    st.write("\n\n\n")

    # Meet Our Team Section
    st.header("Meet Our Team")
    st.write("We are a group of passionate individuals dedicated to creating a positive impact in the field of heart health. Our team consists of people who are committed to improving the lives of individuals with heart health.")
    st.write("\n")
    st.write("\n")
    team_members = [
        ("Sanket Shrestha", "sanket.jpeg"),
        ("Riya Shrestha", "Riya.jpg"),
    ]

    # Display team members with circular images in the center
    cols = st.columns(2)  # Change to 2 columns

    for idx, member in enumerate(team_members):
        name, image_path = member
        with cols[idx % 2]:  # Use modulo to distribute members evenly in the columns
            st.markdown(get_image_with_circle(image_path), unsafe_allow_html=True)
            st.markdown(f"<div style='text-align: center;'>{name}</div>", unsafe_allow_html=True)

    st.write("\n\n\n\n\n")
    st.write("\n\n\n")
    st.write("\n\n\n")
    st.write("\n\n\n")

    # Newsletter Subscription Section
    st.header("Keep Up To Date With Heart Health Tips, & Latest News")
    st.write("\n\n\n")
    with st.form("subscription_form"):
        first_name = st.text_input("First Name")
        email = st.text_input("Email Address")
        # Submit button
        submit_button = st.form_submit_button(label="Subscribe")

        if submit_button:
            # Send data to Formspree
            response = requests.post(
                "https://formspree.io/f/mkgwnedk",
                data={"first_name": first_name, "email": email}
            )
            if response.status_code == 200:
                st.success("Thank you for subscribing!")
            else:
                st.error("Oops! Something went wrong. Please try again later.")

    st.write("\n\n\n\n\n\n")
    st.write("\n\n\n")

if __name__ == "__main__":
    show()
