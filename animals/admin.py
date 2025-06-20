from django.contrib import admin

from zoo.admin import admin_site
from .models import Animal, Procedure, Section


@admin.register(Animal)
class AnimalAdmin(admin.ModelAdmin):
    list_display = ('name', 'species', 'section', 'arrival_date')
    list_filter = ('section', 'species')
    search_fields = ('name', 'species')
    readonly_fields = ('arrival_date',)
    fieldsets = (
        (None, {
            'fields': ('name', 'species', 'section')
        }),
        ('Дополнительно', {
            'fields': ('birth_date', 'arrival_date'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Procedure)
class ProcedureAdmin(admin.ModelAdmin):
    list_display = ('animal', 'procedure_type', 'datetime', 'short_details')
    list_filter = ('procedure_type', 'datetime')
    search_fields = ('animal__name', 'details')
    date_hierarchy = 'datetime'

    def short_details(self, obj):
        return obj.details[:50] + '...' if len(obj.details) > 50 else obj.details

    short_details.short_description = 'Детали'


@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = ('name', 'animal_count')
    search_fields = ('name',)

    def animal_count(self, obj):
        return obj.animals.count()

    animal_count.short_description = 'Количество животных'


admin_site.register(Animal, AnimalAdmin)
admin_site.register(Procedure, ProcedureAdmin)
admin_site.register(Section, SectionAdmin)
