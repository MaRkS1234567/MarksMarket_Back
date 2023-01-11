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


from .models import Review, News, Product, Favorite, Message
from .forms import ReviewForm, ProductForm, OfferForm, CommentForm, MessageForm, AccountCreationForm, SigninForm


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


def shop(request):
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
                return redirect('shop')
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
            return render(request, 'main/shop.html', context)

        elif form_type == 'product_form':
            product_form = ProductForm(request.POST, request.FILES)

            if product_form.is_valid():
                product = product_form.save(commit=False)
                product.user = request.user
                product.save()
                return redirect('shop')

            context['product_form'] = product_form
            return render(request, 'main/shop.html', context)

    return render(request, 'main/shop.html', context)


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


def account(request):

    favorites = Favorite.objects.filter(user=request.user).select_related('product')
    products = Product.objects.order_by('-id').prefetch_related('offers').filter(user=request.user)
    paginator = Paginator(products, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    if request.method == 'POST':
        form_type = request.POST.get('form_type')

        if form_type == 'offer_form':
            offer_form = OfferForm(request.POST)

            if offer_form.is_valid():
                offer = offer_form.save(commit=False)
                # TODO: product validation.
                product_id = request.POST.get('products')
                offer.product = Product.objects.get(id=int(product_id))
                offer.user = request.user
                offer.save()
                return redirect('account')

            return render(request, 'main/account.html', {'offer_form': offer_form, 'page': page, 'favorites': favorites, 'products': products})

    context = {
        'offer_form': OfferForm(),
        'page': page,
        'favorites': favorites,
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

    context = {
        'product': product,
        'offer_form': OfferForm()
    }

    if request.method == 'POST':
        form_type = request.POST.get('form_type')

        if form_type == 'offer_form':
            offer_form = OfferForm(request.POST)

            if offer_form.is_valid():
                offer = offer_form.save(commit=False)
                offer.news = product
                offer.user = request.user
                offer.save()
                return redirect('product', product_id=product_id)

            context['offer_form'] = offer_form
            return render(request, 'main/product.html', context)

    return render(request, 'main/product.html', context)


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

User = get_user_model()

def chat(request, username):
    sender = request.user
    recipient = get_object_or_404(User, username=username)
    messages = Message.objects.filter(Q(sender=sender, recipient=recipient) | Q(sender=recipient, recipient=sender)
                                      ).order_by('created_at')
    form = MessageForm(request.POST)

    if request.method == 'POST':
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = sender
            message.recipient = recipient
            message.save()
            return redirect('chat', username=username)

    context = {
        'recipient': recipient,
        'sender': sender,
        # can not be named messages, because of django.messages rendering in base.html
        'chat_messages': messages,
        'form': form,
    }

    return render(request, 'main/chat.html', context)

def chats(request: HttpRequest):
    users = User.objects.filter(
        Q(sent_messages__recipient=request.user) | 
        Q(received_messages__sender=request.user)
    ).distinct()

    context = {
        'users': users
    }

    return render(request, 'main/chats.html', context)


