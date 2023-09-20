import streamlit as st 
import cv2
import yaml 
import pickle 
from utils import submitNew, get_info_from_id, deleteOne
import numpy as np
import datetime
import subprocess
import re
import psycopg2
st.set_page_config(layout="wide")
st.title("Face Recognition App")
st.write("This app is used to add new faces to the dataset")

# menu = ["Adding"]
# choice = st.sidebar.selectbox("Options",menu)
# if choice == "Adding":
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

def luhn_algorithm_validation(number):
    # Convert the number to a list of integers and reverse it
    digits = [int(digit) for digit in str(number)][::-1]
    
    # Double every second digit and subtract 9 if the result is greater than 9
    for i in range(1, len(digits), 2):
        doubled_digit = digits[i] * 2
        if doubled_digit > 9:
            doubled_digit -= 9
        digits[i] = doubled_digit
    
    # Calculate the sum of all digits
    total = sum(digits)
    
    # Check if the total is divisible by 10
    if total % 10 == 0:
        return True  # The number is valid according to Luhn's algorithm
    else:
        return False  # The number is invalid
    
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
def registration_page():
    st.title("User Registration")
    
    menu = ["Adding","Deleting"]
    choice = st.sidebar.selectbox("Options",menu)
    if choice == "Adding":  
    
        current_date = datetime.date(datetime.datetime.now().year, datetime.datetime.now().month, datetime.datetime.now().day)

        # Set the minimum and maximum dates
        min_date = datetime.date(1900, 1, 1)
        max_date = current_date
        name = st.text_input("Name",placeholder='Enter name')
        id = st.text_input("ID",placeholder='Enter id', max_chars=13)
        
        col1, col2, col3 = st.columns(3)
        first_name = col1.text_input("First Name")
        last_name = col1.text_input("Last Name")
        id_number = col1.text_input("ID Number", max_chars=13)

            # Input fields for date of birth, race, and phone number in the second column
        dob = col2.date_input("Date of Birth", min_value=min_date, max_value=max_date, value=datetime.date.today())
        st.session_state.dob = dob
        race_options = ["White", "Black", "Asian", "Mixed", "Other"]
        race = col2.selectbox("Race", race_options)
        phone_number = col2.text_input("Phone Number", max_chars=10)

            # Input fields for gender, age, provinces, address, district, and ward number in the third column
        gender_options = ["Male", "Female"]
        gender = col3.selectbox("Gender", gender_options)
        age = col3.text_input("Age")
        provinces = ["Eastern Cape", "Free State", "Gauteng", "KwaZulu-Natal", "Limpopo", "Mpumalanga", "Northern Cape", "North West", "Western Cape"]
        province = col3.selectbox("Province", provinces)
        district = col3.text_input("District")
        email = col3.text_input("Email")
        ward_number = col1.text_input("Ward Number")

            # Input fields for email, username, password, and password confirmation
        address = col1.text_input("Address")
        password = col2.text_input("Password", type="password")
        confirm_password = col2.text_input("Confirm Password", type="password")
            
    
            # Form submission button
        
            
            
        #Create 2 options: Upload image or use webcam
        #If upload image is selected, show a file uploader
        #If use webcam is selected, show a button to start webcam
        
        
            # uploaded_image = st.file_uploader("Upload",type=['jpg','png','jpeg'])
            # if uploaded_image is not None:
            #     st.image(uploaded_image)
            #     submit_btn = st.button("Submit",key="submit_btn")
            #     if submit_btn:
            #         if password == "" or id_number == "":
            #             st.error("Please enter name and ID")
            #         else:
            #             ret = submitNew(password, id_number, uploaded_image)
            #             if ret == 1: 
            #                 st.success("Student Added")
            #             elif ret == 0: 
            #                 st.error("Student ID already exists")
            #             elif ret == -1: 
            #                 st.error("There is no face in the picture")
        # if upload == "Webcam":
        # upload = st.radio("Upload image or use webcam",("Webcam"))
        img_file_buffer = st.camera_input("Take a picture")
        submit_btn = st.button("Submit", key="submit_btn")
        
        if img_file_buffer is not None:
                # To read image file buffer with OpenCV:
                bytes_data = img_file_buffer.getvalue()
                cv2_img = cv2.imdecode(np.frombuffer(bytes_data, np.uint8), cv2.IMREAD_COLOR)

        if submit_btn:
            # Check if the user ID already exists in the database
            if (
                password == "" or id_number == "" or
                not all([first_name, last_name, id_number, phone_number, email, password, confirm_password, gender, age, dob, race, province, address, district, ward_number])
            ):
                st.error("Please fill in all the fields.")
            elif not is_valid_id_number(id_number):
                st.error("Invalid ID number. It should have exactly 13 characters and pass the Luhn's algorithm validation.")
            elif not is_valid_email(email):
                st.warning("Invalid email format. Please enter a valid email address.")
            elif password != confirm_password:
                st.error("Passwords do not match.")
            elif not is_valid_password(password):
                st.error("Invalid password. It should be at least 8 characters long and contain at least one digit, one uppercase letter, one lowercase letter, and one special character.")
            elif img_file_buffer is None:
                st.error("Please take a picture for registration.")
            else:
                bytes_data = img_file_buffer.getvalue()
                cv2_img = cv2.imdecode(np.frombuffer(bytes_data, np.uint8), cv2.IMREAD_COLOR)
                if not luhn_algorithm_validation(id_number):
                    st.error("Invalid ID number.")
                else:
                    ret = submitNew(name, id_number, cv2_img)
                        
            conn = psycopg2.connect(
                        host="localhost",
                        port=5430,
                        database="food_ordering_system",
                        user="postgres"
                    )

                    # Create a cursor for database operations
            cursor = conn.cursor()
                                # Insert user information into the database
            cursor.execute('''
                        INSERT INTO users_info (
                            id_number,
                            firstname,
                            lastname,
                            dob,
                            gender,
                            race,
                            age,
                            phone_number,
                            province,
                            ward_number,
                            passwords,
                            address_no,
                            district,
                            email,
                            encoding
                        )
                        VALUES (
                            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
                        )
                    ''', (
                        id_number, first_name, last_name, dob, gender, race, age,
                        phone_number, province, ward_number, password, address,
                        district, email, bytes_data
                    ))
            conn.commit()
            if ret == 1: 
                st.success("User Added")
            elif ret == 0: 
                st.error(" Id number already exists ")
            elif ret == -1: 
                    st.error("There is no face in the picture")
                    
    elif choice == "Deleting":
        def del_btn_callback(id):
            deleteOne(id)
            st.success("Student deleted")
        
        id = st.text_input("ID",placeholder='Enter id')
        submit_btn = st.button("Submit",key="submit_btn")
        if submit_btn:
            name, image,_ = get_info_from_id(id)
            if name == None and image == None:
                st.error("Student ID does not exist")
            else:
                st.success(f"Name of student with ID {id} is: {name}")
                st.warning("Please check the image below to make sure you are deleting the right student")
                st.image(image)
                del_btn = st.button("Delete",key="del_btn",on_click=del_btn_callback, args=(id,)) 
        
    
        Exit_btn = st.button("Back", key="Exit_btn")
        if Exit_btn:
            subprocess.Popen(['streamlit', 'run', 'HomePage.py'])
registration_page()