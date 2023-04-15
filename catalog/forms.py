from django import forms
from django.forms import ChoiceField, ModelForm, TextInput, Textarea

from .models import Review


class ReviewForm(ModelForm):
    CHOICES = (
        ("5", "5"),
        ("4", "4"),
        ("3", "3"),
        ("2", "2"),
        ("1", "1"),
    )
    rating = ChoiceField(choices=CHOICES)

    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'comment': Textarea(attrs={'cols': 60})
        }
