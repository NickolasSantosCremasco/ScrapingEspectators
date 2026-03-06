from django.contrib import admin
from .models import Prospect


@admin.register(Prospect)
class ProspectAdmin(admin.ModelAdmin):
    # Campos que aparecem na tabela principal
    list_display = ('name', 'relevance_score', 'keyword', 'platform', 'created_at')

    # Filtros combinados (Plataforma e Palavra-chave) na lateral direita
    list_filter = ('platform', 'keyword')

    # Busca abrangente (Headline e Bio são fundamentais para o seu scoring)
    search_fields = ('name', 'headline', 'bio', 'keyword')

    # Os leads mais quentes (maior score) aparecem no topo por padrão
    ordering = ('-relevance_score',)