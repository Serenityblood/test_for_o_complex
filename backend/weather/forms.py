from django import forms
from .models import City


class CityForm(forms.Form):
    city = forms.ModelChoiceField(
        queryset=City.objects.all(),
        label="City",
        widget=forms.Select(attrs={"class": "form-control"}),
    )
