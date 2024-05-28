import smtplib, ssl
from os import getenv

# Load environment variables
PASSWORD = getenv("EMAIL_PASSWORD")

def send_email(message: str):
    host = 'smtp.gmail.com'
    port = 465

    username = 'benoit.roux@gmail.com'
    receiver = 'benoit.roux@gmail.com'
    context = ssl.create_default_context()

    with smtplib.SMTP_SSL(host, port, context=context) as server:
        server.login(username, PASSWORD)
        server.sendmail(username, receiver, message)

if __name__ == "__main__":
    message = """Subject: Test Email\n\n
    Hello, World!
"""
    send_email(message)