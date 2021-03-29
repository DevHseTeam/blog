from django.contrib import auth
from django import forms
from .models import Profile


class LoginForm(auth.forms.AuthenticationForm): #ok

    error_messages = {
        'invalid_login': 'Неверное имя пользователя или пароль.',
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.use_required_attribute = False
        self.fields['username'].widget.attrs.pop("autofocus", None)


class AccountCreateForm(auth.forms.UserCreationForm):

    first_name = forms.CharField(max_length=128, widget=forms.TextInput(
        attrs={'placeholder': 'Harry'},
    ))
    last_name = forms.CharField(max_length=128, widget=forms.TextInput(
        attrs={'placeholder': 'Potter'},
    ))
    email = forms.EmailField(max_length=128, widget=forms.EmailInput(
        attrs={'placeholder': 'harry_potter@hogwarts.com'},
    ))
    username = forms.CharField(max_length=128, widget=forms.TextInput(
        attrs={'placeholder': 'harry_potter'},
    ))

    field_order = ('first_name', 'last_name', 'email')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.use_required_attribute = False
        self.fields['username'].widget.attrs.pop("autofocus", None)

    def save(self):
        user = super().save()

        user.email = self.cleaned_data.get('email')
        user.save()

        user.profile.first_name = self.cleaned_data.get('first_name')
        user.profile.last_name = self.cleaned_data.get('last_name')
        user.profile.save()

        return user



class ProfileUpdateForm(forms.ModelForm):

    class Meta:
        model = Profile
        exclude = ['user']
        labels = {
            'first_name': 'Имя',
            'last_name':  'Фамилия',
            'photo':      'Фото',
            'gender':     'Пол',
            'age':        'Возраст',
        }
