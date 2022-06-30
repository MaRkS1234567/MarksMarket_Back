from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator


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
        verbose_name = 'request'
        verbose_name_plural = 'requests'
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
    news = models.ForeignKey(News, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.comment)


class Product(models.Model):
    name = models.CharField(max_length=30)
    description = models.TextField()
    price = models.PositiveIntegerField()
    image = models.ImageField(upload_to='products/')

    def __str__(self):
        return self.name


class Offer(models.Model):
    price = models.PositiveIntegerField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.price)


class Favorite(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.product)








