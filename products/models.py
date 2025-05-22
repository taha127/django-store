from django.db import models
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils import timezone
from ckeditor.fields import RichTextField
from django.utils.translation import gettext_lazy as _


class Product(models.Model):
    title = models.CharField(max_length=100, verbose_name=_("title"))
    description = RichTextField(verbose_name=_("Description"))
    short_description = models.TextField(verbose_name=_("Short Description"), blank=True)
    price = models.PositiveIntegerField(default=0, verbose_name=_("price"))
    active = models.BooleanField(default=True, verbose_name=_("active"))
    image = models.ImageField(upload_to="products/product_image/", verbose_name=_("Image"), blank=True)
    datetime_created = models.DateTimeField(default=timezone.now, verbose_name=_("Date Time Created"))
    datetime_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('product_detail', kwargs={'pk': self.pk})


class ActiveCommentManager(models.Manager):
    def get_queryset(self):
        return super(ActiveCommentManager, self).get_queryset().filter(active=True)


class Comment(models.Model):
    PRODUCT_STARS = [
        ('1', 'very bad'),
        ('2', 'bad'),
        ('3', 'normal'),
        ('4', 'good'),
        ('5', 'perfect'),
    ]
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='comments')
    body = models.TextField(verbose_name=_('Comment Text'))
    stars = models.CharField(max_length=10, choices=PRODUCT_STARS, verbose_name=_('What is your score?'))
    datetime_created = models.DateTimeField(auto_now_add=True)
    datetime_modified = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    # Manager
    objects = models.Manager()  # Default manager
    active_comments = ActiveCommentManager()  # Custom manager

    def get_absolute_url(self):
        return reverse('product_detail', kwargs={'pk': self.product.id})
