from .models import Message, Review, Product, News, Offer, Comment, ReviewOfUser, Order, Profile_Of_User
from django.forms import ModelForm, TextInput, Select, TextInput, FileInput
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm


class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = ["task", "stars"]
        widgets = {
            "task": TextInput(attrs={
                'class': 'form-control fields',
            }),
            "stars": Select(choices=[(str(star), star) for star in range(1, 6)], attrs={
                'class': 'form-control'
            }),
        }

class ReviewProfileForm(ModelForm):
    class Meta:
        model = ReviewOfUser
        fields = ["task", "rating"]
        widgets = {
            "task": TextInput(attrs={
                'class': 'form-control fields',
            }),
            "rating": Select(choices=[(str(star), star) for star in range(1, 6)], attrs={
                'class': 'form-control fields'
            }),
        }


class Profile_Of_Form(ModelForm):
    class Meta:
        model = Profile_Of_User
        fields = ["bio", "avatar"]
        widgets = {
            "bio": TextInput(attrs={
                'class': 'form-control',
            }),
            "avatar":  FileInput(attrs={
                'class': 'form-control'
            }),
        }


class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = ["name", "description", "price", "image"]
        widgets = {
            "name": TextInput(attrs={
                'class': 'form-control',
            }),
            "description": TextInput(attrs={
                'class': 'form-control fields',
            }),
            "price": TextInput(attrs={
                'class': 'form-control',
            }),
            "image": FileInput(attrs={
                'class': 'form-control',
            }),
        }


class YieldForm(ModelForm):
    class Meta:
        model = Order
        fields = ["pnumber", "adress"]
        widgets = {
            "pnumber": TextInput(attrs={
                'class': 'form-control fields',
            }),
            "adress": TextInput(attrs={
                'class': 'form-control fields',
            }),
        }


class OfferForm(ModelForm):
    class Meta:
        model = Offer
        fields = ["price"]
        widgets = {
            "price": TextInput(attrs={
                'class': 'form-control',
                'placeholder': '   Ваш оффер'
            })
        }

# class AvatarForm(ModelForm):
#     class Meta:
#         model = Avatar
#         fields = ["image"]
#         widgets = {
#             "image": FileInput(attrs={
#                 'class': 'form-control',
#             })
#         }


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ["comment"]
        widgets = {
            "comment": TextInput(attrs={
                'class': 'form-control fields',
                'placeholder': 'Введите свой комментарий'
            })
        }


class MessageForm(ModelForm):
    class Meta:
        model = Message
        fields = ['text']
        widgets = {
            "text": TextInput(attrs={
                'class': 'form-control searchmessage',
                'placeholder': 'Введите текст сообщения'
            })
        }

class AccountCreationForm(UserCreationForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class':('form-control')})
        self.fields['password1'].widget.attrs.update({'class':('form-control')})        
        self.fields['password2'].widget.attrs.update({'class':('form-control')})

class SigninForm(AuthenticationForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class':('form-control')})
        self.fields['password'].widget.attrs.update({'class':('form-control')})     