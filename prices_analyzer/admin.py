from django.contrib import admin
from prices_analyzer.models import ProductionPlace, Basis, Depot, ProductKey, Petroleum, Prices


class ProdictionPlaceAdmin(admin.ModelAdmin):
    list_display = ('basis', 'rzd_code', 'name')
    list_filter = ('basis', 'rzd_code', 'name')


admin.site.register(ProductionPlace, ProdictionPlaceAdmin)


admin.site.register(Basis)
admin.site.register(Depot)
admin.site.register(ProductKey)
admin.site.register(Petroleum)
admin.site.register(Prices)
