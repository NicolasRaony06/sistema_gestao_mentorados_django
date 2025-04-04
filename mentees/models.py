from django.db import models
from django.contrib.auth.models import User

class Navigators(models.Model):
    name = models.CharField(max_length=120)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Mentorados(models.Model):
    stages_choices = (
        ('S1', '10-100k'),
        ('S2', '100k-1kk')
    )
    name = models.CharField(max_length=120)
    created_at = models.DateField(auto_now_add=True)
    photo = models.ImageField(upload_to='photos', null=True, blank=True)
    stage = models.CharField(max_length=2, choices=stages_choices)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    navigator = models.ForeignKey(Navigators,null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
