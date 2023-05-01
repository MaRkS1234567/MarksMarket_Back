from pyexpat.errors import messages
from django.contrib import admin
from .models import Review, Product, News, Offer, Comment, Message, ReviewOfUser, Yield, Favorite, Profile_Of_User
# from django.contrib.auth import get_user_model

# User = get_user_model()

admin.site.register(Review)
admin.site.register(ReviewOfUser)
admin.site.register(Offer)
admin.site.register(Comment)
admin.site.register(Message)
admin.site.register(Yield)
admin.site.register(Favorite)
admin.site.register(Profile_Of_User)


class OfferInline(admin.TabularInline):
    model = Offer


class CommentInline(admin.TabularInline):
    model = Comment


# class ProfileInline(admin.TabularInline):
#     model = ReviewOfUser


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [OfferInline]


# @admin.(User)
# class UserAdmin(admin.ModelAdmin):
#     inlines = [ProfileInline]


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    inlines = [CommentInline]
