from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import UpdateView
from django.urls import reverse_lazy
from .models import UserProfile
from . import forms

@login_required
def profile(request):
    profile = UserProfile.objects.get(user=request.user)
    return render(request, 'users/profile.html', { 'profile': profile.profile_picture, 'other': 'other' })

class UserProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = UserProfile
    fields = ['profile_picture']
    template_name = 'users/user_profile.html'
    success_url = reverse_lazy('profile')

    def get_object(self, queryset=None):
        return self.request.user.userprofile

