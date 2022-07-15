"""Form's module"""
from django import forms
from captcha.fields import CaptchaField
from .models import Customer  # pylint: disable=E0402


class CustomerForm(forms.ModelForm):
    """Customer's post form."""

    captcha = CaptchaField(label="Введіть текст з картинки")

    class Meta:  # pylint: disable=R0903
        """Form's settings."""

        model = Customer
        fields = (
            "first_name",
            "last_name",
            "phone_number",
            "email",
            "buying_type",
            "new_post",
            "comment",
        )
        widgets = {"buying_type": forms.RadioSelect}
        help_texts = {"new_post": "(Наприклад: м. Одеса, НП №127)"}
