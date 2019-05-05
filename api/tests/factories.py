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

    reviewer = factory.RelatedFactory(
        'api.tests.factories.ReviewerFactory', 'user')


class CompanyFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Company


class ReviewerFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Reviewer
        django_get_or_create = ('user',)

    user = factory.SubFactory(UserFactory, reviewer=None)


class ReviewFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Review

    rating = 5
    title = factory.Sequence(lambda n: "title_%d" % n)
    summary = factory.Sequence(lambda n: "summary_%d" % n)
    ip_address = '127.0.0.1'
    company = factory.SubFactory(CompanyFactory)
    reviewer = factory.SubFactory(ReviewerFactory)
