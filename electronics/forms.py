from django import forms

class PaymentForm(forms.Form):
    name = forms.CharField(label='Your name', max_length=100, widget=forms.TextInput(attrs={
        'class' : "form-control me-2 text-capitalize",
        'placeholder': 'name'
    }))
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class' : "form-control me-2 text-capitalize",
        'placeholder': 'email'
    }))
    phone=forms.CharField(max_length=14, widget=forms.NumberInput(attrs={
        'class' : "form-control me-2 text-capitalize",
        'placeholder': 'phone'
    }))
    amount = forms.FloatField()