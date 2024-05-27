from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect, get_object_or_404
from .models import Property, Profile
from .forms import SignUpForm, PropertyForm
from django.core.mail import send_mail
from .forms import InterestForm
from django.conf import settings

def home(request):
    properties = Property.objects.all()
    
    properties = Property.objects.all()
    places = Property.objects.values_list('place', flat=True).distinct()
    
    place = request.GET.get('place')
    bedrooms = request.GET.get('bedrooms')
    price = request.GET.get('price_order')

    if place:
        properties = properties.filter(place=place)
    if bedrooms:
        properties = properties.filter(bedrooms=bedrooms)
    if price:
        if price == 'low':
            properties = properties.order_by('price')
        elif price == 'high':
            properties = properties.order_by('-price')
    # Add more filters as needed

    return render(request, 'home.html', {'properties': properties,'places':places,'range':[1,2,3,4,5,6]})

def is_seller(user):
    return user.profile.role == 'seller'

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            phone = form.cleaned_data.get('phone')
            profile = Profile.objects.update( phone=phone)
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

@login_required
def profile_view(request, pk):
    if request.user.pk != pk:
        user = request.user
        return redirect('profile', {'user' : user})

    user = request.user
   
    context = {
        'user': user,
        
    }
    return render(request, 'profile.html', context)

@login_required
@user_passes_test(is_seller)
def property_create(request):
    if request.method == 'POST':
        form = PropertyForm(request.POST)
        if form.is_valid():
            property = form.save(commit=False)
            property.user = request.user
            property.save()
            return redirect('seller_home')
    else:
        form = PropertyForm()
    return render(request, 'property_form.html', {'form': form})

@login_required
@user_passes_test(is_seller)
def property_edit(request, pk):
    property = get_object_or_404(Property, pk=pk)
    if request.method == 'POST':
        form = PropertyForm(request.POST, instance=property)
        if form.is_valid():
            form.save()
            return redirect('seller_home')
    else:
        form = PropertyForm(instance=property)
    return render(request, 'property_form.html', {'form': form})

@login_required
@user_passes_test(is_seller)
def property_delete(request, pk):
    property = get_object_or_404(Property, pk=pk)
    if request.method == 'POST':
        property.delete()
        return redirect('seller_home')

@login_required
def property_like(request, pk):
    property = get_object_or_404(Property, pk=pk)
    if request.user in property.likes.all():
        property.likes.remove(request.user)
    else:
        property.likes.add(request.user)
    return redirect('home')


@login_required
def property_detail(request, pk):
    property = get_object_or_404(Property, pk=pk)
    liked = False
    if request.user.is_authenticated:
        liked = property.likes.filter(id=request.user.id).exists()
    return render(request, 'property_detail.html', {'property': property, 'liked': liked})

@login_required
def property_interest(request, pk):
    property = get_object_or_404(Property, pk=pk)
    seller_profile = property.user
    buyer_profile = request.user

    if request.method == 'POST':
        form = InterestForm(request.POST)
        if form.is_valid():
      
            send_mail(
                'Property Interest - Seller Contact Details',
                f'You have expressed interest in the property: {property.title}. Here are the seller\'s contact details:\n\n'
                f'Name: {property.user.username}\n'
                f'Email: {property.user.email}\n'
                f'Phone: {seller_profile.profile.phone}',
                settings.DEFAULT_FROM_EMAIL,
                [request.user.email],
                fail_silently=False,
            )
            # Send email to seller with buyer details
            send_mail(
                'Property Interest - Buyer Contact Details',
                f'Someone is interested in your property: {property.title}. Here are the buyer\'s contact details:\n\n'
                f'Name: {request.user.username}\n'
                f'Email: {request.user.email}\n'
                f'Phone: {buyer_profile.profile.phone}',
                settings.DEFAULT_FROM_EMAIL,
                [property.user.email],
                fail_silently=False,
            )
            return render(request,'property_interest_confirmation.html',{'buyer':buyer_profile ,'property': property,'pk':pk })
    return render(request, 'property_interest.html',{'buyer':buyer_profile,'seller': seller_profile, 'property': property})

@login_required
@user_passes_test(is_seller)
def seller_home(request):
    properties = Property.objects.filter(user=request.user)
    return render(request, 'seller_home.html', {'properties': properties})