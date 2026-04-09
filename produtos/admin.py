from django.contrib import admin, messages
from django.contrib.auth.models import Group, User
from django.http import HttpResponseRedirect
from django.template.response import TemplateResponse
from django.urls import path, reverse

from .forms import CatalogoImportForm
from .importers import ImportacaoCatalogoErro, importar_catalogo
from .models import Produto, ProdutoImagem, Variacao

admin.site.site_header = "Admin Dona Amora"
admin.site.site_title = "Admin Dona Amora"
admin.site.index_title = "Painel Dona Amora"
admin.site.unregister(User)
admin.site.unregister(Group)


class VariacaoInline(admin.TabularInline):
    model = Variacao
    extra = 3


class ProdutoImagemInline(admin.TabularInline):
    model = ProdutoImagem
    extra = 1


@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    change_list_template = "admin/produtos/produto/change_list.html"
    inlines = [VariacaoInline, ProdutoImagemInline]
    list_display = ("nome", "categoria", "preco", "criado_em")
    list_filter = ("categoria", "criado_em")
    search_fields = ("nome", "descricao")

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                "importar-catalogo/",
                self.admin_site.admin_view(self.importar_catalogo_view),
                name="produtos_produto_importar_catalogo",
            ),
        ]
        return custom_urls + urls

    def importar_catalogo_view(self, request):
        if request.method == "POST":
            form = CatalogoImportForm(request.POST, request.FILES)
            if form.is_valid():
                try:
                    resultado = importar_catalogo(
                        arquivo_csv=form.cleaned_data["arquivo_csv"],
                        arquivo_imagens=form.cleaned_data.get("arquivo_imagens"),
                        atualizar_existentes=form.cleaned_data["atualizar_existentes"],
                    )
                except ImportacaoCatalogoErro as exc:
                    self.message_user(request, str(exc), level=messages.ERROR)
                else:
                    self.message_user(
                        request,
                        (
                            f"Importacao concluida: {resultado.produtos_criados} produto(s) criado(s), "
                            f"{resultado.produtos_atualizados} atualizado(s), "
                            f"{resultado.variacoes_criadas} variacao(oes) criada(s) e "
                            f"{resultado.imagens_importadas} imagem(ns) importada(s)."
                        ),
                        level=messages.SUCCESS,
                    )
                    return HttpResponseRedirect(reverse("admin:produtos_produto_changelist"))
        else:
            form = CatalogoImportForm()

        context = {
            **self.admin_site.each_context(request),
            "opts": self.model._meta,
            "form": form,
            "title": "Importar catalogo",
            "has_view_permission": self.has_view_permission(request),
        }
        return TemplateResponse(request, "admin/produtos/produto/importar_catalogo.html", context)
