from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


class Company(models.Model):
    """
    Represents a company that can be reviewed
    """
    name = models.CharField(max_length=64)
    website = models.URLField(null=True, blank=True)

    def __str__(self):  # pragma: no cover
        return self.name


class Reviewer(models.Model):
    """
    Represents a user who is providing a review
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    website = models.URLField(null=True, blank=True)

    def __str__(self):  # pragma: no cover
        return self.user.username


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
    reviewer = models.ForeignKey(Reviewer, on_delete=models.CASCADE)

    def __str__(self):  # pragma: no cover
        return self.title
