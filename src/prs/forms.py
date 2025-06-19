from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User


class RegisterForm(forms.ModelForm):

    name = forms.CharField(
        required=True,
        min_length=3,
    )
    email = forms.EmailField(
        required=True,
    )
    phone = forms.CharField()
    choices = {
        "1": "Liga da Justiça",
        "2": "Os vingadores"
    }
    group = forms.ChoiceField(
        widget=forms.RadioSelect,
        choices= choices,
    )
    #group.
    class Meta:
        model = User
        fields = (
            'name', 'email', 'phone',
        )