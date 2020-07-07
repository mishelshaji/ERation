from django.forms import forms, ModelForm, TextInput, Textarea, Select, CharField, PasswordInput, NumberInput
from django.contrib.auth.password_validation import validate_password
from eadmin.models import User
from . models import DeliveryStaff


class NewStaffForm(ModelForm):
    class Meta:
        model = DeliveryStaff
        exclude = ['id', 'shop']
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
            'staff_id': TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': '5CB387D65JCE25'

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
        }