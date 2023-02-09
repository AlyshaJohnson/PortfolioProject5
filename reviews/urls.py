from django.urls import path
from reviews import views


urlpatterns = [
    path('reviews/', views.ReviewList.as_view()),
    path('reviews/<int:pk>/', views.ReviewDetailList.as_view()),
]
