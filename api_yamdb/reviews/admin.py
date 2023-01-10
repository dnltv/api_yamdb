from django.contrib import admin

from api_yamdb.reviews.models import Review


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    model = Review
    fields = ('title', 'text', 'author', 'score', 'pub_date')
    search_fields = ('title', 'text', 'author', 'score', 'pub_date')
    list_filter = ('title', 'text', 'author', 'score', 'pub_date')
    empty_value_display = '-пусто-'
