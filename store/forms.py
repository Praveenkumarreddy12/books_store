from django import forms
from .models import Customer, Books_ordered, Books_available
# Add your form classes here 



class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'id_number', 'phone_number','address']

class Books_orderedForm(forms.ModelForm):
    class Meta:
        model = Books_ordered
        fields = ['name', 'book_id', 'customer', 'price']

class Books_availableForm(forms.ModelForm):
    class Meta:
        model = Books_available
        fields = ['name', 'book_id', 'price', 'image','stock']
        