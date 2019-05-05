"""
Tests on the custom filtering backends
"""
from unittest import mock

from django.test import TestCase

from api.filters import IsUserFilterBackend, IsReviewerFilterBackend
from api.models import Reviewer, Review
from api.tests import factories


class IsUserFilterBackendTests(TestCase):
    @mock.patch('rest_framework.request.Request')
    def test_filter_queryset(self, mock_req):
        mock_view = mock.Mock()

        user1 = factories.UserFactory(username='f1')
        user2 = factories.UserFactory(username='f2')
        user3 = factories.UserFactory(username='f3')
        user4 = factories.UserFactory(username='f4', reviewer=None)

        queryset = Reviewer.objects.all()
        f = IsUserFilterBackend()

        for u in [user1, user2, user3]:
            mock_req.user = u
            ret = f.filter_queryset(mock_req, queryset, mock_view)
            self.assertEqual(len(ret), 1)
            self.assertTrue(u.reviewer in ret)

        # user without a reviewer
        mock_req.user = user4
        ret = f.filter_queryset(mock_req, queryset, mock_view)
        self.assertEqual(len(ret), 0)


class IsReviewerFilterBackendTests(TestCase):
    @mock.patch('rest_framework.request.Request')
    def test_filter_queryset(self, mock_req):
        """
        Assert that reviewers can only see their own reviews
        :param mock_req:
        :return:
        """
        mock_view = mock.Mock()

        company = factories.CompanyFactory(name='company1')
        company2 = factories.CompanyFactory(name='company2')

        user1 = factories.UserFactory(username='f1')
        user2 = factories.UserFactory(username='f2')
        user3 = factories.UserFactory(username='f3')
        user4 = factories.UserFactory(username='f4', reviewer=None)

        r1 = factories.ReviewFactory(
            reviewer=user1.reviewer, company=company)

        r2 = factories.ReviewFactory(
            reviewer=user2.reviewer, company=company)
        r3 = factories.ReviewFactory(
            reviewer=user2.reviewer, company=company2)

        r4 = factories.ReviewFactory(
            reviewer=user3.reviewer, company=company)
        r5 = factories.ReviewFactory(
            reviewer=user3.reviewer, company=company)
        r6 = factories.ReviewFactory(
            reviewer=user3.reviewer, company=company2)

        queryset = Review.objects.all()
        f = IsReviewerFilterBackend()

        for i, u in enumerate([user1, user2, user3]):
            mock_req.user = u
            expected_ret = Review.objects.filter(reviewer=u.reviewer)
            ret = f.filter_queryset(mock_req, queryset, mock_view)
            self.assertEqual(set(expected_ret), set(ret))

        # user without a reviewer
        mock_req.user = user4
        ret = f.filter_queryset(mock_req, queryset, mock_view)
        self.assertEqual(len(ret), 0)
