from django.forms import ModelForm
from django import forms

from app_store.models import Reviews


class ReviewForm(ModelForm):
    text = forms.CharField(
        max_length=200,
        required=True,
        widget=forms.Textarea(
            attrs={
                "class": "form-textarea",
                "data-validate": "require",
                "placeholder": "Ваш отзыв",
            }
        ),
    )

    class Meta:
        model = Reviews
        fields = ["text"]
