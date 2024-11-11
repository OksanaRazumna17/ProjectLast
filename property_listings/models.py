from django.db import models
from django.contrib.auth.models import User

# Модель для оголошень (Listings)
class Listing(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    location = models.CharField(max_length=255)
    owner = models.ForeignKey(User, related_name='listings', on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    views_count = models.PositiveIntegerField(default=0)  # Добавляем поле для подсчета просмотров

    def __str__(self):
        return self.title

    def increment_view_count(self):
        """
        Увеличиваем количество просмотров для объявления.
        """
        self.views_count += 1
        self.save()

    def get_reviews_count(self):
        """
        Возвращаем количество отзывов для объявления.
        """
        return self.reviews.count()

# Модель для бронювання (Booking)
class Booking(models.Model):
    listing = models.ForeignKey(Listing, related_name='bookings', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='bookings', on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=20,
                              choices=[('pending', 'Pending'), ('confirmed', 'Confirmed'), ('canceled', 'Canceled')])

    def __str__(self):
        return f"{self.listing.title} - {self.user.username}"

# Модель для відгуків (Review)
class Review(models.Model):
    listing = models.ForeignKey(Listing, related_name='reviews', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='reviews', on_delete=models.CASCADE)
    rating = models.PositiveIntegerField()
    comment = models.TextField()

    def __str__(self):
        return f"Review for {self.listing.title} by {self.user.username}"

# Модель для истории поиска (SearchHistory)
class SearchHistory(models.Model):
    user = models.ForeignKey(User, related_name='search_history', on_delete=models.CASCADE)
    query = models.CharField(max_length=255)
    date_searched = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Search by {self.user.username} - {self.query}"

    @classmethod
    def get_popular_queries(cls):
        """
        Метод для получения популярных запросов (по количеству выполненных запросов).
        """
        return cls.objects.values('query').annotate(query_count=models.Count('query')).order_by('-query_count')

# Модель для истории просмотров (ViewHistory)
class ViewHistory(models.Model):
    user = models.ForeignKey(User, related_name='view_history', on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, related_name='view_history', on_delete=models.CASCADE)
    date_viewed = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"View of {self.listing.title} by {self.user.username}"
