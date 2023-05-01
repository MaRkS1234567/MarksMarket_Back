from asyncio import SendfileNotAvailableError
from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from django.contrib.auth.models import User


class Review(models.Model):
    task = models.TextField('Reviews')
    stars = models.PositiveSmallIntegerField('Stars', validators=[MinValueValidator(1), MaxValueValidator(5)])
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.task

    def stars_range(self):
        """ Used in templates to render self.stars number of stars """
        return range(self.stars)

    class Meta:
        constraints = [
            models.CheckConstraint(
                name='valid_stars_range',
                check=models.Q(stars__gt=0) & models.Q(stars__lt=6)
            ),
        ]


class News(models.Model):
    news = models.TextField()
    source = models.CharField(max_length=30)
    imagenews = models.ImageField(upload_to='products/')

    def __str__(self):
        return self.news


class Comment(models.Model):
    comment = models.TextField()
    news = models.ForeignKey(News, related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.comment)


class Product(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=15)
    description = models.TextField()
    price = models.PositiveIntegerField()
    image = models.ImageField(upload_to='products/')

    def get_absolute_url(self):
        return f'/account'

    def __str__(self):
        return self.name
    

class Yield(models.Model):
    name = models.CharField(max_length=15)
    description = models.TextField()
    price = models.PositiveIntegerField()
    image = models.ImageField(upload_to='products/')

    def get_absolute_url(self):
        return f'/account'

    def __str__(self):
        return self.name


class Offer(models.Model):
    price = models.PositiveIntegerField()
    product = models.ForeignKey(Product, related_name='offers', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.price)


class Favorite(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)
    yields = models.ForeignKey(Yield, on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)


class ReviewOfUser(models.Model):
    task = models.TextField('Reviews')
    rating = models.PositiveIntegerField()
    profile_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='profile_user', on_delete=models.CASCADE)
    comment_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='comment_user', on_delete=models.CASCADE)


    def __str__(self):
        return str(self.profile_user)

    def rating_range(self):
        return range(self.rating)

    class Meta:
        constraints = [
            models.CheckConstraint(
                name='valid_rating_range',
                check=models.Q(rating__gt=0) & models.Q(rating__lt=6)
            ),
        ]

class Message(models.Model):
    text = models.TextField()
    created_at = models.DateTimeField('created', default=timezone.now, blank=True)
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='sent_messages', on_delete=models.CASCADE)
    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='received_messages', on_delete=models.CASCADE)
    
    def datepublished(self):
            return self.created_at.strftime('%T')


    class Meta:
        constraints = [
            models.CheckConstraint(
                name="prevent_self_message",
                check=~models.Q(sender=models.F('recipient'))
            )
        ]


class Order(models.Model):
    yields = models.ForeignKey(Yield, on_delete=models.CASCADE)
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    pnumber =  models.PositiveBigIntegerField('Phone number')
    adress = models.TextField()

    def get_absolute_url(self):
        return f'/account'

    def __str__(self):
        return str(self.customer)
    
# class Avatar(models.Model):
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#     image = models.ImageField(upload_to='avatars/')

#     def __str__(self):
#         return str(self.user)

class Profile_Of_User(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    avatar = models.ImageField(default='default.png', upload_to='avatars/', null=True, blank=True)
    bio = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.user.username





