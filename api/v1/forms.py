from django import forms


class RegistroForm(forms.Form):
    username = forms.CharField(label='User name', max_length=100)
    email = forms.EmailField(label='User email')
    password1 = forms.CharField(max_length=50, widget=forms.PasswordInput)
    password2 = forms.CharField(max_length=50, widget=forms.PasswordInput)

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 != password2:
            raise forms.ValidationError(
                'The two password fields didn’t match.',
                code='password_mismatch'
            )

        return password2


class LoginForm(forms.Form):
    username = forms.CharField(label='User name', max_length=100)
    password = forms.CharField(max_length=50, widget=forms.PasswordInput)
