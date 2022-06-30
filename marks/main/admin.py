from django.contrib import admin
from .models import Review, Product, News, Offer, Comment

admin.site.register(Review)
admin.site.register(Offer)
admin.site.register(Comment)


class OfferInline(admin.TabularInline):
    model = Offer


class CommentInline(admin.TabularInline):
    model = Comment


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [OfferInline]


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    inlines = [CommentInline]
