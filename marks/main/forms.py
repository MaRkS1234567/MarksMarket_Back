from .models import Message, Review, Product, News, Offer, Comment
from django.forms import ModelForm, Textarea, Select, TextInput, FileInput
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm


class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = ["task", "stars"]
        widgets = {
            "task": Textarea(attrs={
                'class': 'form-control',
            }),
            "stars": Select(choices=[(str(star), star) for star in range(1, 6)], attrs={
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
            "description": Textarea(attrs={
                'class': 'form-control',
            }),
            "price": TextInput(attrs={
                'class': 'form-control',
            }),
            "image": FileInput(attrs={
                'class': 'form-control',
            }),
        }


class OfferForm(ModelForm):
    class Meta:
        model = Offer
        fields = ["price"]
        widgets = {
            "price": TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите свой оффер'
            })
        }


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ["comment"]
        widgets = {
            "comment": Textarea(attrs={
                'class': 'form-control',
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