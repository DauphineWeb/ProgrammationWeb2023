from django.contrib import admin
from .models import *

class MovieAdmin(admin.ModelAdmin):
    list_display = ['id','title','genre']

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'subscription_plan']

# Register your models here.
admin.site.register(SubscriptionPlan)
admin.site.register(Movie, MovieAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Review)
