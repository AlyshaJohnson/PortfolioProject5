from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Post


class ReviewListViewTests(APITestCase):
    def setUp(self):
        User.objects.create_user(username='adam', password='pass')

    def test_can_list_reviews(self):
        adam = User.objects.get(username='adam')
        Review.objects.create(owner=adam, title='a title')
        response = self.client.get('/reviews/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print(response.data, len(response.data))

    def test_logged_in_user_can_create_review(self):
        self.client.login(username='adam', password='pass')
        response = self.client.post('/reviews/', {'title': 'a title'})
        count = Reviews.objects.count()
        self.assertEqual(count, 1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class ReviewDetailViewTests(APITestCase):
    def setUp(self):
        adam = User.objects.create_user(username='adam', password='pass')
        brian = User.objects.create_user(username='brian', password='pass')
        Review.objects.create(owner=adam, title='a title', description='adams content')  # noqa
        Review.objects.create(owner=brian, title='some other title', description='brians content')   # noqa

    def test_can_retrieve_review_using_valid_id(self):
        response = self.client.get('/reviews/1/')
        self.assertEqual(response.data['title'], 'a title')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_can_update_own_review(self):
        self.client.login(username='adam', password='pass')
        response = self.client.put('/reviews/1/', {'title': 'a new title'})
        review = Review.objects.filter(pk=1).first()
        self.assertEqual(review.title, 'a new title')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
