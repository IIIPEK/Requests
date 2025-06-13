from django import forms
from .models import Request

class RequestForm(forms.ModelForm):
    class Meta:
        model = Request
        fields = ['title', 'description', 'quantity', 'price', 'month', 'year', 'department', 'approver']
