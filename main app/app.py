import streamlit as st
import sqlite3
import hashlib

# Import your other pages
import aortaai
import doctor
import heart
import contact
import wow

st.set_page_config(page_title="AortaAI", page_icon="💖")


# Custom CSS for styling
st.markdown("""
    <style>
    .footer {
        padding: 20px;
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
    @media (max-width: 768px) {
        .footer .footer-left h3 {
            font-size: 1.2rem;
        }
        .footer .footer-left p {
            font-size: 0.9rem;
        }
        .footer .footer-bottom {
            font-size: 0.8rem;
        }
    }
    </style>
""", unsafe_allow_html=True)

# JavaScript to scroll to top and hide sidebar
st.markdown("""
    <script>
    function scrollToTop() {
        window.scrollTo(0, 0);
    }
    </script>
""", unsafe_allow_html=True)

# Database functions
def init_db():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (username TEXT PRIMARY KEY, password TEXT)''')
    conn.commit()
    conn.close()

def get_db_connection():
    return sqlite3.connect('users.db')

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def create_user(username, password):
    conn = get_db_connection()
    c = conn.cursor()
    try:
        c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hash_password(password)))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def authenticate(username, password):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, hash_password(password)))
    result = c.fetchone()
    conn.close()
    return result is not None

# Initialize the database
init_db()

# Streamlit app
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
    st.session_state.sidebar_state = 'collapsed'

if not st.session_state.authenticated:
    st.title("Login / Sign Up")
    
    tab1, tab2 = st.tabs(["Login", "Sign Up"])
    
    with tab1:
        username = st.text_input("Username", key="login_username")
        password = st.text_input("Password", type="password", key="login_password")
        
        if st.button("Login"):
            if authenticate(username, password):
                st.session_state.authenticated = True
                st.session_state.username = username
                st.session_state.current_page = "Home"
                st.session_state.sidebar_state = 'collapsed'
                st.experimental_rerun()
            else:
                st.error("Invalid username or password")
    
    with tab2:
        new_username = st.text_input("New Username", key="signup_username")
        new_password = st.text_input("New Password", type="password", key="signup_password")
        confirm_password = st.text_input("Confirm Password", type="password", key="confirm_password")
        
        if st.button("Sign Up"):
            if new_username and new_password and new_password == confirm_password:
                if create_user(new_username, new_password):
                    st.success("Account created successfully! You can now log in.")
                else:
                    st.error("Username already exists. Please choose a different username.")
            else:
                st.error("Please fill all fields and ensure passwords match.")

else:
    # Create a sidebar for navigation
    with st.sidebar:
        st.title(f"Welcome, {st.session_state.username}")
        
        if st.button("🏠 Home"):
            st.session_state.current_page = "Home"
            st.session_state.sidebar_state = 'collapsed'
            st.experimental_rerun()
        
        if st.button("ℹ️ About Us"):
            st.session_state.current_page = "About Us"
            st.session_state.sidebar_state = 'collapsed'
            st.experimental_rerun()
        
        if st.button("👨‍⚕️ Doctor"):
            st.session_state.current_page = "Doctor"
            st.session_state.sidebar_state = 'collapsed'
            st.experimental_rerun()
        
        if st.button("❤️ General Prediction"):
            st.session_state.current_page = "Heart"
            st.session_state.sidebar_state = 'collapsed'
            st.experimental_rerun()

        if st.button("🤖 Complex Prediction"):
            st.session_state.current_page = "wow"
            st.session_state.sidebar_state = 'collapsed'
            st.experimental_rerun()
        
        if st.button("📞 Contact"):
            st.session_state.current_page = "Contact"
            st.session_state.sidebar_state = 'collapsed'
            st.experimental_rerun()

        # Logout button
        if st.button("🚪 Log out"):
            st.session_state.authenticated = False
            st.session_state.sidebar_state = 'collapsed'
            st.experimental_rerun()

    # Main content area
    main_content = st.container()

    with main_content:
        if st.session_state.current_page == "Home":
            st.title("Welcome to AortaAI")
            st.write("This is the home page of AortaAI. Please select an option from the sidebar to explore our services.")
            st.write("\n")
            st.write("\n")
            st.write("\n")
            st.write("\n")
            st.write("\n")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.info("🩺 Expert Doctors")
                st.write("Our platform connects you with expert doctors specializing in cardiovascular health.")
            with col2:
                st.success("❤️ Heart Health")
                st.write("Learn about maintaining a healthy heart and preventing cardiovascular diseases.")
            with col3:
                st.warning("🤖 AI-Powered")
                st.write("Leveraging artificial intelligence to provide cutting-edge cardiac care solutions.")
            st.write("\n")
            st.write("\n")
            st.write("\n")
            st.write("\n")

        elif st.session_state.current_page == "About Us":
            aortaai.show()

        elif st.session_state.current_page == "Doctor":
            doctor.show()

        elif st.session_state.current_page == "Heart":
            heart.show()
        
        elif st.session_state.current_page == "wow":
            wow.show()

        elif st.session_state.current_page == "Contact":
            contact.show()

    # Footer
    st.markdown("""
        <div class="footer">
            <div class="footer-content">
                <div class="footer-left">
                    <h3>Every Heartbeat Matters</h3>
                    <p>Take the first step towards understanding your heart health with our AI-powered platform. Gain insights and early detection possibilities to empower your well-being. Start your journey today.</p>
                </div>
            </div>
            <hr class="horizontal-line">
            <div class="footer-bottom">
                &copy; 2024 Aorta AI, Inc. All Rights Reserved
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Scroll to top when page changes
    st.markdown('<script>scrollToTop();</script>', unsafe_allow_html=True)

# Set sidebar state
st.sidebar.markdown(f"""
    <script>
        var sidebar = window.parent.document.querySelector('[data-testid="stSidebar"]');
        sidebar.setAttribute('data-collapsed', '{st.session_state.sidebar_state}');
    </script>
""", unsafe_allow_html=True)