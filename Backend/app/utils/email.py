from fastapi_mail import FastMail, MessageSchema
from core.email import conf
from .otp import generate_otp

async def send_otp_to_email(email: str, purpose: str):
    try:
        otp = generate_otp()

        html_content = f"""
        <div style="font-family: Arial, sans-serif; text-align: center; padding: 20px;">
            <h2 style="color: #e91e63;">Your OTP Code for {purpose}</h2>
            <p style="font-size: 16px; color: #333;">Use the following code to proceed:</p>
            <div style="margin: 20px 0; font-size: 24px; font-weight: bold; color: #000; letter-spacing: 4px;">
                {otp}
            </div>
            <p style="font-size: 14px; color: #666;">This code is valid for 5 minutes. Do not share it with anyone.</p>
            <hr style="margin: 20px 0; border: none; border-top: 1px solid #ddd;">
            <p style="font-size: 12px; color: #999;">If you did not request this, please ignore this email.</p>
        </div>
        """

        message = MessageSchema(
            subject=f"Your OTP Code for {purpose}",
            recipients=[email],
            body=html_content,
            subtype="html"
        )

        fm = FastMail(conf)
        await fm.send_message(message)
        return otp
    except Exception as e:
        raise e
