from django.core.validators import MinValueValidator
from django.db import models


class Produto(models.Model):
    CATEGORIAS = [
        ("vestidos", "Vestidos"),
        ("blusas", "Blusas"),
        ("calcas", "Calças"),
        ("conjuntos", "Conjuntos"),
        ("saias", "Saias"),
        ("shorts", "Shorts"),
        ("jaquetas", "Jaquetas"),
    ]

    nome = models.CharField(max_length=200, default="")
    descricao = models.TextField(blank=True, default="")
    preco = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(0)],
    )
    categoria = models.CharField(max_length=20, choices=CATEGORIAS, blank=True, default="")
    imagem = models.ImageField(upload_to="produtos/", blank=True, null=True)
    criado_em = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.nome

    @property
    def galeria_imagens(self):
        imagens = list(self.imagens_adicionais.all())
        if self.imagem:
            return [self.imagem, *[imagem.arquivo for imagem in imagens]]
        return [imagem.arquivo for imagem in imagens]


class Variacao(models.Model):
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE, related_name="variacoes")
    tamanho = models.CharField(max_length=10)
    cor = models.CharField(max_length=50, blank=True, default="")
    estoque = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.produto.nome} - {self.tamanho} - {self.cor}"


class ProdutoImagem(models.Model):
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE, related_name="imagens_adicionais")
    arquivo = models.ImageField(upload_to="produtos/galeria/")
    ordem = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ("ordem", "id")

    def __str__(self):
        return f"Imagem de {self.produto.nome}"
