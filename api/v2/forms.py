from django import forms
from django.contrib.auth import password_validation


class RegistroForm(forms.Form):

    email = forms.EmailField(label='User email')
    password1 = forms.CharField(label='password',
                                widget=forms.PasswordInput,
                                help_text=password_validation.password_validators_help_text_html())
    password2 = forms.CharField(label='password confirmation',
                                widget=forms.PasswordInput)

    name = forms.CharField(label='name', max_length=150)
    phone = forms.CharField(label='phone', max_length=30)
    institution = forms.CharField(label='institution', max_length=30)
    role = forms.CharField(label='role', max_length=30)

    def clean_name(self):
        return self.cleaned_data.get('name').lower()

    def clean_institution(self):
        return self.cleaned_data.get('institution').lower()

    def clean_role(self):
        return self.cleaned_data.get('role').lower()

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 != password2:
            raise forms.ValidationError(
                'The two password fields didn’t match.',
                code='password_mismatch'
            )

        return password2

    def clean(self):
        password = self.cleaned_data.get('password1')
        if password:
            try:
                password_validation.validate_password(password, None)
            except forms.ValidationError as error:
                self.add_error('password1', error)
