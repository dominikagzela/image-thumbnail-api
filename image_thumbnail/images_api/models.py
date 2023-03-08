from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.exceptions import ValidationError


def validate_thumbnail_height_sizes(value):
    try:
        sizes = [int(s.strip()) for s in value.split(',')]
    except ValueError:
        raise ValidationError('Invalid input format. Please enter comma-separated list of integers')

    for size in sizes:
        if size < 300 or size > 300000:
            raise ValidationError('Thumbnail height size should be between 300 and 300.000.')


class Tier(models.Model):
    name = models.CharField(max_length=50)
    link_to_original = models.BooleanField(default=True)
    thumbnail_height_sizes = models.CharField(
        max_length=255,
        help_text='Comma-separated list of thumbnail height sizes (e.g. 200, 400)',
        validators=[validate_thumbnail_height_sizes]
    )
    expiring_links = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class User(AbstractUser):
    tier = models.ForeignKey(Tier, on_delete=models.CASCADE, blank=True, null=True)


class TierImage(models.Model):
    upload_file = models.ImageField(upload_to='images/')
    duration = models.IntegerField(validators=[
        MinValueValidator(300),
        MaxValueValidator(300000)
    ], null=True, blank=True, default=None)
    tier = models.ForeignKey(Tier, on_delete=models.CASCADE)
