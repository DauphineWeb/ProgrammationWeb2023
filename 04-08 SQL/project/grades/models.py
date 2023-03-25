from django.db import models
from django.forms import ModelForm

# Create your models here.
class ProblemSet(models.Model):
    title = models.CharField(max_length=100)
    due = models.DateField()

    def __str__(self):
        return f'{self.title}, due {self.due}'
    
class Question(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=1000)
    score = models.IntegerField()
    problem_set = models.ForeignKey(ProblemSet, on_delete=models.CASCADE, related_name='questions')

    def __str__(self):
        return f'{self.score} points to reach: {self.title}: {self.description}'

class ProblemSetForm(ModelForm):
    class Meta:
        model = ProblemSet
        fields = [ 'title', 'due' ]
