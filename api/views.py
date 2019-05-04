from django.contrib.auth.models import User
from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.views import ObtainAuthToken

from api.filters import IsReviewerFilterBackend, IsUserFilterBackend
from api.models import Company, Review
from api.serializers import CompanySerializer, ReviewerSerializer, ReviewSerializer


class AuthenticateUserView(ObtainAuthToken):
    """
    Endpoint to get the token for a reviewer.

    GET: not supported.

    POST: send payload as follows to get a token
        {"username": username,
         "password": password
        }
    """
    authentication_classes = ()
    permission_classes = (AllowAny,)


# --------------------------------------
# Views that require TokenAuthentication
# set header as:
# (Authorization: Token 5ee20320125}
# --------------------------------------
class ReviewerListView(generics.CreateAPIView):
    """
    List endpoint to allow a reviewer to register with the system.

    GET: not supported

    POST: allowed by anyone to register with the system
    """
    queryset = User.objects.all()
    serializer_class = ReviewerSerializer
    authentication_classes = ()
    permission_classes = (AllowAny,)
    filter_backends = (IsUserFilterBackend,)


class ReviewerDetailView(generics.RetrieveUpdateAPIView):
    """
    Detail endpoint to allow a reviewer to manage their information.

    GET: return information about the current user

    PUT/PATCH: update the current user
    """
    queryset = User.objects.all()
    serializer_class = ReviewerSerializer
    filter_backends = (IsUserFilterBackend,)


class CompanyListView(generics.ListAPIView):
    """
    Read-only list endpoint for companies

    GET: list of companies
    """
    queryset = Company.objects.all()
    serializer_class = CompanySerializer


class CompanyDetailView(generics.RetrieveAPIView):
    """
    Read-only detail endpoint of companies

    GET: return a single company
    """
    queryset = Company.objects.all()
    serializer_class = CompanySerializer


class ReviewListView(generics.ListCreateAPIView):
    """
    List endpoint to allow a reviewer to view and create their reviews

    GET: list all reviews by this user

    POST: create a new review by this user
    """
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    filter_backends = (IsReviewerFilterBackend,)


class ReviewDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Detail endpoint to allow a reviewer to view and edit their reviews

    GET: return a specific review by this user

    PUT/PATCH: update a specific review by this user

    DELETE: delete a specific review by a user
    """
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    filter_backends = (IsReviewerFilterBackend,)
