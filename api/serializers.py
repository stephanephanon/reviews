from django.contrib.auth.models import User
from rest_framework import serializers

from api.models import Company, Review, Reviewer


IP_ADDRESS_REQUEST_FIELDS = {
    'client_forwarded': 'HTTP_X_FORWARDED_FOR',
    'direct_api_access': 'REMOTE_ADDR'}


class CompanySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'


class ReviewSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer for user reviews about companies
    """
    ip_address = serializers.CharField(
        read_only=True
    )

    reviewer = serializers.HyperlinkedRelatedField(
        read_only=True,
        view_name='reviewer-detail'
    )

    def _get_ip_address_from_request(self):
        """
        Get the IP address from either of the headers
        """
        request = self.context['request']
        client_forwarded = IP_ADDRESS_REQUEST_FIELDS['client_forwarded']
        ip_addresses = request.META.get(client_forwarded, '')
        ip_address = ip_addresses.split(',')[0]

        if not ip_address:
            direct_access = IP_ADDRESS_REQUEST_FIELDS['direct_api_access']
            ip_address = request.META.get(direct_access)

        return ip_address

    def _get_request_user(self):
        """
        Get the request user.
        :return: User object
        :raise: ValidationError if AnonymousUser
        """
        error_msg_anonymous = {'reviewer': "AnonymousUser is not a valid reviewer"}
        error_msg_no_reviewer = {'reviewer': "Did not find a valid reviewer for this user"}
        user = self.context['request'].user

        if user.is_anonymous:
            raise serializers.ValidationError(error_msg_anonymous)

        try:
            reviewer = user.reviewer
        except Reviewer.DoesNotExist:
            raise serializers.ValidationError(error_msg_no_reviewer)

        return reviewer

    def to_internal_value(self, data):
        """
        Manually set the ip_address and reviewer fields.
        They are read-only for the client.

        :param data: data dictionary
        :return: dictionary
        :raise: ValidationError
        """
        ret = super().to_internal_value(data)
        ret['ip_address'] = self._get_ip_address_from_request()
        ret['reviewer'] = self._get_request_user()
        return ret

    class Meta:
        model = Review
        fields = '__all__'


class ReviewerSerializer(serializers.HyperlinkedModelSerializer):

    url = serializers.HyperlinkedIdentityField(
        view_name='reviewer-detail',
        read_only=True
    )

    date_joined = serializers.DateTimeField(
        read_only=True
    )

    bio = serializers.CharField(source="reviewer.bio",
                                required=False,
                                allow_blank=True)
    website = serializers.URLField(source="reviewer.website",
                                   required=False,
                                   allow_null=True,
                                   allow_blank=True)

    password = serializers.CharField(
        write_only=True
    )

    def create(self, validated_data):
        """
        Create a User and the corresponding Reviewer model
        :param validated_data:
        :return:
        """
        reviewer_data = validated_data.pop('reviewer', {})
        password = validated_data.pop('password', '')

        instance = super().create(validated_data)
        if password:
            instance.set_password(password)
            instance.save()

        # create reviewer data, even if just empty
        reviewer_data['user'] = instance
        Reviewer.objects.create(**reviewer_data)
        return instance

    def update(self, instance, validated_data):
        """
        Update a User and the corresponding Reviewer model
        :param instance:
        :param validated_data:
        :return:
        """
        reviewer_data = validated_data.pop('reviewer', {})
        password = validated_data.pop('password', '')

        instance = super().update(instance, validated_data)

        if password:
            instance.set_password(password)
            instance.save()

        if reviewer_data:
            reviewer = instance.reviewer
            for attr, value in reviewer_data.items():
                setattr(reviewer, attr, value)
            reviewer.save()

        return instance

    class Meta:
        model = User
        fields = ('url', 'username', 'first_name', 'last_name',
                  'email', 'date_joined', 'password',
                  'bio', 'website')
