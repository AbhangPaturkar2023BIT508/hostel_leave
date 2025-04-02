from django import forms
from django.contrib.auth.hashers import make_password  # Add this import
from .models import HostelUser
from .models import LeaveApplication

class HostelUserForm(forms.ModelForm):
    class Meta:
        model = HostelUser
        fields = ['username', 'password', 'email', 'contact', 'address', 'role']
        widgets = {
            'password': forms.PasswordInput(),
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.password = make_password(user.password)  # Hash the password before saving
            user.save()
        return user



class LeaveApplicationForm(forms.ModelForm):
    class Meta:
        model = LeaveApplication
        fields = ['start_date', 'end_date', 'reason']

    def __init__(self, *args, **kwargs):
        super(LeaveApplicationForm, self).__init__(*args, **kwargs)
        self.fields['start_date'].widget = forms.DateInput(attrs={'type': 'date'})
        self.fields['end_date'].widget = forms.DateInput(attrs={'type': 'date'})

