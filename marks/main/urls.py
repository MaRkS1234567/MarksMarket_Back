from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('about-us', views.about, name='about'),
    path('login', views.signin, name='login'),
    path('register', views.register, name='register'),
    path('logout', views.signout, name='logout'),
    path('help', views.help_view, name='help'),
    path('account', views.account, name='account'),
    path('shop', views.shop, name='shop'),
    path('note', views.note, name='note'),
    path('news/<int:news_id>', views.news, name='news'),
    path('product/<int:product_id>', views.product, name='product'),
    path('favorite/<int:product_id>', views.favorite, name='favorite'),
    path('chats', views.chats, name='chats'),
    path('chat/<str:username>', views.chat, name='chat'), 
    path('product/<int:pk>/update', views.ProductUpdateView.as_view(), name='product-update'),
    path('product/<int:pk>/delete', views.ProductDeleteView.as_view(), name='product-delete')
]
