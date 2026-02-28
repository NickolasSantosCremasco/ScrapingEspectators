from django.contrib import admin
from .models import Prospect

@admin.register(Prospect)
class ProspectAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'platform',
        'role',
        'relevance_score',
        'created_at'
    )
    search_fields = ('name', 'headline', 'bio', 'keywords')
    list_filter = ('platform',)