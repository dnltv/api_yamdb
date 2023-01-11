from django.contrib import admin

from .models import Comment, Review


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    model = Review
    fields = ('title', 'text', 'author', 'score', 'pub_date')
    search_fields = ('title', 'text', 'author', 'score', 'pub_date')
    list_filter = ('title', 'text', 'author', 'score', 'pub_date')
    empty_value_display = '-пусто-'


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    model = Comment
    fields = ('review', 'author', 'text', 'pub_date')
    search_fields = ('review', 'author', 'text', 'pub_date')
    list_filter = ('review', 'author', 'text', 'pub_date')
    empty_value_display = '-пусто-'
