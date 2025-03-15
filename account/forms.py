from django import forms
from django.forms import ImageField, FileInput, DateInput

from .models import KYC


class DateInput(forms.DateInput):
    input_type = 'date'


