import streamlit as st
import requests

def show():
    # Custom CSS for styling
    st.markdown("""
        <style>
        .footer {
            padding: 40px 20px;
            text-align: center;
        }
        .footer img {
            width: 70px;
            display: block;
            margin: 0 auto 10px;
        }
        .footer .footer-content {
            max-width: 800px;
            margin: 0 auto;
        }
        .footer .footer-left {
            margin: 10px 0;
        }
        .footer .footer-left h3 {
            font-size: 1.5rem;
            margin: 10px 0;
        }
        .footer .footer-left p {
            font-size: 1rem;
            margin: 10px 0;
        }
        .footer .footer-bottom {
            margin-top: 20px;
            font-size: 0.9rem;
            text-align: center;
        }
        .footer .horizontal-line {
            border: 0.5px solid white;
            margin: 20px 0;
        }
        </style>
    """, unsafe_allow_html=True)

    # Header section
    st.title("Contact Us")
    st.subheader("Aorta AI - Web-based Heart Prediction System")

    # Introduction text
    st.markdown("""
    Welcome to Aorta AI's contact page. We value your feedback and inquiries.
    Please fill out the form below, and our team will get back to you as soon as possible.
    """)

    # Initialize session state variables
    if 'form_submitted' not in st.session_state:
        st.session_state.form_submitted = False

    # Check if the form was just submitted
    if st.session_state.form_submitted:
        st.success("Thank you for your message! We will get back to you soon.")
        # Reset the form_submitted state
        st.session_state.form_submitted = False
    
    # Contact form
    with st.form(key='contact_form'):
        name = st.text_input("Full Name")
        email = st.text_input("Email Address")
        subject = st.text_input("Subject")
        message = st.text_area("Message")

        # Submit button
        submit_button = st.form_submit_button(label='Submit')
        
    if submit_button:
        if not name or not email or not message:
            st.error("Please fill out all fields.")
        else:
            form_data = {
                'name': name,
                'email': email,
                'subject': subject,
                'message': message
            }
            # Submit form data to Formspree endpoint
            response = requests.post('https://formspree.io/f/mpwawqyr', data=form_data)

            if response.status_code == 200:
                st.session_state.form_submitted = True
                # Rerun the app to show the success message and clear the form
                st.experimental_rerun()
            else:
                st.error("Oops! Something went wrong. Please try again later.")

if __name__ == '__main__':
    show()