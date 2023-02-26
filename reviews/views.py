from rest_framework import status, permissions, generics, filters
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import Http404
from .models import Review
from .serializers import ReviewSerializer
from whirl.permissions import IsOwnerOrReadOnly
from django.db.models import Count
from django_filters.rest_framework import DjangoFilterBackend


class ReviewList(APIView):
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Review.objects.annotate(
        likes_count=Count('likes', distinct=True),
        comments_count=Count('comment', distinct=True)
    ).order_by('-created_at')
    filter_backends = [
        filters.OrderingFilter,
        filters.SearchFilter,
        DjangoFilterBackend,
    ]
    filterset_fields = [
        'owner__followed__owner__profile',
        'likes__owner__profile',
        'owner__profile',
    ]
    search_fields = [
        'owner__username',
        'title',
    ]
    ordering_fields = [
        'likes_count',
        'comments_count',
        'likes__created_at',
    ]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class ReviewDetailList(APIView):
    serializer_class = ReviewSerializer
    permission_classes = [
        IsOwnerOrReadOnly,
        permissions.IsAdminUser,
        permissions.IsAuthenticatedOrReadOnly,
        ]
    queryset = Review.objects.annotate(
        likes_count=Count('likes', distinct=True),
        comments_count=Count('comment', distinct=True)
    ).order_by('-created_at')

    def delete(self, request, pk):
        review = self.get.object(pk)
        review.delete()
        return Response(
            status=status.HTTP_204_NO_CONTENT
        )
