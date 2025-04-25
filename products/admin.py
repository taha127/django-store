from django.contrib import admin

from products.models import Product, Comment


class CommentInline(admin.StackedInline):
    model = Comment
    extra = 0
    fields = ('author', 'body', 'active', 'stars',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'active',)
    inlines = [CommentInline, ]

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('product', 'author', 'body', 'active', 'stars',)
