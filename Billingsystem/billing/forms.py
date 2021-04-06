from django.forms import ModelForm
from .models import Purchase,Order,Item
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class BillPurchaseForm(ModelForm):
    class Meta:
        model=Purchase
        fields="__all__"

class OrderCreateForm(ModelForm):
    class Meta:
        model=Order
        fields=["billnumber",
                "customer_name",
                "phone_number"]
class OrderlineForm(forms.Form):
    bill_number=forms.CharField()
    product_qty=forms.IntegerField()
    product_name = Purchase.objects.all().values_list("item_name__item_name")
    result=[(tp[0],tp[0]) for tp in product_name]
    product_name=forms.ChoiceField(choices=result)
class Registrationform(UserCreationForm):
    class Meta:
        model=User
        fields=['first_name','last_name','email','password1','password2']
class Loginform(forms.Form):
    username=forms.CharField(max_length=120)
    password=forms.CharField(max_length=120)
class Dateform(forms.Form):
    date=forms.DateField()

