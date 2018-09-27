from django import forms
from .models import Contact

class NewContactForm(forms.ModelForm):
    # name = forms.CharField()
    # adress = forms.CharField(widget=forms.Textarea)
    # photo = forms.ImageField()
    class Meta:
        """docstring for Meta."""
        model = Contact
        fields = '__all__'
