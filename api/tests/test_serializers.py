"""
Tests on custom serializer methods
"""
from unittest import mock

from django.test import TestCase
from rest_framework.exceptions import ValidationError

from api.serializers import ReviewSerializer, ReviewerSerializer
from api.tests import factories


class ReviewSerializerTests(TestCase):
    """
    Tests on ReviewSerializer
    """
    @mock.patch('rest_framework.request.Request')
    def test__get_ip_address_from_request_client_forward(self, mock_req):
        mock_req.META = {
            'HTTP_X_FORWARDED_FOR': '192.0.0.1',
            'REMOTE_ADDR': '142.0.0.1'
        }

        s = ReviewSerializer(context={'request': mock_req})
        expected_ret = '192.0.0.1'
        ret = s._get_ip_address_from_request()
        self.assertEqual(ret, expected_ret)

    @mock.patch('rest_framework.request.Request')
    def test__get_ip_address_from_request_direct_ip(self, mock_req):
        mock_req.META = {
            'HTTP_X_FORWARDED_FOR': '',
            'REMOTE_ADDR': '142.0.0.1'
        }

        s = ReviewSerializer(context={'request': mock_req})
        expected_ret = '142.0.0.1'
        ret = s._get_ip_address_from_request()
        self.assertEqual(ret, expected_ret)

    @mock.patch('rest_framework.request.Request')
    def test__get_ip_address_from_request_no_match(self, mock_req):
        mock_req.META = {
            'HTTP_X_FORWARDED_FOR': '',
            'REMOTE_ADDR': ''
        }
        s = ReviewSerializer(context={'request': mock_req})
        expected_ret = ''
        ret = s._get_ip_address_from_request()
        self.assertEqual(ret, expected_ret)

    @mock.patch('rest_framework.request.Request')
    def test__get_request_user_known_user(self, mock_req):
        user = factories.UserFactory(username='r1')
        reviewer = user.reviewer
        mock_req.user = user

        s = ReviewSerializer(context={'request': mock_req})
        expected_ret = reviewer
        ret = s._get_request_user()
        self.assertEqual(ret, expected_ret)

    @mock.patch('rest_framework.request.Request')
    def test__get_request_user_no_reviewer(self, mock_req):
        user = factories.UserFactory(username='u1', reviewer=None)
        mock_req.user = user

        s = ReviewSerializer(context={'request': mock_req})
        with self.assertRaises(ValidationError):
            s._get_request_user()

    @mock.patch('rest_framework.request.Request')
    def test__get_request_user_anon_user(self, mock_req):
        # set the property, then reset when done
        user = factories.UserFactory(username='a1', reviewer=None)
        type(user).is_anonymous = mock.PropertyMock(return_value=True)
        mock_req.user = user

        s = ReviewSerializer(context={'request': mock_req})
        with self.assertRaises(ValidationError):
            s._get_request_user()

        type(user).is_anonymous = mock.PropertyMock(return_value=False)

    @mock.patch('rest_framework.request.Request')
    def test_to_internal_value_adds_ip_and_reviewer(
            self, mock_req):
        user = factories.UserFactory(username='ip_user')
        mock_req.META = {
            'HTTP_X_FORWARDED_FOR': '192.0.0.1',
            'REMOTE_ADDR': '142.0.0.1'
        }
        mock_req.user = user
        mock_req.versionong_scheme.get_versioned_viewname.return_value = ''

        s = ReviewSerializer(context={'request': mock_req}, partial=True)

        data = {
            "rating": 5,
            "title": "test title",
            "summary": "test summary",
        }
        expected_ret = {
            "rating": 5,
            "title": "test title",
            "summary": "test summary",
            "ip_address": "192.0.0.1",
            "reviewer": user.reviewer

        }
        ret = s.to_internal_value(data)
        self.assertEqual(ret, expected_ret)


class ReviewerSerializerTests(TestCase):
    """
    Tests on Reviewer Serializer
    """
    def test_create(self):
        """
        Assert that we create a user and
        a corresponding reviewer object
        """
        data = {
            "username": "test_create_user",
            "first_name": "f",
            "last_name": "l",
            "password": "pwd",
            "reviewer": {"bio": "i'm a user!"}
        }
        s = ReviewerSerializer()

        ret = s.create(data)
        self.assertEqual(ret.username, 'test_create_user')
        self.assertEqual(ret.reviewer.bio, "i'm a user!")

        # no password
        data = {
            "username": "test_create_user_2",
            "first_name": "f",
            "last_name": "l",
            "reviewer": {"bio": "i'm a user 2!"}
        }
        s = ReviewerSerializer()

        ret = s.create(data)
        self.assertEqual(ret.username, 'test_create_user_2')
        self.assertEqual(ret.reviewer.bio, "i'm a user 2!")

    def test_update_user_and_reviewer_data_and_password(self):
        user = factories.UserFactory(
            username='test_update_user',
            first_name='update_fn',
            last_name='update_ln'
        )
        user.reviewer.bio = 'test bio'
        user.save()

        data = {

            "first_name": "update_fn",
            "last_name": "update_ln",
            "password": "new_pwd",
            "reviewer": {"bio": "update bio"}
        }
        s = ReviewerSerializer()

        ret = s.update(user, data)
        self.assertEqual(ret.username, 'test_update_user')
        self.assertEqual(ret.first_name, 'update_fn')
        self.assertEqual(ret.last_name, 'update_ln')
        self.assertEqual(ret.reviewer.bio, "update bio")

    def test_update_user_data(self):
        user = factories.UserFactory(
            username='test_update_user_only',
            first_name='only_fn',
            last_name='only_ln'
        )
        user.reviewer.bio = 'test bio'
        user.save()

        data = {

            "first_name": "only_fn",
            "last_name": "only_ln",
        }
        s = ReviewerSerializer()

        ret = s.update(user, data)
        self.assertEqual(ret.username, 'test_update_user_only')
        self.assertEqual(ret.first_name, 'only_fn')
        self.assertEqual(ret.last_name, 'only_ln')
        self.assertEqual(ret.reviewer.bio, "test bio")
