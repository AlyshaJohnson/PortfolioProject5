from rest_framework import permissions, filters, generics
from rest_framework.response import Response
from django.http import Http404
from .models import Book, Genre, Tags
from .serializers import LibrarySerializer
from django.db.models import Count


class LibraryList(generics.ListCreateAPIView):
    serializer_class = LibrarySerializer
    queryset = Book.objects.annotate(
        books_count=Count('title', distinct=True),
    )
    filter_backends = [
        filters.OrderingFilter,
        filters.SearchFilter,
    ]
    search_fields = [
        'book__title',
        'book__author',
        'book__genre'
    ]
    ordering_fields = [
        'books_count',
    ]

    def get_permissions(self):
        if self.request.method in ['POST']:
            permission_classes = [permissions.IsAdminUser]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        serializer.save()


class LibraryDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = LibrarySerializer
    queryset = Book.objects.annotate(
        books_count=Count('title', distinct=True),
    )

    def get_permissions(self):
        if self.request.method in ['PUT', 'DELETE']:
            permission_classes = [permissions.IsAdminUser]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]
