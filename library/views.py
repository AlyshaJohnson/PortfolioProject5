from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import Http404
from .models import Book, Genre, Tags
from .serializers import LibrarySerializer


class LibraryList(APIView):
    def get(self, request):
        books = Book.objects.all()
        serializer = LibrarySerializer(books, many=True)
        return Response(serializer.data)


class LibraryDetail(APIView):
    serializer_class = LibrarySerializer()

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
        serializer = LibrarySerializer(book, date=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
