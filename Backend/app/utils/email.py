from fastapi_mail import FastMail, MessageSchema
from core.email import conf
from .otp import generate_otp

async def send_otp_to_email(email: str):
    try:
        otp = generate_otp()
        message = MessageSchema(
            subject="Your OTP Code",
            recipients=[email],
            body=f"Your OTP code for registration is: {otp}",
            subtype="plain"
        )
        fm = FastMail(conf)
        await fm.send_message(message)
        return otp
    except Exception as e:
        raise e