from django.contrib import admin

from api.models import Company, Review, Reviewer


class CompanyAdmin(admin.ModelAdmin):
    list_display = ('pk', '__str__')


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('pk', 'company', 'title', 'rating', 'reviewer')


class ReviewerAdmin(admin.ModelAdmin):
    list_display = ('pk', '__str__')


admin.site.register(Company, CompanyAdmin)
admin.site.register(Reviewer, ReviewerAdmin)
admin.site.register(Review, ReviewAdmin)
