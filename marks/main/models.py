from asyncio import SendfileNotAvailableError
from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone


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
        return f'/account/'

    # def __str__(self):
    #     return self.name


class Offer(models.Model):
    price = models.PositiveIntegerField()
    product = models.ForeignKey(Product, related_name='offers', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.price)


class Favorite(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.product)


class Message(models.Model):
    text = models.TextField()
    created_at = models.DateTimeField('created', default=timezone.now, blank=True)
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='sent_messages', on_delete=models.CASCADE)
    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='received_messages', on_delete=models.CASCADE)
    
    class Meta:
        constraints = [
            models.CheckConstraint(
                name="prevent_self_message",
                check=~models.Q(sender=models.F('recipient'))
            )
        ]







