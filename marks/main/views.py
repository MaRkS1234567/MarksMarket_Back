from re import U
from this import s
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib import messages
from django.db.models import Avg, Max, Min, Q
from django.core.paginator import Paginator
from django.http import Http404, HttpRequest, HttpResponse
from django.views.generic import UpdateView, DeleteView


from .models import Review, News, Product, Favorite, Message, ReviewOfUser, Yield, Order, Profile_Of_User, Offer
from .forms import ReviewForm, ProductForm, OfferForm, CommentForm, MessageForm, AccountCreationForm, SigninForm, ReviewProfileForm, YieldForm, Profile_Of_Form

User = get_user_model()

def alltimefunc(request):
    profile_of_user = Profile_Of_User.objects.get(user = request.user)
    return profile_of_user


def index(request):
    news = News.objects.order_by('-id').prefetch_related('comments')
    paginator = Paginator(news, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    if request.method == 'POST':
        form_type = request.POST.get('form_type')

        if form_type == 'comment_form':
            comment_form = CommentForm(request.POST)

            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                # TODO: product validation.
                news_id = request.POST.get('product')
                comment.news = News.objects.get(id=int(news_id))
                comment.user = request.user
                comment.save()
                return redirect('')

            return render(request, 'main/index.html',
                          {'comment_form': comment_form, 'page': page})
    context = {
        'comment_form': CommentForm(),
        'page': page
    }

    return render(request, 'main/index.html', context)


def trade(request):
    min_price = Product.objects.aggregate(Min("price"))['price__min']
    max_price = Product.objects.aggregate(Max("price"))['price__max']

    query = request.GET.get("q")
    min_ = request.GET.get("min")
    max_ = request.GET.get("max")

    products = Product.objects.order_by('-id').prefetch_related('offers')

    if query is not None:
        products = products.filter(name__icontains=query)

    if min_ is not None and min_.isdigit():
        products = products.filter(price__gte=min_)

    if max_ is not None and max_.isdigit():
        products = products.filter(price__lte=max_)

    paginator = Paginator(products, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    context = {
        'min_price': min_price,
        'max_price': max_price,
        'page': page,
        'product_form': ProductForm(),
        'offer_form': OfferForm(),
    }

    if request.method == 'POST':
        form_type = request.POST.get('form_type')

        if form_type == 'offer_form':
            offer_form = OfferForm(request.POST)

            if offer_form.is_valid():
                offer = offer_form.save(commit=False)
                product_id = request.POST.get('product')
                offer.product = Product.objects.get(id=int(product_id))
                offer.user = request.user
                offer.save()
                return redirect('trade')
                # error = ''
                # if product_id is None:
                #     error = 'No product_id'
                #
                # if not error:
                #     try:
                #         product_id = int(product_id)
                #     except ValueError:
                #         error = 'product_id must be an integer'
                #
                # if not error:
                #     product = Product.objects.filter(id=product_id).first()
                #     if product is None:
                #         error = 'Product with id "{product_id}" was not found.'
                #
                # if not error:
                #     offer.product = product
            context['offer_form'] = offer_form
            return render(request, 'main/trade.html', context)

        elif form_type == 'product_form':
            product_form = ProductForm(request.POST, request.FILES)

            if product_form.is_valid():
                product = product_form.save(commit=False)
                product.user = request.user
                product.save()
                return redirect('trade')

            context['product_form'] = product_form
            return render(request, 'main/trade.html', context)

    return render(request, 'main/trade.html', context)


# class NewsDetailView(DetailView):
#     model = Product
#     template_name = 'news/details_view.html'
#     context_object_name = 'article'


class ProductUpdateView(UpdateView):
    model = Product
    template_name = 'main/update.html'
    form_class = ProductForm


class ProductDeleteView(DeleteView):
    model = Product
    success_url = '/account'
    template_name = 'main/delete.html'


class UserDeleteView(DeleteView):
    model = User
    success_url = '/shop'
    template_name = 'main/user_delete.html'


class FavoriteDeleteView(DeleteView):
    model = Favorite
    success_url = '/account'
    template_name = 'main/delete_favorite.html'


class OrderUpdateView(UpdateView):
    model = Order
    template_name = 'main/update_order.html'
    form_class = YieldForm


class OrderDeleteView(DeleteView):
    model = Order
    success_url = '/account'
    template_name = 'main/delete_order.html'


def favourites(request):
    favorites = Favorite.objects.filter(user=request.user).select_related('product')
    favorites_for_yield = Favorite.objects.filter(user=request.user).select_related('yields')

    context = {
        'favorites': favorites,
        'favorites_for_yield': favorites_for_yield,
    }

    return render(request, 'main/favourites.html', context)



def account(request):

    profile_ = ReviewOfUser.objects.order_by('-id').filter(profile_user = request.user)
    try:
        profile_of_user = Profile_Of_User.objects.get(user = request.user)
    except Profile_Of_User.DoesNotExist:
        profile_of_user = Profile_Of_User.objects.get_or_create(user = request.user)
    profile_of_user = Profile_Of_User.objects.get(user = request.user)
    average = round(ReviewOfUser.objects.aggregate(Avg('rating'))['rating__avg'])
    paginator_ = Paginator(profile_, 5)
    page_number_ = request.GET.get('page_')
    page_ = paginator_.get_page(page_number_)
    favorites = Favorite.objects.filter(user=request.user).select_related('product').order_by('-id')[:4]
    favorites_for_yield = Favorite.objects.filter(user=request.user).select_related('yields').order_by('-id')[:4]
    products = Product.objects.order_by('-id').prefetch_related('offers').filter(user=request.user)[:4]
    paginator = Paginator(favorites, 3)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    orders = Order.objects.order_by('-id').filter(customer = request.user).select_related('yields')[:4]

    try:
        profile = request.user.profile_of_user
    except Profile_Of_User.DoesNotExist:
        profile = Profile_Of_User(user=request.user)

    if request.method == 'POST':
        profile_form = Profile_Of_Form(request.POST, request.FILES, instance=profile)
        if profile_form.is_valid():
            profile_form.save()
            return redirect('account')
    else:
        profile_form = Profile_Of_Form(instance=profile)

    # if request.method == 'POST':

    #     form_for_user = Profile_Of_Form(request.POST, request.FILES)

    #     if form_for_user.is_valid():
    #         profiles_for_user = form_for_user.save(commit=False)
    #         profiles_for_user.user = request.user
    #         profiles_for_user.save()
    #         return redirect('account')

    context = {
        'offer_form': OfferForm(),
        'profile_form': Profile_Of_Form(),
        'orders': orders,
        'profile_': profile_,
        'profile_of_user': profile_of_user,
        'page_': page_,
        'average': average,
        'page': page,
        'favorites': favorites,
        'favorites_for_yield': favorites_for_yield,
        'products': products
    }

    return render(request, 'main/account.html', context)


def news(request, news_id):
    news = get_object_or_404(
        News.objects.prefetch_related('comments'), id=news_id)

    context = {
        'news': news,
        'comment_form': CommentForm()
    }

    if request.method == 'POST':
        form_type = request.POST.get('form_type')

        if form_type == 'comment_form':
            comment_form = CommentForm(request.POST)

            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.news = news
                comment.user = request.user
                comment.save()
                return redirect('news', news_id=news_id)

            context['comment_form'] = comment_form
            return render(request, 'main/news.html', context)

    return render(request, 'main/news.html', context)


def product(request, product_id):
    product = get_object_or_404(
        Product.objects.prefetch_related('offers'), id=product_id)
    # favorite = Favorite.objects.get(product = product, user=request.user)
    offers = Offer.objects.filter(user = request.user, product = product)

    context = {
        'offers': offers,
        'product': product,
        # 'favorite': favorite,
        'offer_form': OfferForm()
    }

    if request.method == 'POST':
        form_type = request.POST.get('form_type')

        if form_type == 'offer_form':
            offer_form = OfferForm(request.POST)

            if offer_form.is_valid():
                offer = offer_form.save(commit=False)
                offer.product = product
                offer.user = request.user
                offer.save()
                return redirect('product', product_id=product_id)

            context['offer_form'] = offer_form
            return render(request, 'main/product.html', context)

    return render(request, 'main/product.html', context)


def yields(request, yield_id):
    yields = get_object_or_404(Yield, id=yield_id)
    # favorite_for_yield = Favorite.objects.get(yields=yields, user=request.user)

    context = {
        'yields': yields,
        # 'favorite_for_yield': favorite_for_yield,
    }
    return render(request, 'main/yield.html', context)


def about(request):
    reviews = Review.objects.order_by('-id')
    paginator = Paginator(reviews, 5)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    average = round(Review.objects.aggregate(Avg('stars'))['stars__avg'])

    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect('login')

        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.save()
            return redirect('about')
        else:
            return render(request, 'main/about.html', {'form': form, 'page': page, 'average': average})

    form = ReviewForm()
    context = {
        'form': form,
        'page': page,
        'average': average
    }

    return render(request, 'main/about.html', context)


def signin(request):
    if request.method == 'POST':
        form = SigninForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            messages.success(
                request, f'Вы успешно вошли в свой аккаунт, {form.data["username"]} !')
            return redirect('home')
        else:
            return render(request, 'main/login.html', {'form': form})

    form = SigninForm()
    context = {'form': form}

    return render(request, 'main/login.html', context)


def register(request):
    if request.method == 'POST':
        form = AccountCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request, f'Вы успешно вошли в аккакнт,{form.data["username"]}!')
            return redirect('login')
        return render(request, 'main/register.html', {'form': form})
    form = AccountCreationForm()
    context = {
        'form': form,
    }
    return render(request, 'main/register.html', context)


def note(request):
    return render(request, 'main/note.html')


def signout(request):
    logout(request)
    return redirect('home')


def help_view(request):
    return render(request, 'main/help.html')


def favorite(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    user = request.user

    Favorite.objects.get_or_create(product=product, user=user)
    return redirect('account')


def favorite_for_yields(request, yield_id):
    yields = get_object_or_404(Yield, id=yield_id)
    user = request.user

    Favorite.objects.get_or_create(yields=yields, user=user)
    return redirect('account')


User = get_user_model()

def chat(request: HttpRequest, username):
    users = User.objects.filter(
        Q(sent_messages__recipient=request.user) | 
        Q(received_messages__sender=request.user)
    ).distinct()
     
    sender = request.user
    recipient = get_object_or_404(User, username=username)
    messages = Message.objects.filter(Q(sender=sender, recipient=recipient) | Q(sender=recipient, recipient=sender)).order_by('created_at')
    form = MessageForm(request.POST)
    profile_of_sender = Profile_Of_User.objects.get(user = recipient)

    if request.method == 'POST':
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = sender
            message.recipient = recipient
            message.save()
            return redirect('chat', username=username)

    context = {
        'users': users,
        'recipient': recipient,
        'profile_of_sender': profile_of_sender,
        'sender': sender,
        'chat_messages': messages,
        'form': form,
    }

    return render(request, 'main/chat.html', context)

def chats(request: HttpRequest):
    users = User.objects.filter(
        Q(sent_messages__recipient=request.user) | 
        Q(received_messages__sender=request.user)
    ).distinct()
    sender = request.user
    # recipient = get_object_or_404(User)
    messages = Message.objects.filter(sender = sender)[:1]

    context = {
        'users': users,
        'chat__messages': messages
    }

    return render(request, 'main/chats.html', context)

def shop(request):
    min_price = Yield.objects.aggregate(Min("price"))['price__min']
    max_price = Yield.objects.aggregate(Max("price"))['price__max']

    query = request.GET.get("q")
    min_ = request.GET.get("min")
    max_ = request.GET.get("max")

    yields = Yield.objects.order_by('-id')

    yield_id = request.POST.get('yields')   


    if query is not None:
        yields = yields.filter(name__icontains=query)

    if min_ is not None and min_.isdigit():
        yields = yields.filter(price__gte=min_)

    if max_ is not None and max_.isdigit():
        yields = yields.filter(price__lte=max_)

    paginator = Paginator(yields, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    context = {
        'min_price': min_price,
        'max_price': max_price,
        'page': page,
    }

    return render(request, 'main/shop.html', context)


def profile(request, username):
    profile_user = get_object_or_404(User, username=username)
    profile_Of_user = Profile_Of_User.objects.get(user = profile_user)
    profile_ = ReviewOfUser.objects.order_by('-id').filter(profile_user = profile_user)
    paginator = Paginator(profile_, 5)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    products = Product.objects.order_by('-id').prefetch_related('offers').filter(user = profile_user)
    paginator_ = Paginator(products, 5)
    page_number_ = request.GET.get('page_')
    page_ = paginator_.get_page(page_number_)
    average = round(ReviewOfUser.objects.aggregate(Avg('rating'))['rating__avg'])
    user_ = get_object_or_404(User, username=username)


    form = ReviewProfileForm(request.POST)

    if request.method == 'POST':
        if form.is_valid():
            profile = form.save(commit=False)
            profile.comment_user = request.user
            profile.profile_user = profile_user
            profile.save()
            return redirect('profile', username=username)
        else:
            return render(request, 'main/profile.html', {'profile_': profile_ , 'form': form, 'page': page,'average': average,'products': products,'user_': user_,'porfiles': profiles})

    context = {
        'profile_Of_user': profile_Of_user,
        'profile_': profile_ ,
        'form': form,
        'page': page,
        'page_': page_,
        'average': average,
        'products': products,
        'user_': user_,
    }

    return render(request, 'main/profile.html', context)


def order(request, yield_id):
    yields = get_object_or_404(Yield, id=yield_id)
    form = YieldForm(request.POST)

    if request.method == 'POST':
        if form.is_valid():
            yields_ = form.save(commit=False)
            yields_.customer = request.user
            yields_.yields = yields
            yields_.save()
            return redirect('account')
        else:
            return render(request, 'main/shop.html', {'yields': yields, 'form': form})

    context = {
        'yields': yields,
        'form': form
    }

    return render(request, 'main/order.html', context)


def my_products(request):
    products = Product.objects.order_by('-id').prefetch_related('offers').filter(user=request.user)
    context = {
        'products': products
    }
    return render(request, 'main/my_products.html', context)


def my_orders(request):
    orders = Order.objects.order_by('-id').filter(customer = request.user).select_related('yields')
    context = {
        'orders': orders
    }
    return render(request, 'main/my_orders.html', context)
