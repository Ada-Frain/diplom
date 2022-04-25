from django import forms
from .models import Order

from django.forms import Field
from django.utils.translation import ugettext_lazy

Field.default_error_messages = {
    "invalid": "Введите корректный email.",
    "required": "Это поле обязательно для заполнения.",
}


class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ["first_name", "last_name", "email", "address", "postal_code", "city"]