from django import forms


class RegistroForm(forms.Form):

    email = forms.EmailField(label='User email')
    password1 = forms.CharField(max_length=50, widget=forms.PasswordInput)
    password2 = forms.CharField(max_length=50, widget=forms.PasswordInput)

    name = forms.CharField(label='name', max_length=150)
    phone = forms.CharField(label='phone', max_length=30)
    institution = forms.CharField(label='institution', max_length=30)
    role = forms.CharField(label='role', max_length=30)

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 != password2:
            raise forms.ValidationError(
                'The two password fields didn’t match.',
                code='password_mismatch'
            )

        return password2
