from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Review
from library.models import Book


class ReviewListViewTests(APITestCase):
    def setUp(self):
        User.objects.create_user(username='john', password='pass')
        Book.objects.create(title='harry potter', author='jk rowling')

    def test_can_list_reviews(self):
        john = User.objects.get(username='john')
        hp = Book.objects.get(title='harry potter')
        Review.objects.create(
            owner=john,
            title='a title',
            description='a description',
            book=hp,
            rating=2,
            )
        response = self.client.get('/reviews/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print(response.data, len(response.data))

    def test_logged_in_user_can_create_review(self):
        hp = Book.objects.get(title='harry potter')
        self.client.login(username='john', password='pass')
        response = self.client.post(
            '/reviews/', {
                'title': 'a title',
                'description': 'a description',
                'book': hp,
                'rating': 1
                }
        )
        count = Review.objects.count()
        self.assertEqual(count, 1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class ReviewDetailViewTests(APITestCase):
    def setUp(self):
        john = User.objects.create_user(username='john', password='pass')
        jane = User.objects.create_user(username='jane', password='pass')
        Book.objects.create(title='harry potter', author='jk rowling')
        Review.objects.create(
            owner=john,
            title='johns title',
            description='a description',
            book=Book.objects.get(title='harry potter'),
            rating=2,
        )
        Review.objects.create(
            owner=jane,
            title='janes title',
            description='a description',
            book=Book.objects.get(title='harry potter'),
            rating=4,
        )

    def test_can_retrieve_review_using_valid_id(self):
        response = self.client.get('/reviews/1/')
        self.assertEqual(response.data['title'], 'johns title')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_can_update_own_review(self):
        self.client.login(username='adam', password='pass')
        response = self.client.put('/reviews/1/', {'title': 'a new title'})
        review = Review.objects.filter(pk=1).first()
        self.assertEqual(review.title, 'a new title')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
