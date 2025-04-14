import smtplib
import os
import random
import jwt
from datetime import datetime, timedelta
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from fastapi import BackgroundTasks
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
SMTP_SERVER = os.getenv('SMTP_SERVER')
SMTP_PORT = int(os.getenv('SMTP_PORT', 587))  
SENDER_EMAIL = os.getenv('SENDER_EMAIL')
SENDER_PASSWORD = os.getenv('SENDER_PASSWORD')
SENDER_NAME = os.getenv('SENDER_NAME')
SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = os.getenv('ALGORITHM', 'HS256')
RESET_TOKEN_EXPIRE_MINUTES = int(os.getenv('RESET_TOKEN_EXPIRE_MINUTES', 30))

# Generate a 6-digit numeric verification code
def generate_verification_code() -> str:
    """Generate a 6-digit numeric verification code."""
    return str(random.randint(100000, 999999))

def get_email_template(verification_code: str) -> str:
    """Generate an HTML email template for verification."""
    return f"""
    <html>
    <body style="font-family: Arial, sans-serif; background-color: #f4f4f4; padding: 20px;">
        <div style="max-width: 600px; margin: auto; background-color: #ffffff; padding: 30px; border-radius: 10px; box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);">
            <h2 style="color: #4caf50; text-align: center;">Verify Your Email</h2>
            <p style="font-size: 16px; color: #333;">Hello,</p>
            <p style="font-size: 16px; color: #333;">Your verification code is:</p>
            <div style="text-align: center; font-size: 24px; font-weight: bold; color: #4caf50; margin: 20px 0;">
                {verification_code}
            </div>
            <p style="font-size: 14px; color: #555;">
                Please enter this code on the verification page to complete your registration.
            </p>
        </div>
    </body>
    </html>
    """

def get_reset_password_template(reset_link: str) -> str:
    """Generate an HTML email template for password reset."""
    return f"""
    <html>
    <body style="font-family: Arial, sans-serif; background-color: #f4f4f4; padding: 20px;">
        <div style="max-width: 600px; margin: auto; background-color: #ffffff; padding: 30px; border-radius: 10px; box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);">
            <h2 style="color: #4caf50; text-align: center;">Reset Your Password</h2>
            <p style="font-size: 16px; color: #333;">Hello,</p>
            <p style="font-size: 16px; color: #333;">Click the link below to reset your password:</p>
            <div style="text-align: center; margin: 20px 0;">
                <a href="{reset_link}" style="text-decoration: none; color: white; background-color: #4caf50; padding: 10px 20px; border-radius: 5px;">Reset Password</a>
            </div>
            <p style="font-size: 14px; color: #555;">
                If you did not request a password reset, please ignore this email.
            </p>
        </div>
    </body>
    </html>
    """

def send_email(email: str, msg_or_subject: str, body: str = None) -> None:
    """Send an email with optional HTML body."""
    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.ehlo()
            server.starttls()
            server.ehlo()
            server.login(SENDER_EMAIL, SENDER_PASSWORD)

            if isinstance(msg_or_subject, MIMEMultipart):
                server.sendmail(SENDER_EMAIL, email, msg_or_subject.as_string())
            else:
                msg = MIMEMultipart()
                msg['From'] = f"{SENDER_NAME} <{SENDER_EMAIL}>"
                msg['To'] = email
                msg['Subject'] = msg_or_subject
                msg.attach(MIMEText(body, 'html'))
                server.sendmail(SENDER_EMAIL, email, msg.as_string())

            print(f"Email sent to {email} successfully.")
    except Exception as e:
        print(f"Failed to send email to {email}: {e}")

def send_verification_email(email: str, verification_code: str, background_tasks: BackgroundTasks) -> None:
    """Send an email with a verification code."""
    subject = "Your Verification Code for SustainaWare"
    html_body = get_email_template(verification_code)
    msg = MIMEMultipart()
    msg["From"] = f"{SENDER_NAME} <{SENDER_EMAIL}>"
    msg["To"] = email
    msg["Subject"] = subject
    msg.attach(MIMEText(html_body, "html"))
    background_tasks.add_task(send_email, email, msg)

def generate_reset_token(email: str) -> str:
    """Generate a JWT reset token for the given email."""
    expire = datetime.utcnow() + timedelta(minutes=RESET_TOKEN_EXPIRE_MINUTES)
    payload = {"sub": email, "exp": expire}
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def send_reset_password_email(email: str, token: str, background_tasks: BackgroundTasks) -> None:
    """Send an email with a password reset link."""
    reset_link = f"http://localhost:5173/reset-password?token={token}"
    subject = "Reset Your Password"
    html_body = get_reset_password_template(reset_link)
    msg = MIMEMultipart()
    msg["From"] = f"{SENDER_NAME} <{SENDER_EMAIL}>"
    msg["To"] = email
    msg["Subject"] = subject
    msg.attach(MIMEText(html_body, "html"))
    background_tasks.add_task(send_email, email, msg)
