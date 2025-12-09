import smtplib
from pathlib import Path

from PIL import Image
from pydantic import EmailStr

from app.config import settings
from app.tasks.email_templates import create_booking_confirmation_template
from app.tasks.worker import celery


@celery.task
def process_pic(
        path: str
):
    img_path = Path(path)
    img = Image.open(img_path)
    img_resized_big = img.resize((1000, 500))
    img_resized_smol = img.resize((200, 100))
    img_resized_big.save(f"app/frontend/static/img/img_resized_big{img_path.name}")
    img_resized_big.save(f"app/frontend/static/img/img_resized_smol{img_path.name}")


@celery.task
def send_booking_confirmation_email(
        booking: dict,
        email_to: EmailStr
):
    email_to_mock = settings.SMT_EMAIL
    msg_content = create_booking_confirmation_template(booking, email_to_mock)

    with smtplib.SMTP_SSL(settings.SMT_HOST, settings.SMT_PORT) as server:
        server.login(settings.SMT_EMAIL, settings.SMT_PASSWORD)
        server.send_message(msg_content)