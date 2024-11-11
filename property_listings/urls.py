# property_listings/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ListingViewSet, BookingViewSet, ReviewViewSet,
    SearchHistoryViewSet, ViewHistoryViewSet,
    RegisterUser, LoginUser
)

router = DefaultRouter()
router.register(r'listings', ListingViewSet)
router.register(r'bookings', BookingViewSet)
router.register(r'reviews', ReviewViewSet)
router.register(r'search-history', SearchHistoryViewSet)
router.register(r'view-history', ViewHistoryViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('register/', RegisterUser.as_view(), name='register'),
    path('login/', LoginUser.as_view(), name='login'),
]









