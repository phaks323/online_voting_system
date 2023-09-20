
import streamlit as st
import cv2
import face_recognition as frg
import yaml 
import psycopg2
from utils import recognize, build_dataset
import subprocess
import os
import random
import re
# Path: code\app.py

st.set_page_config(layout="wide")
#Config
cfg = yaml.load(open('config.yaml','r'),Loader=yaml.FullLoader)
PICTURE_PROMPT = cfg['INFO']['PICTURE_PROMPT']
WEBCAM_PROMPT = cfg['INFO']['WEBCAM_PROMPT']



def is_valid_id_number(id_number):
    # ID Number validation: Should have exactly 13 characters
    return len(id_number) == 13

def is_valid_email(email):
    # Email validation using regular expression
    email_pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    return re.match(email_pattern, email)


def is_valid_username(username):
    # Username validation: Should have a combination of characters and numbers
    return bool(re.match(r"^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]+$", username))

def is_valid_password(password):
    # Password validation: 8 or more characters, at least one digit, one uppercase, one lowercase, and one special character
    return bool(re.match(r"^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[@$!%^*?&()-_=+[\]{}|;:'\",.<>/?])[A-Za-z\d@$!%^*?&()-_=+[\]{}|;:'\",.<>/?]{8,}$", password))

personal_info = {}
def send_otp(phone_number, otp):
    # Set up your Twilio account credentials
    account_sid = "YOUR_TWILIO_ACCOUNT_SID"
    auth_token = "YOUR_TWILIO_AUTH_TOKEN"
    twilio_phone_number = "YOUR_TWILIO_PHONE_NUMBER"

    client = client(account_sid, auth_token)

    # Send the OTP via SMS to the user's phone number
    message = client.messages.create(
        body=f"Your OTP for password reset is: {otp}",
        from_=twilio_phone_number,
        to=phone_number
    )

def login_page():
    st.title("Face Recognition App")
    st.write(WEBCAM_PROMPT)

    id_number = st.text_input("ID Number", max_chars=13)
    password = st.text_input("Password", type="password")
    
    col1, col2 = st.columns(2)
    
    if col2.button("ForgotPassword"):
        reset_method = st.radio("Reset Method:", ("Email", "Phone Number"))

        if reset_method == "Email":
            email = st.text_input("Please enter your registered email")
            if email and is_valid_email(email):
                # Add your logic here to send the reset link to the user's email
                # After sending the reset link, show a success message to the user
                st.success(f"An email with password reset instructions has been sent to {email}.")
                st.write("Please check your email and follow the instructions to reset your password.")
            elif email:
                st.warning("Invalid email address. Please enter a valid email.")
        else:  # Reset method is Phone Number
            phone_number = st.text_input("Please enter your registered phone number")
            if phone_number and len(phone_number) == 10 and phone_number.isdigit():
                # Generate a random 6-digit OTP
                otp = str(random.randint(100000, 999999))
                # Add your logic to send the OTP to the user's phone number
                send_otp(phone_number, otp)
                st.success("An OTP has been sent to your registered phone number.")
                otp_input = st.text_input("Please enter the OTP to reset your password.")
                # Here, you can add your logic to verify the OTP and reset the password accordingly
                # For example, you can check if the OTP entered by the user matches the generated OTP
                # If it matches, you can proceed with the password reset process
                # You may use a button to trigger the password reset after verifying the OTP.
            elif phone_number:
                st.warning("Invalid phone number. Please enter a valid 10-digit number.")
        
    # Create the "LogIn" button
    login_button = col1.button("LogIn")
    
    # Always open the webcam
    cam = cv2.VideoCapture(0)
    cam.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    
    FRAME_WINDOW = st.image([])
    
    TOLERANCE = 0.4
    login_successful = False  # Flag to track login status
    
    while not login_successful:
        ret, frame = cam.read()
        if not ret:
            st.error("Failed to capture frame from the camera")
            st.info("Please turn off the other app using the camera and restart this app")
            st.stop()
        image, name, id = recognize(frame, TOLERANCE)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        FRAME_WINDOW.image(image)  
        
        # Check if id_number is not 'Unknown' before comparing
        if login_button:
            if id_number != 'Unknown' and str(id_number) == str(id) and name == name:
                st.success("Face match found. Access granted.")
                st.success("Successful logged in")
                st.write('Redirecting to dashboard...')
                
                subprocess.Popen(['streamlit', 'run', 'Voting_page.py'])

                # Exit the current script (login page)
                os._exit(0)  # Stop rendering the login page
                
            else:
                st.success("Failed to login")
                break
    
    

        # with st.sidebar.form(key='my_form'):
        #     st.title("Developer Section")
        #     submit_button = st.form_submit_button(label='REBUILD DATASET')
        #     if submit_button:
        #         with st.spinner("Rebuilding dataset..."):
        #             build_dataset()
        #             st.success("Dataset has been reset")

login_page()
        
        
