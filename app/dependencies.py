from functools import lru_cache, wraps
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import EmailStr
import re
from quart import render_template, request, redirect, url_for, flash
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import aiosmtplib
from http import HTTPStatus


def validate_phone_number(phone: str) -> str:
    """
    Validate if phone number is a valid Kenyan number
    """
    pattern = re.compile(r"^(?:\+?254\s?|0)(7|1)\d{8}$")
    if not pattern.match(phone):
        raise ValueError("Phone number must be a valid Kenyan number")
    return phone


def valid_json(f):
    """
    Decorator to check if the request is a valid JSON.

    Sets the body of the request as a keyword argument on success.

    :param f: The function to decorate.

    """
    @wraps(f)
    async def decorated_function(*args, **kwargs):
        if not request.is_json:
            return {"error": "Request must be a valid JSON"}, HTTPStatus.BAD_REQUEST.value

        try:
            kwargs["body"] = await request.get_json()
        except Exception as e:  # catch BadRequest error
            return {"error": str(e)}, HTTPStatus.BAD_REQUEST.value
        return await f(*args, **kwargs)
    return decorated_function


@lru_cache()
def get_settings():
    """
    Get application settings
    """

    class Settings(BaseSettings):
        """
        Application settings
        """

        model_config = SettingsConfigDict(
            env_prefix="APP_",
            env_file="./app/.env",
        )

        admin_email: EmailStr
        admin_password: str

        # email settings
        email_host: str = "smtp.gmail.com"
        email_port: int = 465
        email_use_tls: bool = True

        cors_allow_origin: str = "*"

    return Settings()


async def send_email(
    sender_email: str,
    sender_password: str,
    recipient_email: str,
    header_subject: str,
    msg: str,
):
    """
    Send email

    :param sender_email: sender email address
    :param sender_password: sender email password
    :param recipient_email: recipient email address
    :param header_subject: email subject (header)
    :param msg: email message

    """
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = recipient_email
    message["Subject"] = header_subject
    message.attach(MIMEText(msg, "html"))

    async with aiosmtplib.SMTP(
        hostname=get_settings().email_host,
        port=get_settings().email_port,
        use_tls=get_settings().email_use_tls,
    ) as smtp:
        await smtp.login(sender_email, sender_password)
        await smtp.send_message(message)


async def send_email_template(
    sender_email: str,
    sender_password: str,
    recipient_email: str,
    header_subject: str,
    template: str,
    **kwargs
):
    """
    Send email using template
    """
    message = await render_template(template, **kwargs)
    await send_email(sender_email, sender_password, recipient_email, header_subject, message)


async def send_contact_us_email(
    sender_email: str, sender_password: str, recipient_email: str, header_subject: str, **kwargs
):
    """
    Send contact us email
    """
    await send_email_template(
        sender_email,
        sender_password,
        recipient_email,
        header_subject,
        "email/contact_us.html",
        **kwargs
    )


async def send_quotation_email(
    sender_email: str, sender_password: str, recipient_email: str, header_subject: str, **kwargs
):
    """
    Send quotation email
    """
    await send_email_template(
        sender_email,
        sender_password,
        recipient_email,
        header_subject,
        "email/quotation.html",
        **kwargs
    )
