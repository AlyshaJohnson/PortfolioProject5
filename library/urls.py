from django.urls import path
from library import views

urlpatterns = [
    path('library/', views.LibraryList.as_view()),
    path('library/<int:pk>/', views.LibraryDetail.as_view()),
]
