# property_listings/views.py

from rest_framework import viewsets, permissions, generics
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from django.db.models import Count

from .models import Listing, Booking, Review, SearchHistory, ViewHistory
from .serializers import ListingSerializer, BookingSerializer, ReviewSerializer, SearchHistorySerializer, ViewHistorySerializer, UserSerializer

# ViewSet для оголошень (Listing)
class ListingViewSet(viewsets.ModelViewSet):
    queryset = Listing.objects.all()
    serializer_class = ListingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_update(self, serializer):
        listing = self.get_object()
        if listing.owner != self.request.user:
            raise PermissionDenied("Ви не можете редагувати це оголошення.")
        serializer.save()

    def perform_destroy(self, instance):
        if instance.owner != self.request.user:
            raise PermissionDenied("Ви не можете видалити це оголошення.")
        instance.delete()

    def get_queryset(self):
        queryset = Listing.objects.all()
        ordering = self.request.query_params.get('ordering', 'price')
        if ordering == 'popularity':
            queryset = queryset.annotate(views_count=Count('view_history')).order_by('-views_count')
        return queryset

# ViewSet для бронювання (Booking)
class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]

# ViewSet для відгуків (Review)
class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated]

# ViewSet для історії пошуків (SearchHistory)
class SearchHistoryViewSet(viewsets.ModelViewSet):
    queryset = SearchHistory.objects.all()
    serializer_class = SearchHistorySerializer
    permission_classes = [permissions.IsAuthenticated]

# ViewSet для історії переглядів (ViewHistory)
class ViewHistoryViewSet(viewsets.ModelViewSet):
    queryset = ViewHistory.objects.all()
    serializer_class = ViewHistorySerializer
    permission_classes = [permissions.IsAuthenticated]

# View для регистрации пользователя
class RegisterUser(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

# View для входа пользователя и получения токена
class LoginUser(generics.GenericAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')

        try:
            user = User.objects.get(username=username)
            if user.check_password(password):
                refresh = RefreshToken.for_user(user)
                return Response({
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }, status=200)
            else:
                return Response({'error': 'Неправельный пароль'}, status=400)
        except User.DoesNotExist:
            return Response({'error': 'Пользователя не найденно'}, status=404)

