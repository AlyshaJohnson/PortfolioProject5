from rest_framework import serializers
from .models import Review


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = [
            'id', 'book', 'title', 'description', 'date_added',
            'book_started', 'book_finished', 'rating', 'tags',
            'visibility',
        ]
