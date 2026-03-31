from decimal import Decimal

from django.core.exceptions import ValidationError
from django.test import TestCase
from django.urls import reverse

from .models import Produto, Variacao


class ProdutoViewsTests(TestCase):
    def setUp(self):
        self.produto = Produto.objects.create(
            nome="Vestido Aurora",
            descricao="Vestido longo floral",
            preco=Decimal("149.90"),
            categoria="vestidos",
        )
        Variacao.objects.create(
            produto=self.produto,
            tamanho="M",
            cor="Rose",
            estoque=3,
        )

    def test_home_carrega_produtos(self):
        response = self.client.get(reverse("index"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Vestido Aurora")

    def test_lista_filtra_por_categoria(self):
        Produto.objects.create(
            nome="Jaqueta Luna",
            descricao="Jaqueta leve",
            preco=Decimal("199.90"),
            categoria="jaquetas",
        )

        response = self.client.get(reverse("todos_produtos"), {"categoria": "vestidos"})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Vestido Aurora")
        self.assertNotContains(response, "Jaqueta Luna")

    def test_detalhe_carrega_produto(self):
        response = self.client.get(reverse("detalhe", args=[self.produto.id]))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Vestido Aurora")
        self.assertContains(response, "Rose")


class ProdutoModelTests(TestCase):
    def test_preco_nao_aceita_valor_negativo(self):
        produto = Produto(
            nome="Teste",
            descricao="",
            preco=Decimal("-1.00"),
            categoria="vestidos",
        )

        with self.assertRaises(ValidationError):
            produto.full_clean()
