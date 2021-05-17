from django.contrib import admin

from api.models import VaccineCenter, County,SubCounty


class VaccineCentersAdmin(admin.ModelAdmin):
    list_display = ('name', 'sub_county', 'location', 'mfl', 'ownership')


admin.site.register(VaccineCenter, VaccineCentersAdmin)


class CountiesAdmin(admin.ModelAdmin):
    pass


admin.site.register(County, CountiesAdmin)


class SubCountyAdmin(admin.ModelAdmin):
    pass


admin.site.register(SubCounty, SubCountyAdmin)