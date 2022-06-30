from .models import Review, Product, News, Offer, Comment
from django.forms import ModelForm, Textarea, Select, TextInput


class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = ["task", "stars"]
        widgets = {
            "task": Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Введите отзыв'
            }),
            "stars": Select(choices=[(str(star), star) for star in range(1, 6)]),
        }


class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = ["name", "description", "price", "image"]
        widgets = {
            "name": TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите имя товара'
            }),
            "description": Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Введите описание'
            }),
            "price": TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите цену'
            }),
            "image": TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Выбрете файл'
            })
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