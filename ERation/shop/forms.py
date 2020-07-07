from django.forms import forms, ModelForm, TextInput, Textarea, Select, CharField, NumberInput
from . models import *
from eadmin.models import SalesReport
from customer.models import Orders

class NewShopForm(ModelForm):
    class Meta:
        model = Shop
        exclude = ['id']
        widgets = {
            # 'id': Select(
            #     attrs={
            #         'class': 'form-control',
            #         'required': 'required'
            #     }
            # ),
            'name': TextInput(
                attrs={
                    'class': 'form-control',
                    'required': 'required'
                }
            ),
            'shop_id': TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': '5CB387D65JCE25'

                }
            ),
            'place': TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ernakulam'
                }
            ),
            'address': Textarea(
                attrs={
                    'class': 'form-control'
                }
            ),
            'phone': TextInput(
                attrs={
                    'class': 'form-control',
                    'type': 'number',
                    'maxlength': 10,
                    'minvalue': 6666666666,
                    'placeholder': 'XX XXX XXX XX'
                }
            ),
            'pin': TextInput(
                attrs={
                    'class': 'form-control',
                    'type': 'number',
                    'maxlength': 6,
                    'minvalue': 111111,
                    'placeholder': 'XXXXXX'
                }
            )
        }
    
class NewSaleForm(ModelForm):
    # class Meta:
    #     model=SalesReport
    #     fields="__all__"
    #     widgets={
    #         'shop_id': TextInput(
    #             attrs={
    #                 'class': 'form-control',
    #                 'placeholder': 'Shop ID'
    #             }
    #         ),
    #         'card_number': TextInput(
    #             attrs={
    #                 'class': 'form-control',
    #                 'placeholder': 'Ration Card Number'
    #             }
    #         )
    #     }
    pass

class NewCollectionForm(forms.Form):
    
    product=CharField(
        widget=TextInput(
            attrs={'class':'form-control', 'required':'required'}
        )
    )

    quantity=CharField(
        widget=NumberInput(
            attrs={'class':'form-control', 'required':'required'}
        )
    )

    card_number=CharField(
        widget=TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Ration Card Number',
            }
        )
    )
    shop_id=CharField(
        widget=TextInput(
            attrs={
            'class': 'form-control',
            'required': 'required'
        }
        )
    )

class ManageOrderForm(ModelForm):
    class Meta:
        model = Orders
        fields = '__all__'
