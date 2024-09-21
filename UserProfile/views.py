from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from .models import UserProfile

# Create your views here.
def user_profile(request, pk):
    user = User.objects.get(id=pk)
    return render(request, 'user/user_profile.html', {'user': user})

def all_users(request):
    users = User.objects.all()
    return render(request, 'user/all_users.html', {'users': users})

@login_required
def upload_profile_picture(request):
    if request.method == 'POST':
        profile_picture = request.FILES.get('profile_picture')

        if profile_picture:
            # Update the user's profile picture
            profile = request.user.profile
            profile.profile_picture = profile_picture
            profile.save()
            
            return redirect('profile', pk=request.user.id)
    
    return render(request, 'user/upload_profile_picture.html')

# View to update the bio
@login_required
def update_bio(request):
    if request.method == 'POST':
        bio = request.POST.get('bio')
        if bio:
            profile = request.user.profile
            profile.bio = bio
            profile.save()
            messages.success(request, 'Bio updated successfully.')
        return redirect('profile', pk=request.user.id)

# View to update the date of birth
@login_required
def update_dob(request):
    if request.method == 'POST':
        dob = request.POST.get('date_of_birth')
        if dob:
            profile = request.user.profile
            profile.date_of_birth = dob
            profile.save()
            messages.success(request, 'Date of Birth updated successfully.')
        return redirect('profile', pk=request.user.id)

# View to update the phone number
@login_required
def update_phone(request):
    if request.method == 'POST':
        phone_prefix = request.POST.get('phone_prefix')
        phone_number = request.POST.get('phone_number')
        if phone_prefix and phone_number:
            profile = request.user.profile
            profile.phone_prefix = phone_prefix
            profile.phone_number = phone_number
            profile.save()
            messages.success(request, 'Phone number updated successfully.')
        return redirect('profile', pk=request.user.id)

# View to update the address
@login_required
def update_address(request):
    if request.method == 'POST':
        profile = request.user.profile
        profile.house_number = request.POST.get('house_number')
        profile.street_name = request.POST.get('street_name')
        profile.city = request.POST.get('city')
        profile.state = request.POST.get('state')
        profile.country = request.POST.get('country')
        profile.postal_code = request.POST.get('postal_code')
        profile.save()
        messages.success(request, 'Address updated successfully.')
        return redirect('profile', pk=request.user.id)
