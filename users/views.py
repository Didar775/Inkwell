# blog/views.py
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .forms import ProfileForm
from .models import Profile, Follow


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            Profile.objects.create(user=user)
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registration.html', {'form': form})


@login_required
def profile(request, username):
    user = User.objects.get(username=username)
    profile = user.profile
    return render(request, 'profile.html', {'profile': profile})


@login_required
def user_list(request):
    users = User.objects.exclude(id=request.user.id)  # Exclude the current user
    following_usernames = request.user.profile.following.values_list('following__user__username', flat=True)

    followed_users = users.filter(username__in=following_usernames)
    non_followed_users = users.exclude(username__in=following_usernames)

    return render(request, 'user_list.html', {
        'followed_users': followed_users,
        'non_followed_users': non_followed_users,
    })


@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect('profile', username=request.user.username)
    else:
        form = ProfileForm(instance=request.user.profile)
    return render(request, 'edit_profile.html', {'form': form})


@login_required
def follow(request, username):
    followed_user = get_object_or_404(User, username=username)
    followed_profile = get_object_or_404(Profile, user=followed_user)

    # Create a follow relationship
    Follow.objects.get_or_create(follower=request.user.profile, following=followed_profile)

    return redirect('user_list')


@login_required
def unfollow(request, username):
    followed_user = get_object_or_404(User, username=username)
    followed_profile = get_object_or_404(Profile, user=followed_user)

    Follow.objects.filter(follower=request.user.profile, following=followed_profile).delete()

    return redirect('user_list')


@login_required
def profile_view(request, username):
    user = get_object_or_404(User, username=username)
    profile = get_object_or_404(Profile, user=user)
    posts = user.post_set.all()

    return render(request, 'profile_view.html', {'profile': profile, 'posts': posts})
