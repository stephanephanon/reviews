import datetime
import factory
import pytz

from django.contrib.auth.models import User

from api.models import Company, Review, Reviewer


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
        django_get_or_create = ('username',)

    username = factory.Sequence(lambda n: 'a{0}'.format(n))
    first_name = ''
    last_name = ''
    is_active = True
    is_superuser = False
    is_staff = False
    last_login = pytz.utc.localize(datetime.datetime.utcnow())
    password = factory.PostGenerationMethodCall('set_password', 'pw')
    email = ''


class CompanyFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Company


class ReviewFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Review


class ReviewerFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Reviewer
