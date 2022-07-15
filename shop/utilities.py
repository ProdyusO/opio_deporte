"""Added abilities."""
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings
from django.core.exceptions import ValidationError


def validation_phone_number(phone):
    """Validate correct data nput of phone number."""
    if phone.startswith("0") is False or len(phone) != 10 or phone.isdigit() is False:
        raise ValidationError(
            'Будь ласка, вкажіть коректний номер телефону, наприклад "0671234567"',
            params={"phone": phone},
        )


def send_email_to_boss(owner, customer_orders, price):
    """Sends email to owner."""
    email_body_template = render_to_string(
        "email/boss_mail.txt",
        {"owner": owner, "customer_orders": customer_orders, "price": price},
    )
    email_to_boss = EmailMessage(
        f"Yoooo! Шоколадний ти отримав замовлення від {owner}",
        email_body_template,
        settings.EMAIL_HOST_USER,
        ["cahek102@gmail.com"],
    )
    email_to_boss.fail_silently = False
    email_to_boss.send()


def send_email_to_customer(owner, customer_orders, price):
    """Sends email to the client."""
    email_body_template = render_to_string(
        "email/customer_mail.txt",
        {"owner": owner, "customer_orders": customer_orders, "price": price},
    )
    email_to_customer = EmailMessage(
        "Замовлення, інтернет-магазин одягу @opio_deporte",
        email_body_template,
        settings.EMAIL_HOST_USER,
        [f"{owner.email}"],
    )
    email_to_customer.fail_silently = False
    email_to_customer.send()
