from rest_framework import filters


class IsUserFilterBackend(filters.BaseFilterBackend):
    """
    Filter that only allows users to see their own objects.
    """
    # https://www.django-rest-framework.org/api-guide/filtering/#setting-filter-backends
    def filter_queryset(self, request, queryset, view):
        """
        The queryset of users that is returned is only
        the set that the request.user created.

        Will return an empty queryset if the user is anonymous.

        :return: filtered queryset
        """
        user = request.user
        return queryset.filter(pk=user.pk)


class IsReviewerFilterBackend(filters.BaseFilterBackend):
    """
    Filter that only allows users to see their own objects.
    """
    def filter_queryset(self, request, queryset, view):
        """
        The queryset of reviews that is returned is only
        the set that the request.user created.

        Will return an empty queryset if the user is anonymous.

        :return: filtered queryset
        """
        user = request.user
        try:
            reviewer = user.reviewer
        except AttributeError:
            # somehow the user wasn't authenticated
            reviewer = None

        return queryset.filter(reviewer=reviewer)
