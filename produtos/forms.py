from django import forms


class CatalogoImportForm(forms.Form):
    arquivo_csv = forms.FileField(
        label="Planilha CSV",
        help_text=(
            "Use uma linha por variacao. Colunas: nome, descricao, preco, categoria, "
            "imagem, tamanho, cor, estoque. Para varias fotos, separe os nomes com |."
        ),
    )
    arquivo_imagens = forms.FileField(
        label="ZIP com imagens",
        required=False,
        help_text="Opcional. O nome do arquivo no ZIP deve bater com a coluna imagem do CSV.",
    )
    atualizar_existentes = forms.BooleanField(
        label="Atualizar produtos ja existentes",
        required=False,
        initial=True,
    )
