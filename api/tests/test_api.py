"""
Tests on the API calls in api application
"""
from unittest import mock

from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase, APIRequestFactory, force_authenticate, APIClient

from api import views
from api.tests import factories


class AuthenticateUserViewTests(APITestCase):
    """
    Tests on the endpoint to get a user token
    """
    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = views.AuthenticateUserView.as_view()
        self.user = factories.UserFactory(username='request_user')

    def test_cannot_get(self):
        request = self.factory.get('/api/token-auth/')
        force_authenticate(request, user=self.user)
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    @mock.patch('rest_framework.authtoken.serializers.AuthTokenSerializer.validate')
    def test_can_post_good_credentials(self, mock_validate):
        user = factories.UserFactory(username='u0')

        mock_validate.return_value = {
            'username': 'u0',
            'password': 'pw',
            'user': user
        }
        data = {
            'username': 'u0',
            'password': 'pw'
        }

        request = self.factory.post(
            '/api/token-auth/',
            data,
            format='json'
        )
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(response.data['token'])

    def test_can_post_bad_credentials(self):
        data = {
            'username': 'u0',
            'password': 'BAD'
        }

        request = self.factory.post(
            '/api/token-auth/',
            data,
            format='json'
        )
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class CompanyListTests(APITestCase):
    """
    Tests on the Company list endpoints.
    These are read-only (set in django admin)
    """
    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = views.CompanyListView.as_view()
        self.user = factories.UserFactory(username='request_user')
        self.token, _ = Token.objects.get_or_create(user=self.user)

    def test_can_get_list(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = client.get('/api/companies/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_cannot_post(self):
        data = {}
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = client.post('/api/companies/',
                               data, format='json')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)


class CompanyDetailTests(APITestCase):
    """
    Tests on the Company detail endpoints.
    These are read-only (set in django admin)
    """
    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = views.CompanyDetailView.as_view()
        self.user = factories.UserFactory(username='request_user')
        self.token, _ = Token.objects.get_or_create(user=self.user)
        self.company = factories.CompanyFactory(name="company_api")

    def test_can_get_detail(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = client.get('/api/companies/{}/'.format(self.company.pk))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'company_api')

    def test_cannot_edit(self):
        data = {}
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = client.put('/api/companies/{}/'.format(self.company.pk),
                              data, format='json')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_cannot_delete(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = client.delete('/api/companies/{}/'.format(self.company.pk))
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)


class ReviewListTests(APITestCase):
    """
    Tests on the Review list endpoints.
    Users can only see and create their own reviews
    """
    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = views.ReviewDetailView.as_view()
        self.user = factories.UserFactory(username='request_user')
        self.user2 = factories.UserFactory(username='another_user')
        self.token, _ = Token.objects.get_or_create(user=self.user)
        self.token2, _ = Token.objects.get_or_create(user=self.user2)

    def test_can_get_list(self):
        review1 = factories.ReviewFactory(
            reviewer=self.user.reviewer,
            title='reviewer1_title1')
        review1b = factories.ReviewFactory(
            reviewer=self.user.reviewer,
            title='reviewer1_title1b'
        )
        review2 = factories.ReviewFactory(
            reviewer=self.user2.reviewer,
            title='reviewer2_title1'
        )

        # reviewer 1 sees their stuff
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = client.get('/api/reviews/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        titles = set([i.get('title') for i in response.data])
        self.assertEqual(titles, {review1.title, review1b.title})

        # reviewer 2 sees their stuff
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + self.token2.key)
        response = client.get('/api/reviews/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        titles = set([i.get('title') for i in response.data])
        self.assertEqual(titles, {review2.title})

    def test_can_post(self):
        c = factories.CompanyFactory(name="company_can_post")

        data = {
            'rating': 5,
            'title': 'i can post',
            'summary': 'i can summarize',
            'company': 'http://testserver/api/companies/{}/'.format(c.pk)

        }
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = client.post('/api/reviews/',
                               data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class ReviewDetailTests(APITestCase):
    """
    Tests on the Review detail endpoints.
    Users can only see and edit their own reviews
    """
    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = views.ReviewDetailView.as_view()
        self.user = factories.UserFactory(username='request_user')
        self.user2 = factories.UserFactory(username='another_user')
        self.token, _ = Token.objects.get_or_create(user=self.user)
        self.token2, _ = Token.objects.get_or_create(user=self.user2)

    def test_can_get_detail(self):
        """
        Assert that each user can only get their own reviews
        """
        review1 = factories.ReviewFactory(
            reviewer=self.user.reviewer,
            title='private_review'
        )

        # for the first user
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = client.get('/api/reviews/{}/'.format(review1.pk))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'private_review')

        # second user -- can't see it
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + self.token2.key)
        response = client.get('/api/reviews/{}/'.format(review1.pk))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_can_edit(self):
        """
        Assert that each user can only edit their own reviews
        """
        review1 = factories.ReviewFactory(reviewer=self.user.reviewer)

        # first reviewer can edit his review
        data = {'title': "new_and_improved"}
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = client.patch('/api/reviews/{}/'.format(review1.pk),
                                data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'new_and_improved')

        # second user cannot
        data = {'title': "not_mine"}
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + self.token2.key)
        response = client.patch('/api/reviews/{}/'.format(review1.pk),
                                data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_can_delete(self):
        """
        Assert that each user can only delete their own reviews
        """
        review1 = factories.ReviewFactory(reviewer=self.user.reviewer)
        review2 = factories.ReviewFactory(reviewer=self.user.reviewer)

        # first reviewer can delete his review
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = client.delete('/api/reviews/{}/'.format(review1.pk))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # second user cannot
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + self.token2.key)
        response = client.delete('/api/reviews/{}/'.format(review2.pk))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class ReviewerListTests(APITestCase):
    """
    Tests on the Reviewer list endpoints.
    Anyone can create a reviewer account,
    """
    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = views.ReviewerListView.as_view()
        self.user = factories.UserFactory(username='request_user')
        self.token, _ = Token.objects.get_or_create(user=self.user)

    def test_cannot_get_list(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = client.get('/api/reviewers/')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_can_post(self):
        data = {
            'username': 'new_user',
            'password': 'password'
        }
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = client.post('/api/reviewers/',
                               data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class ReviewerDetailTests(APITestCase):
    """
    Tests on the Reviewer detail endpoints.
    Anyone can edit their own reviewer account.
    """
    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = views.ReviewerDetailView.as_view()
        self.user = factories.UserFactory(username='request_user')
        self.user2 = factories.UserFactory(username='another_user')
        self.token, _ = Token.objects.get_or_create(user=self.user)
        self.token2, _ = Token.objects.get_or_create(user=self.user2)

    def test_can_get_detail(self):
        """
        Assert that a reviewer can only see their own info
        """
        # for the first user
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = client.get('/api/reviewers/{}/'.format(self.user.pk))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'request_user')

        # second user -- can't see it
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + self.token2.key)
        response = client.get('/api/reviewers/{}/'.format(self.user.pk))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_can_edit(self):
        """
        Assert that a reviewer can only edit their own info
        """
        # first reviewer can edit his info
        data = {'first_name': "new_and_improved"}
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = client.patch('/api/reviewers/{}/'.format(self.user.pk),
                                data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['first_name'], 'new_and_improved')

        # second user cannot
        data = {'first_name': "not_mine"}
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + self.token2.key)
        response = client.patch('/api/reviewers/{}/'.format(self.user.pk),
                                data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_cannot_delete(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = client.delete('/api/reviewers/{}/'.format(self.user.pk))
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
