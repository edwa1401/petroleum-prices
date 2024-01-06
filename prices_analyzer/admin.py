from django.contrib import admin
from prices_analyzer.models import ProductionPlace, Basis, Depot


class ProdictionPlaceAdmin(admin.ModelAdmin):
    list_display = ('basis_code', 'basis_name', 'rzd_code_code', 'rzd_code_station_name', 'name')
    list_filter = ('basis_name', 'rzd_code_station_name', 'name')


admin.site.register(ProductionPlace, ProdictionPlaceAdmin)


admin.site.register(Basis)
admin.site.register(Depot)
