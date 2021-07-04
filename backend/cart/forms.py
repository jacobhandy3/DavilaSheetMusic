from django import forms

#list of quantites for an item
QUANTITIES = [(i,str(i)) for i in range(1,21)]

class CartAddForm(forms.Form):
    #field to specify number of items, must be int
    quantity = forms.TypedChoiceField(label="",choices=QUANTITIES,coerce=int)
    #determines whether specific quantity requested, rather than just adding to current quantity
    override = forms.BooleanField(required=False,initial=False,widget=forms.HiddenInput)