from rest_framework import serializers
from .models import Book


class LibrarySerializer(serializers.ModelSerializer):
    def validate_cover(self, value):
        if value.size > 2 * 1024 * 1024:
            raise serializers.ValidationError('Image size larger than 2MB!')
        if value.image.height > 4096:
            raise serializers.ValidationError(
                'Image height larger than 4096px!'
            )
        if value.image.width > 4096:
            raise serializers.ValidationError(
                'Image width larger than 4096px!'
            )
        return value

    class Meta:
        model = Book
        fields = [
            'id', 'title', 'author', 'ISBN', 'publisher',
            'published', 'blurb', 'series_title',
            'series_book_no', 'series_links', 'cover',
        ]
