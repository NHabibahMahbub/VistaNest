from django import forms
from .models import Platform,  Bid


class PlatformForm(forms.ModelForm):
    class Meta:
        model = Platform
        fields = '__all__'


class SearchForm(forms.ModelForm):
    query = forms.CharField(label='Search', max_length=100, required=True)

    class Meta:
        model = Platform
        fields = ['query']

class BidForm(forms.ModelForm):
    class Meta:
        model = Bid
        fields = ['amount']