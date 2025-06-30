from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User


class RegisterForm(forms.ModelForm):

    name = forms.CharField(
        required=True,
        min_length=3,
        label='Nome:',
    )
    name.widget.template_name_label = 'Nome'
    email = forms.EmailField(
        required=True,
        label='E-mail:',
    )
    phone = forms.CharField(
        label='Telefone:',
    )
    choices = {
        "Liga da Justiça": "Liga da Justiça",
        "Os vingadores": "Os vingadores"
    }
    group = forms.ChoiceField(
        widget=forms.RadioSelect,
        choices= choices,
        label='Quero ser do grupo:'
    )
    #group.
    class Meta:
        model = User
        fields = (
            'name', 'email', 'phone',
        )


class ContactForm(forms.ModelForm):

    class Meta:
       fields = (
           'name',
           'email',
           'phone',
           'group',
       )