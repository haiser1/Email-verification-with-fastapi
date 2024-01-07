import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import os
from dotenv import load_dotenv

load_dotenv()

def send_email_virification(receiver_email: str, verification_code: str):

    email = os.getenv('EMAIL')
    password = os.getenv('PASSWORD')
    print(email, password)

    subject = 'Verification Code'
    body = f'Your code is: {verification_code}'

    message = MIMEMultipart()
    message['from'] = email
    message['to'] = receiver_email
    message['Subject'] = subject

    message.attach(MIMEText(body, 'plain'))

    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login(email, password)

        server.sendmail(email, receiver_email, message.as_string())


