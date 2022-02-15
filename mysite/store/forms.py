from django import forms

class LoginForm(forms.Form):
    userid = forms.CharField(label = 'Account',required = True)
    password = forms.CharField(label = 'Password', widget= forms.PasswordInput)

class RegistrationForm(forms.Form):
    userid = forms.CharField(label='Account', required=True)
    name = forms.CharField(label='Name', required=True)
    password1 = forms.CharField(label='Password', widget = forms.PasswordInput )
    password2 = forms.CharField(label='Password Again', widget = forms.PasswordInput )
    birthday = forms.DateField(label='Date of Birth',error_messages={'invalid': 'Invalid input'})
    address = forms.CharField(label='Address', required=False)
    phone = forms.CharField(label='Account', required=False)

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('You two input passwords do not match')

        return password2


