import asyncio
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from dotenv import load_dotenv
from fastapi import HTTPException

load_dotenv()

EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")


def _send_mail_sync(worker, subject: str, message: str):
    msg = MIMEMultipart()

    msg["From"] = "vmkmanoj13@gmail.com"
    msg["To"] = worker.email
    msg["Subject"] = subject

    body = f"""
        Dear {worker.first_name} {worker.last_name},

        {message}

        Best Regards,

        Human Resources Team
        Manojkumar V
    """

    msg.attach(MIMEText(body, "plain"))

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login("vmkmanoj13@gmail.com", "wesu kefi sbfv kzdu")
        server.sendmail("vmkmanoj13@gmail.com", worker.email, msg.as_string())


async def send_mail_information(worker, subject: str, message: str):
    try:
        await asyncio.to_thread(_send_mail_sync, worker, subject, message)

        print(f"Mail sent to {worker.first_name} {worker.last_name}")
        return True

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to send email: {e!s}")


def send_email(worker):
    try:
        msg = MIMEMultipart()
        msg["From"] = "vmkmanoj13@gmail.com"
        msg["To"] = worker.email
        msg["Subject"] = "Worker added"
        body = f"""
            Dear {worker.name},

            We are pleased to welcome you to our organization.

            Your profile has been successfully created in our employee management system, and we are excited to have you as part of our team.

            Your details:

            Name   : {worker.name}
            Role   : {worker.role}
            Email  : {worker.email}
            Phone  : {worker.phone}
            Status : {worker.status}

            Our team will contact you soon with further information regarding your onboarding process, work schedule, and any other necessary details.

            If you have any questions, please feel free to contact your manager or the Human Resources team.

            We wish you a successful and rewarding journey with us.

            Best Regards,

            Human Resources Team
            Manojkumar
        """

        msg.attach(MIMEText(body, "plain"))
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login("vmkmanoj13@gmail.com", "wesu kefi sbfv kzdu")
            server.sendmail(EMAIL_ADDRESS, worker.email, msg.as_string())

        print(f"Mail sended {worker.email}")
        return True

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to send email: {e!s}")

