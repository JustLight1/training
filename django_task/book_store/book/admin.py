from django.contrib import admin

from book.models import Book


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'author', 'count')
    search_fields = ('id', 'title', 'author')
    autocomplete_fields = ('author',)
