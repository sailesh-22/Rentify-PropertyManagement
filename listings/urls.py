from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('seller/home/', views.seller_home, name='seller_home'),
    path('property/new/', views.property_create, name='property_create'),
    path('property/<int:pk>/edit/', views.property_edit, name='property_edit'),
    path('property/<int:pk>/delete/', views.property_delete, name='property_delete'),
    path('property/<int:pk>/', views.property_detail, name='property_detail'),
    path('property/<int:pk>/like/', views.property_like, name='property_like'),
    path('profile/<int:pk>/', views.profile_view, name='profile'),
    path('property/<int:pk>/property-interest/', views.property_interest, name='property_interest'),
]
