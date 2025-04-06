from django.db import models
from django.contrib.auth.models import User
from datetime import timedelta
import secrets

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
    photo = models.ImageField(upload_to='photos', default='photos/default.bmp')
    stage = models.CharField(max_length=2, choices=stages_choices)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    navigator = models.ForeignKey(Navigators,null=True, blank=True, on_delete=models.CASCADE)
    token = models.CharField(max_length=16, unique=True)

    def save(self, *args, **kwargs):
        if not self.token:
            self.token = self.gen_uniq_token()
        super().save(*args, **kwargs)

    def gen_uniq_token(self):
        while True:
            token = secrets.token_urlsafe(8)
            if not Mentorados.objects.filter(token=token).exists():
                return token
            
    def __str__(self):
        return self.name

class ScheduleAvailability(models.Model):
    start_date = models.DateTimeField(null=True, blank=True)
    mentor = models.ForeignKey(User, on_delete=models.CASCADE)
    scheduled = models.BooleanField(default=False)

    @property
    def final_date(self):
        try:
            return self.start_date + timedelta(minutes=50)
        except:
            return None