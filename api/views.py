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

    get:
    not supported

    post:
    send payload as follows to get an authentication token
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
    Access is open to all users.

    get:
    not supported

    post:
    create a new reviewer
    """
    queryset = User.objects.all()
    serializer_class = ReviewerSerializer
    authentication_classes = ()
    permission_classes = (AllowAny,)
    filter_backends = (IsUserFilterBackend,)


class ReviewerDetailView(generics.RetrieveUpdateAPIView):
    """
    Detail endpoint to allow a reviewer to manage their own information.

    get:
    return details about the given user if the user is the request user

    put:
    update the given user if the user is the request user

    patch:
    update the given user if the user is the request user
    """
    queryset = User.objects.all()
    serializer_class = ReviewerSerializer
    filter_backends = (IsUserFilterBackend,)


class CompanyListView(generics.ListAPIView):
    """
    Read-only endpoint for companies.

    get:
    return a list of all companies

    """
    queryset = Company.objects.all()
    serializer_class = CompanySerializer


class CompanyDetailView(generics.RetrieveAPIView):
    """
    Read-only detail endpoint of companies.

    get:
    return a details about the given company
    """
    queryset = Company.objects.all()
    serializer_class = CompanySerializer


class ReviewListView(generics.ListCreateAPIView):
    """
    List endpoint to allow a reviewer to view and create their reviews.

    get:
    return a list of all reviews by this request user

    post:
    create a new review by this request user
    """
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    filter_backends = (IsReviewerFilterBackend,)


class ReviewDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Detail endpoint to allow a reviewer to view and edit their reviews.

    get:
    return the given review by this request user

    put:
    update the given review by this request user

    patch:
    update the given review by this request user

    delete:
    delete the given review by this request user
    """
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    filter_backends = (IsReviewerFilterBackend,)
