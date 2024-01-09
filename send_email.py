import smtplib
import os
from dotenv import load_dotenv
import random
import string

load_dotenv()

def generate_code():
    chracter = string.digits

    random_code = ''.join(random.choice(chracter) for _ in range(6))
    return random_code

def send_email_virification(receiver_email: str, verification_code: str):

    email = os.getenv('MAIL_USERNAME')
    password = os.getenv('MAIL_PASSWORD')
    host = os.getenv('HOST')

    subject = "Your OTP Code"
    body = f"OTP Code: {verification_code}\n Your code expired in 1 minutes"

    msg = f"Subject: {subject}\n\n{body}"

    try:
        smtp = smtplib.SMTP(host, 587)

        smtp.ehlo()

        smtp.starttls()

        smtp.login(email, password)

        smtp.sendmail(email, receiver_email, msg)

        smtp.quit()
        
        print(f'Email send successfuly')

    except Exception as err:
        print(f'Invalid send email, Error: {err}')

