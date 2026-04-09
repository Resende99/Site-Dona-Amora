import csv
import io
import zipfile
from dataclasses import dataclass
from decimal import Decimal, InvalidOperation

from django.core.files.base import ContentFile
from django.db import transaction

from .models import Produto, ProdutoImagem, Variacao


class ImportacaoCatalogoErro(Exception):
    pass


@dataclass
class ImportacaoCatalogoResultado:
    produtos_criados: int = 0
    produtos_atualizados: int = 0
    variacoes_criadas: int = 0
    imagens_importadas: int = 0


def importar_catalogo(*, arquivo_csv, arquivo_imagens=None, atualizar_existentes=True):
    try:
        conteudo_csv = arquivo_csv.read().decode("utf-8-sig")
    except UnicodeDecodeError as exc:
        raise ImportacaoCatalogoErro("O CSV precisa estar em UTF-8.") from exc

    leitor = csv.DictReader(io.StringIO(conteudo_csv))
    colunas_obrigatorias = {"nome", "descricao", "preco", "categoria", "imagem", "tamanho", "cor", "estoque"}
    colunas_encontradas = set(leitor.fieldnames or [])
    colunas_faltando = colunas_obrigatorias - colunas_encontradas
    if colunas_faltando:
        faltando = ", ".join(sorted(colunas_faltando))
        raise ImportacaoCatalogoErro(f"Colunas obrigatorias ausentes no CSV: {faltando}.")

    categorias_validas = {valor for valor, _ in Produto.CATEGORIAS}
    imagens_zip = _carregar_imagens_zip(arquivo_imagens) if arquivo_imagens else {}
    resultado = ImportacaoCatalogoResultado()
    produtos_por_nome = {}
    imagens_importadas_por_produto = set()

    with transaction.atomic():
        for indice, linha in enumerate(leitor, start=2):
            nome = (linha.get("nome") or "").strip()
            if not nome:
                raise ImportacaoCatalogoErro(f"Linha {indice}: informe o nome do produto.")

            categoria = (linha.get("categoria") or "").strip()
            if categoria and categoria not in categorias_validas:
                raise ImportacaoCatalogoErro(
                    f"Linha {indice}: categoria '{categoria}' invalida. "
                    f"Use uma das categorias cadastradas no sistema."
                )

            preco = _parse_preco(linha.get("preco"), indice)
            defaults = {
                "descricao": (linha.get("descricao") or "").strip(),
                "preco": preco,
                "categoria": categoria,
            }

            produto = produtos_por_nome.get(nome)
            produto_criado = False

            if produto is None:
                if atualizar_existentes:
                    produto, produto_criado = Produto.objects.update_or_create(
                        nome=nome,
                        defaults=defaults,
                    )
                else:
                    produto, produto_criado = Produto.objects.get_or_create(
                        nome=nome,
                        defaults=defaults,
                    )
                    if not produto_criado:
                        produtos_por_nome[nome] = produto
                        continue

                produtos_por_nome[nome] = produto
                if produto_criado:
                    resultado.produtos_criados += 1
                else:
                    resultado.produtos_atualizados += 1

            nomes_imagem = _parse_nomes_imagem(linha.get("imagem"))
            if nomes_imagem and produto.pk not in imagens_importadas_por_produto:
                if atualizar_existentes:
                    produto.imagens_adicionais.all().delete()

                for ordem, nome_imagem in enumerate(nomes_imagem):
                    if nome_imagem not in imagens_zip:
                        continue

                    conteudo = ContentFile(imagens_zip[nome_imagem], name=nome_imagem)
                    if ordem == 0:
                        produto.imagem.save(nome_imagem, conteudo, save=True)
                    else:
                        imagem_adicional = ProdutoImagem(produto=produto, ordem=ordem)
                        imagem_adicional.arquivo.save(nome_imagem, conteudo, save=True)

                    resultado.imagens_importadas += 1

                imagens_importadas_por_produto.add(produto.pk)

            tamanho = (linha.get("tamanho") or "").strip()
            cor = (linha.get("cor") or "").strip()
            estoque_str = (linha.get("estoque") or "").strip()

            if tamanho or cor or estoque_str:
                estoque = _parse_estoque(estoque_str, indice)
                _, variacao_criada = Variacao.objects.get_or_create(
                    produto=produto,
                    tamanho=tamanho,
                    cor=cor,
                    defaults={"estoque": estoque},
                )
                if variacao_criada:
                    resultado.variacoes_criadas += 1
                elif atualizar_existentes:
                    Variacao.objects.filter(
                        produto=produto,
                        tamanho=tamanho,
                        cor=cor,
                    ).update(estoque=estoque)

    return resultado


def _carregar_imagens_zip(arquivo_imagens):
    try:
        with zipfile.ZipFile(arquivo_imagens) as zip_file:
            return {
                info.filename.split("/")[-1]: zip_file.read(info.filename)
                for info in zip_file.infolist()
                if not info.is_dir()
            }
    except zipfile.BadZipFile as exc:
        raise ImportacaoCatalogoErro("O arquivo de imagens precisa ser um ZIP valido.") from exc


def _parse_preco(valor, indice):
    texto = (valor or "").strip().replace(",", ".")
    try:
        preco = Decimal(texto)
    except (InvalidOperation, TypeError) as exc:
        raise ImportacaoCatalogoErro(f"Linha {indice}: preco invalido '{valor}'.") from exc

    if preco < 0:
        raise ImportacaoCatalogoErro(f"Linha {indice}: preco nao pode ser negativo.")

    return preco


def _parse_estoque(valor, indice):
    texto = (valor or "0").strip()
    if not texto:
        return 0

    try:
        estoque = int(texto)
    except ValueError as exc:
        raise ImportacaoCatalogoErro(f"Linha {indice}: estoque invalido '{valor}'.") from exc

    if estoque < 0:
        raise ImportacaoCatalogoErro(f"Linha {indice}: estoque nao pode ser negativo.")

    return estoque


def _parse_nomes_imagem(valor):
    return [nome.strip() for nome in (valor or "").split("|") if nome.strip()]
