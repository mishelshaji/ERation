from django.forms import forms, ModelForm, TextInput, Textarea, Select, CharField, PasswordInput, NumberInput
from django.contrib.auth.password_validation import validate_password
from .models import User, Cards, Products, Allocations, Complaints


class LoginForm(ModelForm):
    password = CharField(
        label = 'password', 
        max_length=15,
        # validators=[validate_password],
        widget=PasswordInput(
            attrs={
                'class': 'form-control',
                'required': 'required'
            }
        )
    )

    #? Disable uniqueness checking
    def validate_unique(x):
        return False

    class Meta:
        model = User
        fields = ('email',)
        widgets = {
            'email': TextInput(
                attrs={
                    'class': 'form-control',
                    'type': 'email',
                    'required': 'required',
                    'placeholder': 'someone@example.com'
                }
            ),
            # 'password': TextInput(attrs={
            #     'class': 'form-control',
            #     'type': 'password',
            #     'required': 'required'
            # })
        }

class NewCardForm(ModelForm):
    class Meta:
        model = Cards
        fields = '__all__'
        widgets = {
            'card_name': TextInput(
                attrs={
                    'class': 'form-control',
                    'required': 'required',
                    'placeholder': 'type here...',
                    'minlength': 3,
                }
            )
        }


class NewProductForm(ModelForm):
    class Meta:
        model=Products
        fields='__all__'
        widgets={
            'name': TextInput(
                attrs={
                    'class': 'form-control',
                    'required': 'required'
                }
            ),
            'unit': Select(
                attrs={
                    'class': 'form-control',
                    'required': 'required'
                }
            ),
            'details': Textarea(
                attrs={
                    'class': 'form-control'
                }
            ),
            'price': NumberInput(
                attrs={
                    'class': 'form-control'
                }
            )
        }

class NewAllocationForm(ModelForm):
    class Meta:
        model=Allocations
        fields="__all__"
        widgets={
            'card_name': Select(
                attrs={
                    'class': 'form-control',
                    'required': 'required'
                }
            ),
            'product': Select(
                attrs={
                    'class': 'form-control',
                    'required': 'required'
                }
            ),
            'quantity': NumberInput(
                attrs={
                    'class': 'form-control',
                    'required': 'required'
                }
            )
        }

class NewComplaintForm(ModelForm):
    """Form definition for NewComplaint."""

    class Meta:
        """Meta definition for NewComplaintform."""

        model = Complaints
        exclude = ('customer',)
