from django.core.validators import MaxLengthValidator, ProhibitNullCharactersValidator
from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=300)
    content = models.TextField(null=True, blank=True)
    date_posted = models.DateTimeField(auto_now_add=True)
    is_edited = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_DEFAULT, default='-1')
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    parent_comment = models.ForeignKey('self', on_delete=models.DO_NOTHING, null=True, blank=True) # If null render as top level ?
    content = models.TextField(null=False, max_length=10000,
                               validators=[MaxLengthValidator(limit_value=10000, message='Exceeded post length'),
                                           ProhibitNullCharactersValidator(message='Null characters are not allowed')])
    date_posted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by \"{self.user.username}\" on post \"{self.post.title}\"'
