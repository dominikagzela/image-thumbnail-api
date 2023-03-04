from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator


class Tier(models.Model):
    name = models.CharField(max_length=50)
    link_to_original = models.BooleanField(default=True)
    thumbnail_height_sizes = models.CharField(max_length=255,
                                              help_text='Comma-separated list of thumbnail height sizes (e.g. 200, 400)'
                                              )
    expiring_links = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class User(AbstractUser):
    tier = models.ForeignKey(Tier, on_delete=models.CASCADE, blank=True, null=True)


class TierImage(models.Model):
    upload_file = models.ImageField(upload_to='images/')
    duration = models.IntegerField(validators=[
        MaxValueValidator(300),
        MinValueValidator(300000)
    ])
    tier = models.ForeignKey(Tier, on_delete=models.CASCADE)
