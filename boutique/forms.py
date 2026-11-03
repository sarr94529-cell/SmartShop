from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
class InscriptionForm(UserCreationForm):
    email=forms.EmailField(required=True)
    class Meta:
        model=User
        fields=('username','email','password1','password2')
    def clean_email(self):
        email=self.cleaned_data['email']
        if User.objects.filter(email__iexact=email).exists(): raise forms.ValidationError('Cette adresse e-mail est déjà utilisée.')
        return email
class CommandeForm(forms.Form):
    nom=forms.CharField(max_length=150)
    telephone=forms.CharField(max_length=30)
    adresse=forms.CharField(widget=forms.Textarea(attrs={'rows':3}))
