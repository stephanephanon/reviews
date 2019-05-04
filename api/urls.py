from django.urls import path, include

from . import views

urlpatterns = [

    path('companies/', views.CompanyListView.as_view(), name='company-list'),
    path('companies/<int:pk>', views.CompanyDetailView.as_view(), name='company-detail'),

    path('reviews/', views.ReviewListView.as_view(), name='review-list'),
    path('reviews/<int:pk>/', views.ReviewDetailView.as_view(), name='review-detail'),

    path('reviewers/', views.ReviewerListView.as_view(), name='reviewer-list'),
    path('reviewers/<int:pk>/', views.ReviewerDetailView.as_view(), name='reviewer-detail'),
]
