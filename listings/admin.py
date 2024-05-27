from django.contrib import admin
from .models import Profile, Property

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'role')
    search_fields = ('user__username', 'phone', 'role')

@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'place', 'price', 'created_at')
    search_fields = ('title', 'place', 'user__username')
    list_filter = ('place', 'bedrooms', 'bathrooms', 'price')
