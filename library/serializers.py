from rest_framework import serializers
from .models import Book


class LibrarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = [
            'id', 'title', 'author', 'ISBN', 'publisher',
            'published', 'blurb', 'series_title',
            'series_book_no', 'series_links'
        ]
