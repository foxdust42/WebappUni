from django.core.validators import ProhibitNullCharactersValidator, MaxLengthValidator
from django.db import models
from django.contrib.auth.models import User, UserManager
from PIL import Image
from .validators import NoFutureDateValidator


# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

    description = models.TextField(null=True, max_length=5000, blank=True, default=None,
                                   validators=[ProhibitNullCharactersValidator(), MaxLengthValidator(5000)])

    avatar = models.ImageField(default='default_profile.jpg', upload_to='profile_pics')

    is_public = models.BooleanField(default=False)

    date_of_birth = models.DateField(null=True, blank=True, default=None)

    def __str__(self):
        return f'Profile for {self.user.username}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.avatar.path)
        if img.height > 256 or img.width > 256:
            output_size = (256, 256)
            img.thumbnail(output_size)
            img.save(self.avatar.path)
