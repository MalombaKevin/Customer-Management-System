
from django import forms

from django.forms import ModelForm

from .models import *

class OrderForm(forms.ModelForm):

    class Meta:
        model = Order
        fields = '__all__'

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = '__all__'
