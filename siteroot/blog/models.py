from django.conf import settings
from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.urls import reverse


class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('profile-posts', args=[self.user.username])


class Profile(models.Model):

    MALE, FEMALE = 'M', 'F'
    GENDER_CHOICES = ((MALE, 'Male'), (FEMALE, 'Female'))

    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    first_name = models.CharField(max_length=128, default='', blank=True)
    last_name = models.CharField(max_length=128, default='', blank=True)
    gender = models.CharField(
        max_length=1, choices=GENDER_CHOICES, default=MALE, blank=True
    )
    age = models.PositiveSmallIntegerField(default=0, blank=True)

    def __str__(self):
        return self.user.username

    def get_absolute_url(self):
        return reverse('profile-detail', args=[self.user.username])

    def get_absolute_update_url(self):
        return reverse('profile-update', args=[self.user.username])

    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'

    def get_all_profile_posts(self):
        return reverse('profile-posts', args=[self.user.username])
