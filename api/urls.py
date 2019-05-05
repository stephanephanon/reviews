from django.urls import path

from . import views

urlpatterns = [

    # supports POST only -- get a non-expiring token for the other endpoints
    path('token-auth/', views.AuthenticateUserView.as_view(), name='reviewer-auth'),

    path('companies/', views.CompanyListView.as_view(), name='company-list'),
    path('companies/<int:pk>/', views.CompanyDetailView.as_view(), name='company-detail'),

    path('reviews/', views.ReviewListView.as_view(), name='review-list'),
    path('reviews/<int:pk>/', views.ReviewDetailView.as_view(), name='review-detail'),

    path('reviewers/', views.ReviewerListView.as_view(), name='reviewer-list'),
    path('reviewers/<int:pk>/', views.ReviewerDetailView.as_view(), name='reviewer-detail'),
]
