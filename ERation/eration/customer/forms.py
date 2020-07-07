from django.forms import forms, ModelForm, CharField, TextInput, EmailInput, NumberInput, Textarea, Select
from .models import Customer
from eadmin.models import Complaints

class CustomerLoginForm(forms.Form):
    card_no = CharField(
        label='Card Number',
        help_text='Your ration card number',
        min_length=5,
        max_length=20,
        widget=TextInput(
            attrs={
                'class':'form-control',
                'required':'true'
            }
        )
    )

    phone = CharField(
        label='Phone',
        min_length=10,
        max_length=10,
        help_text='Your 10 digit mobile number',
        widget=NumberInput(
            attrs={
                'class':'form-control',
                'required':'true',
                'minlength': 10,
                'maxlength':10
            }
        )
    )

class NewCustomerForm(ModelForm):
    class Meta:
        fields = '__all__'
        model = Customer
        widgets = {
            'name': TextInput(
                attrs={
                    'class': 'form-control',
                }
            ),
            'phone': NumberInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': '10 digit mobile number'
                }
            ),
            'address': Textarea(
                attrs={
                    'class': 'form-control',
                }
            ),
            'card_number': TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': '10 digit card number'
                }
            ),
            'card_type': Select(
                attrs={
                    'class': 'form-control',
                }
            ),
            'shop_id': Select(
                attrs={
                    'class': 'form-control',
                }
            ),
            'email': EmailInput(
                attrs={
                    'class': 'form-control',
                }
            ),
            'aadhar': NumberInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': '12 to 16 digits'
                }
            ),
        }

class NewComplaintForm(ModelForm):
    """Form definition for NewComplaint."""

    class Meta:
        """Meta definition for NewComplaintform."""

        model = Complaints
        exclude = ('reply',)
        widgets={
            'customer': TextInput(attrs={
                'type': 'hidden',
                'value': '1'
            })
        }