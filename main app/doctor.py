import streamlit as st
import base64
import requests

# Sample availability data for physical and online consultations
availability = {
    "Dr. DANIEL SMITH, MBBS, MD": {
        "physical": ["Monday 10:00 AM", "Wednesday 2:00 PM", "Friday 11:00 AM"],
        "online": ["Tuesday 9:00 AM", "Thursday 3:00 PM", "Saturday 10:00 AM"]
    },
    "Dr. JENNIE RUBY JANE, MBBS, MD": {
        "physical": ["Monday 2:00 PM", "Wednesday 10:00 AM", "Friday 1:00 PM"],
        "online": ["Tuesday 11:00 AM", "Thursday 1:00 PM", "Saturday 9:00 AM"]
    },
    "Dr. JOHN DOE, MBBS, MD": {
        "physical": ["Monday 2:00 PM", "Wednesday 10:00 AM", "Friday 1:00 PM"],
        "online": ["Tuesday 11:00 AM", "Thursday 1:00 PM", "Saturday 9:00 AM"]
    },
    "Dr. PARK THOMAS, MBBS, MD": {
        "physical": ["Tuesday 11:00 AM", "Thursday 1:00 PM", "Saturday 9:00 AM"],
        "online": ["Monday 2:00 PM", "Wednesday 10:00 AM", "Friday 1:00 PM"]
    },
    "Dr. ASHLESHA SHRESTHA, MBBS, MD": {
        "physical": ["Monday 9:00 AM", "Wednesday 1:00 PM", "Friday 3:00 PM"],
        "online": ["Tuesday 2:00 PM", "Thursday 10:00 AM", "Saturday 11:00 AM"]
    },
    "Dr. JOSEPH WILL, MBBS, MD": {
        "physical": ["Tuesday 2:00 PM", "Thursday 10:00 AM", "Saturday 11:00 AM"],
        "online": ["Monday 9:00 AM", "Wednesday 1:00 PM", "Friday 3:00 PM"]
    }
}

def show():
    # Custom CSS for styling
    st.markdown("""
        <style>
        .doctor-card {
            width: 300px;
            border: 1px solid #ddd;
            border-radius: 10px;
            padding: 20px;
            text-align: center;
            box-shadow: 0 0 10px rgba(0,0,0,0.1);
            background-color: #fff;
            margin-bottom: 20px;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            height: 350px;
        }
        .doctor-image {
            border-radius: 50%;
            width: 150px;
            height: 150px;
            object-fit: cover;
            margin: 0 auto 15px;
        }
        .doctor-info {
            font-size: 14px;
            color: #333;
            font-family: 'Arial', sans-serif;
        }
        .doctor-name {
            font-weight: bold;
            font-size: 18px;
            margin-top: 10px;
            color: #ff0000;
        }
        .doctor-position {
            color: #555;
            margin-top: 5px;
            font-size: 13px;
        }
        .doctor-nmc {
            color: #888;
            margin-top: 5px;
            font-size: 12px;
        }
        .why-book {
            text-align: center;
            padding: 20px;
        }
        .reasons-container {
            display: flex;
            flex-wrap: wrap;
            justify-content: center;
            margin-top: 20px;
        }
        .reason {
            text-align: center;
            margin: 10px;
            flex: 1 1 300px;
            max-width: 300px;
        }
        .reason-icon {
            font-size: 50px;
        }
        @media (max-width: 600px) {
            .reason {
                flex: 1 1 100%;
            }
        }
        </style>
    """, unsafe_allow_html=True)

    # App title
    st.title("Know Your Doctor")
    st.write("\n")
    st.write("\n")

    # Doctors' Information
    doctors = [
        {"name": "Dr. DANIEL SMITH, MBBS, MD", "position": "CONSULTANT CARDIOLOGIST & HEAD OF DEPARTMENT", "nmc": "NMC NO. 5565", "image": "doc5.jpg"},
        {"name": "Dr. JENNIE RUBY JANE, MBBS, MD", "position": "CONSULTANT CARDIOLOGIST & ASSOCIATE PROFESSOR", "nmc": "NMC NO. 6268", "image": "doc2.jpg"},
        {"name": "Dr. JOHN DOE, MBBS, MD", "position": "SR. CONSULTANT CARDIOLOGIST", "nmc": "NMC NO. 1654", "image": "doc3.jpg"},
        {"name": "Dr. PARK THOMAS, MBBS, MD", "position": "CARDIOLOGIST", "nmc": "NMC NO. 2225", "image": "doc4.jpg"},
        {"name": "Dr. ASHLESHA SHRESTHA, MBBS, MD", "position": "CARDIOLOGIST", "nmc": "NMC NO. 8198", "image": "doc1.jpg"},
        {"name": "Dr. JOSEPH WILL, MBBS, MD", "position": "CARDIOLOGIST", "nmc": "NMC NO. 3579", "image": "doc6.jpg"},
    ]

    # Function to encode images to base64
    def get_image_base64(image_path):
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode()

    # Displaying doctors in a grid layout with two columns
    for i in range(0, len(doctors), 2):
        cols = st.columns(2)
        for j in range(2):
            if i + j < len(doctors):
                doctor = doctors[i + j]
                with cols[j]:
                    image_base64 = get_image_base64(doctor['image'])
                    st.markdown(f"""
                        <div class="doctor-card">
                            <div>
                                <img src="data:image/jpeg;base64,{image_base64}" class="doctor-image" alt="{doctor['name']}">
                                <div class="doctor-info">
                                    <div class="doctor-name">{doctor['name']}</div>
                                    <div class="doctor-position">{doctor['position']}</div>
                                    <div class="doctor-nmc">{doctor['nmc']}</div>
                                </div>
                            </div>
                        </div>
                    """, unsafe_allow_html=True)

    st.write("\n")
    st.write("\n")

    # New section for booking a doctor/consultant
    st.header("Book a doctor")
    # Dropdowns for selecting doctor and appointment type
    doctor_names = list(availability.keys())
    selected_doctor = st.selectbox("Select a doctor:", doctor_names)
    appointment_type = st.selectbox("Select Appointment Type:", ["Physical", "Online"])

    # Display availability based on the selected appointment type
    if selected_doctor and appointment_type:
        appointment_key = "physical" if appointment_type == "Physical" else "online"
        available_slots = availability[selected_doctor][appointment_key]
        
        if available_slots:
            selected_slot = st.selectbox("Choose a time slot:", available_slots, key=f"slot_{selected_doctor}")
            user_email = st.text_input("Enter your email address:", key=f"email_{selected_doctor}")
            
            if st.button("Confirm Booking"):
                if user_email:
                    response = requests.post(
                        "https://formspree.io/f/mpwawqyr",
                        data={"doctor": selected_doctor, "appointment_type": appointment_type, "time_slot": selected_slot, "email": user_email}
                    )
                    if response.status_code == 200:
                        # Update availability to remove the booked slot
                        availability[selected_doctor][appointment_key].remove(selected_slot)
                        
                        # Notify user of successful booking
                        st.success(f"Appointment booked with {selected_doctor} for {selected_slot}")
                    else:
                        st.warning("Failed to send booking information. Please try again.")
                else:
                    st.warning("Please enter your email address.")
        else:
            st.warning("Doctor not available for the selected appointment type. Please choose another doctor or appointment type.")

    st.write("\n")
    st.write("\n")

    # Why Book An Appointment section (mobile-responsive)
    st.markdown("""
        <div class="why-book">
            <h2>Why Book An Appointment Through Aorta-AI?</h2>
            <p>Book An Appointment Online With Aorta-AI Without A Hectic Process.</p>
            <div class="reasons-container">
                <div class="reason">
                    <div class="reason-icon">⏳</div>
                    <h4>Save Time</h4>
                    <p>Avoid Waiting With A Long Queue & Book An Appointment Instantly.</p>
                </div>
                <div class="reason">
                    <div class="reason-icon">💸</div>
                    <h4>Save Money</h4>
                    <p>Get Special Discount Offers On Appointment Booking With Aorta-AI.</p>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    st.write("\n")
    # Footer

if __name__ == "__main__":
    show()