from django.contrib import admin
from .models import Produto, Variacao

class VariacaoInline(admin.TabularInline):
    model = Variacao
    extra = 3

@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    inlines = [VariacaoInline]
    list_display = ("nome", "categoria", "preco", "criado_em")
    list_filter = ("categoria", "criado_em")
    search_fields = ("nome", "descricao")
