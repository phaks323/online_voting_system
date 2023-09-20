import datetime

def calculate_age_from_id_number(id_number):
    # Extract the year, month, and day from the ID number
    year = int(id_number[:2])
    month = int(id_number[2:4])
    day = int(id_number[4:6])

    # Calculate the current year
    current_year = datetime.datetime.now().year

    # Calculate the user's age
    age = current_year - (1900 + year)  # Adjust the base year as needed

    return age
