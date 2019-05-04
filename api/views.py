from rest_framework import generics
from rest_framework.permissions import IsAdminUser

from api.models import Company, Reviewer, Review
from api.serializers import CompanySerializer, ReviewerSerializer, ReviewSerializer


# TODO: token authentication
# TODO: can users edit their review after submission?
# TODO: unit tests


class CompanyListView(generics.ListCreateAPIView):
    """
    TODO: add documentation
    """
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = (IsAdminUser,)


class CompanyDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    TODO: add documentation    """
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = (IsAdminUser,)


class ReviewerListView(generics.ListCreateAPIView):
    """
    TODO: add documentation    """
    queryset = Reviewer.objects.all()
    serializer_class = ReviewerSerializer
    permission_classes = (IsAdminUser,)


class ReviewerDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    TODO: add documentation
    """
    queryset = Reviewer.objects.all()
    serializer_class = ReviewerSerializer
    permission_classes = (IsAdminUser,)


class ReviewListView(generics.ListCreateAPIView):
    """
    TODO: add documentation
    """
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    # TODO: permissions. Only user who wrote review can see the review
    # permission_classes = (IsAdminUser,)


class ReviewDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    TODO: add documentation
    """
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    # TODO: permissions. Only user who wrote review can see the review
    # permission_classes = (IsAdminUser,)

