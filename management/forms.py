from django import forms
from management.models import User

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = '__all__'
        #field = ['salutation', 'first_name', 'last_name', 'email']
