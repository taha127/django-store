from django.contrib import admin
from products.models import Product, Comment
from jalali_date.admin import ModelAdminJalaliMixin


class CommentInline(admin.StackedInline):
    model = Comment
    extra = 0
    fields = ('author', 'body', 'active', 'stars',)


@admin.register(Product)
class ProductAdmin(ModelAdminJalaliMixin, admin.ModelAdmin):
    list_display = ('title', 'price', 'active',)
    inlines = [CommentInline, ]


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('product', 'author', 'body', 'active', 'stars',)
