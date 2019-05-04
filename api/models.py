from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


class Company(models.Model):
    """
    Represents a company that can be reviewed
    """
    name = models.CharField(max_length=64)
    website = models.URLField(null=True, blank=True)

    def __str__(self):
        return self.name


class Review(models.Model):
    """
    Represents a user review about a company
    """
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)])
    title = models.CharField(max_length=64)
    summary = models.CharField(max_length=10000)
    ip_address = models.GenericIPAddressField()
    submission_date = models.DateTimeField(auto_now_add=True)
    company = models.ForeignKey(Company, on_delete=models.PROTECT)
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
