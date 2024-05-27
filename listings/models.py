from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    USER_ROLES = (
        ('buyer','BUYER'),
        ('seller','SELLER'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15)
    role = models.CharField(max_length=10,choices=USER_ROLES)
    
    def __str__(self):
        return f"{self.user.username} - {self.role}"

class Property(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
    place = models.CharField(max_length=100)
    area = models.DecimalField(max_digits=10, decimal_places=2)
    bedrooms = models.IntegerField()
    bathrooms = models.IntegerField()
    hospitals_nearby = models.CharField(max_length=100)
    colleges_nearby = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    likes = models.ManyToManyField(User, related_name='liked_properties', blank=True, default=None)
    booked_by = models.OneToOneField(User, related_name='booked_property', null=True, blank=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title