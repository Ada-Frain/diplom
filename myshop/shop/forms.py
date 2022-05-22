from django import forms
from .models import Rating, RatingStar, Response

class ResponseForm(forms.ModelForm):
    class Meta:
        model = Response
        fields = ('name', 'comment',)


class RatingForm(forms.ModelForm):
    """Форма добавления рейтинга"""
    star = forms.ModelChoiceField(
        queryset=RatingStar.objects.all(), widget=forms.RadioSelect(), empty_label=None
    )

    class Meta:
        model = Rating
        fields = ("star",)