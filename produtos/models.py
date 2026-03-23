from django.db import models

class Produto(models.Model):
    CATEGORIAS = [
        ('vestidos', 'Vestidos'),
        ('blusas', 'Blusas'),
        ('calcas', 'Calças'),
        ('conjuntos', 'Conjuntos'),
        ('saias', 'Saias'),
        ('shorts', 'Shorts'),
        ('jaquetas', 'Jaquetas'),
    ]

    nome = models.CharField(max_length=200, default='')
    descricao = models.TextField(blank=True, default='')
    preco = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    categoria = models.CharField(max_length=20, choices=CATEGORIAS, blank=True, default='')
    imagem = models.ImageField(upload_to='produtos/', blank=True, null=True)
    criado_em = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.nome


class Variacao(models.Model):
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE, related_name='variacoes')
    tamanho = models.CharField(max_length=10)
    cor = models.CharField(max_length=50, blank=True, default='')
    estoque = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.produto.nome} - {self.tamanho} - {self.cor}'