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
    path('trade', views.trade, name='trade'),
    path('shop', views.shop, name='shop'),
    path('note', views.note, name='note'),
    path('chats', views.chats, name='chats'),
    path('news/<int:news_id>', views.news, name='news'),
    path('product/<int:product_id>', views.product, name='product'),
    path('yields/<int:yield_id>', views.yields , name='yields'),
    path('profile/<str:username>', views.profile, name='profile'),
    path('favorite/<int:product_id>', views.favorite, name='favorite'),
    path('favorite_for_yields/<int:yield_id>', views.favorite_for_yields, name='favorite_for_yields'),
    path('chat/<str:username>', views.chat, name='chat'), 
    path('product/<int:pk>/update', views.ProductUpdateView.as_view(), name='product-update'),
    path('product/<int:pk>/delete', views.ProductDeleteView.as_view(), name='product-delete')
]
