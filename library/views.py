from rest_framework import permissions, filters
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import Http404
from .models import Book, Genre, Tags
from .serializers import LibrarySerializer
from django.db.models import Count


class LibraryList(APIView):
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
            return [permissions.IsAdminUser()]
        return [permissions.IsAuthenticated()]

    def get(self, request):
        books = Book.objects.all()
        serializer = LibrarySerializer(books, many=True)
        self.check_object_permissions(self.request, books)
        return Response(serializer.data)

    def post(self, request):
        serializer = LibrarySerializer(
            data=request.data, context={'request': request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data, status=status.HTTP_201_CREATED
            )
        return Response(
            serializer.errors, status=status.HTTP_400_BAD_REQUEST
        )


class LibraryDetail(APIView):
    serializer_class = LibrarySerializer
    permission_classes = [permissions.IsAdminUser]

    def get_permissions(self):
        if self.request.method in ['PUT', 'DELETE']:
            return [permissions.IsAdminUser()]
        return [permissions.IsAuthenticated()]

    def get_object(self, pk):
        try:
            book = Book.objects.get(pk=pk)
            return book
        except Book.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        book = self.get_object(pk)
        serializer = LibrarySerializer(book)
        return Response(serializer.data)

    def put(self, request, pk):
        book = self.get_object(pk)
        serializer = LibrarySerializer(book, data=request.data)
        self.check_object_permissions(self.request, books)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        book = self.get.object(pk)
        book.delete()
        return Response(
            status=status.HTTP_204_NO_CONTENT
        )
