from email.message import EmailMessage

from pydantic import EmailStr

from app.config import settings


def create_booking_confirmation_template(
        booking: dict,
        email_to: EmailStr,

):
    email = EmailMessage()
    email["Subject"] = "Booking confirmation"
    email["From"] = settings.SMT_EMAIL
    email["To"] = email_to

    email.set_content(
        f'''
            <h1>Booking confirmation</h1>
            <p>You booking hotel with {booking["date_from"]} from {booking["date_to"]}</p>
        ''',
        subtype="html",
    )
    return email