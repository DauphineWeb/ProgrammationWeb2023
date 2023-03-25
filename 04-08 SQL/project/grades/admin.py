from django.contrib import admin
from .models import *

class QuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'score', 'problem_set')

class ProblemSetAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'due')

# Register your models here.
admin.site.register(ProblemSet, ProblemSetAdmin)
admin.site.register(Question, QuestionAdmin)
