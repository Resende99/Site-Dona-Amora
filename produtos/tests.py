from decimal import Decimal
import io
import zipfile

from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse

from .importers import ImportacaoCatalogoErro, importar_catalogo
from .models import Produto, ProdutoImagem, Variacao


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

    def test_detalhe_exibe_galeria_adicional(self):
        ProdutoImagem.objects.create(produto=self.produto, arquivo="produtos/galeria/look-1.jpg", ordem=1)

        response = self.client.get(reverse("detalhe", args=[self.produto.id]))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "look-1.jpg")


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


class ImportacaoCatalogoTests(TestCase):
    def test_importa_produtos_variacoes_e_imagem(self):
        csv_content = "\n".join(
            [
                "nome,descricao,preco,categoria,imagem,tamanho,cor,estoque",
                "Vestido Aurora,Vestido longo floral,149.90,vestidos,aurora.jpg|aurora-costas.jpg,P,Rose,2",
                "Vestido Aurora,Vestido longo floral,149.90,vestidos,aurora.jpg|aurora-costas.jpg,M,Rose,3",
                "Jaqueta Luna,Jaqueta leve,199.90,jaquetas,luna.jpg,G,Preto,1",
            ]
        )
        csv_file = SimpleUploadedFile("catalogo.csv", csv_content.encode("utf-8"), content_type="text/csv")
        imagens_zip = self._criar_zip(
            {
                "aurora.jpg": b"imagem-aurora",
                "aurora-costas.jpg": b"imagem-aurora-costas",
                "luna.jpg": b"imagem-luna",
            }
        )

        resultado = importar_catalogo(arquivo_csv=csv_file, arquivo_imagens=imagens_zip)

        self.assertEqual(resultado.produtos_criados, 2)
        self.assertEqual(resultado.variacoes_criadas, 3)
        self.assertEqual(resultado.imagens_importadas, 3)
        self.assertEqual(Produto.objects.count(), 2)
        self.assertEqual(Variacao.objects.count(), 3)
        self.assertIn("aurora", Produto.objects.get(nome="Vestido Aurora").imagem.name)
        self.assertEqual(ProdutoImagem.objects.filter(produto__nome="Vestido Aurora").count(), 1)

    def test_rejeita_csv_sem_colunas_obrigatorias(self):
        csv_file = SimpleUploadedFile(
            "catalogo.csv",
            b"nome,preco\nVestido Aurora,149.90\n",
            content_type="text/csv",
        )

        with self.assertRaises(ImportacaoCatalogoErro):
            importar_catalogo(arquivo_csv=csv_file)

    def _criar_zip(self, arquivos):
        buffer = io.BytesIO()
        with zipfile.ZipFile(buffer, "w") as zip_file:
            for nome, conteudo in arquivos.items():
                zip_file.writestr(nome, conteudo)
        buffer.seek(0)
        return SimpleUploadedFile("imagens.zip", buffer.getvalue(), content_type="application/zip")
