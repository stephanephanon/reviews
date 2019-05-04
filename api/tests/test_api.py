"""
Tests on the API calls in api application
"""
from rest_framework.test import APITestCase


class CompanyTests(APITestCase):
    """
    Tests on the Company endpoints.
    These are read-only (set in django admin)
    """
    pass


class ReviewTests(APITestCase):
    """
    Tests on the Review endpoints.
    Users can only see and edit their own reviews
    """


class ReviewerTests(APITestCase):
    """
    Tests on the Reviewer endpoints.
    Anyone can create a reviewer account,
    and they can edit their own reviewer account.
    """
    pass
