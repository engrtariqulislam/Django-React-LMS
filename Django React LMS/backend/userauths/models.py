from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save

class User(AbstractUser):
    username = models.CharField(unique=True, max_length=100)
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=100, blank=True, null=True)
    otp = models.CharField(max_length=100, blank=True, null=True)

    USERNAME_FIELD = 'email'    
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email

    def save(self, *args, **kwargs):
        email_username = self.email.split("@")[0]
        if not self.full_name:
            self.full_name = email_username
        if not self.username:
            self.username = email_username
        super(User, self).save(*args, **kwargs)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="user_folder", default="default-user.jpg", blank=True, null=True)
    full_name = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    about = models.TextField(blank=True, null=True)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        if self.full_name:
            return self.full_name
        return self.user.full_name

    def save(self, *args, **kwargs):
        if not self.full_name:
            self.full_name = self.user.username
        super(Profile, self).save(*args, **kwargs)


        def create_user_profile(sender, instance, created, **kwargs):
            if created:
              Profile.objects.create(user=instance)

        def save_user_profile(sender, instance, **kwargs):
            instance.profile.save()

        post_save.connect(create_user_profile, sender=User)
        post_save.connect(save_user_profile, sender=User)