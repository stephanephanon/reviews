from django.contrib import admin

from api.models import Company, Review


class CompanyAdmin(admin.ModelAdmin):
    list_display = ('pk', '__str__')


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('pk', 'company', 'title', 'rating')


admin.site.register(Company, CompanyAdmin)
admin.site.register(Review, ReviewAdmin)
