from django import forms
from .models import Order
from django.forms import Field

Field.default_error_messages = {
    "invalid": "Введите корректный email.",
    "required": "Это поле обязательно для заполнения.",
}

MY_CHOICES = [(0, 'СДЭК'), (1, 'Почта'), (2, 'Самовывоз'),]



class OrderCreateForm(forms.ModelForm):
    
    status = forms.ChoiceField(label="Выбор доставки", widget=forms.RadioSelect(attrs={'onchange': 'showOrHide()'}), choices=MY_CHOICES)

    class Meta:
        model = Order
        fields = ["first_name", "last_name", "email", "address", "postal_code"]