from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import Http404
from .models import Review
from .serializers import ReviewSerializer
from whirl.permissions import IsOwnerOrReadOnly, IsLibrarianOrUser


class ReviewList(APIView):
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request):
        reviews = Review.objects.all()
        serializer = ReviewSerializer(
            reviews, many=True, context={'request': request}
        )
        return Response(serializer.data)

    def post(self, request):
        serializer = ReviewSerializer(
            data=request.data, context={'request': request}
        )
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(
                serializer.data, status=status.HTTP_201_CREATED
            )
        return Response(
            serializer.errors, status=status.HTTP_400_BAD_REQUEST
        )


class ReviewDetailList(APIView):
    serializer_class = ReviewSerializer
    permission_classes = [
        IsOwnerOrReadOnly,
        IsLibrarianOrUser,
        permissions.IsAuthenticatedOrReadOnly,
        ]

    def get_object(self, pk):
        try:
            review = Review.objects.get(pk=pk)
            return review
        except Review.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        review = self.get_object(pk)
        serializer = ReviewSerializer(review)
        return Response(serializer.data)

    def put(self, request, pk):
        review = self.get_object(pk)
        serializer = ReviewSerializer(review, data=request.data)
        self.check_object_permissions(self.request, reviews)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        post = self.get.object(pk)
        post.delete()
        return Response(
            status=status.HTTP_204_NO_CONTENT
        )
