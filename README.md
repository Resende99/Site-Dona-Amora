# Site Dona Amora

Loja virtual em Django para apresentar o catalogo da Dona Amora, com vitrine de produtos, pagina de detalhes e painel admin para cadastrar pecas manualmente ou importar o catalogo em lote.

## Recursos

- Vitrine inicial com destaque de produtos.
- Listagem completa com filtro por categoria.
- Pagina de detalhe com descricao, variacoes e galeria de fotos.
- Painel admin do Django para cadastro manual.
- Importacao em lote por `CSV + ZIP de imagens`.
- Suporte a varias fotos por produto.
- Link direto para atendimento via WhatsApp.

## Tecnologias

- Python
- Django
- SQLite
- HTML + CSS

## Como rodar localmente

1. Clone o repositorio:

```bash
git clone https://github.com/Resende99/Site-Dona-Amora.git
cd Site-Dona-Amora
```

2. Crie e ative um ambiente virtual.

No Windows:

```powershell
python -m venv venv
venv\Scripts\activate
```

3. Instale as dependencias:

```bash
pip install django pillow
```

4. Defina a chave do Django:

```powershell
$env:DJANGO_SECRET_KEY="sua-chave-secreta"
```

5. Rode as migrations:

```bash
python manage.py migrate
```

6. Crie um usuario admin:

```bash
python manage.py createsuperuser
```

7. Inicie o servidor:

```bash
python manage.py runserver
```

Abra `http://127.0.0.1:8000/` no navegador.

## Variaveis de ambiente

O projeto usa estas variaveis:

- `DJANGO_SECRET_KEY`: obrigatoria fora de `DEBUG`.
- `DJANGO_DEBUG`: ativa modo debug quando usar `1`, `true`, `yes` ou `on`.
- `DJANGO_ALLOWED_HOSTS`: lista separada por virgula.
- `WHATSAPP_NUMBER`: numero usado nos links do WhatsApp.
- `INSTAGRAM_HANDLE`: usuario do Instagram.
- `INSTAGRAM_URL`: link completo do Instagram.

## Admin e catalogo

No admin do Django, o cadastro pode ser feito de dois jeitos:

- Manualmente, produto por produto.
- Em lote, pelo botao `Importar catalogo`.

### Formato do CSV

Cada linha representa uma variacao do produto:

```csv
nome,descricao,preco,categoria,imagem,tamanho,cor,estoque
Vestido Aurora,Vestido longo floral,149.90,vestidos,aurora.jpg|aurora-costas.jpg,P,Rose,2
Vestido Aurora,Vestido longo floral,149.90,vestidos,aurora.jpg|aurora-costas.jpg,M,Rose,3
Jaqueta Luna,Jaqueta leve,199.90,jaquetas,luna.jpg,G,Preto,1
```

### Regras da importacao

- A coluna `imagem` aceita uma ou varias fotos.
- Para varias fotos, separe os nomes com `|`.
- O arquivo de imagens deve ser enviado em `.zip`.
- Os nomes dos arquivos no `.zip` precisam bater com os nomes informados no CSV.
- Categorias aceitas: `vestidos`, `blusas`, `calcas`, `conjuntos`, `saias`, `shorts`, `jaquetas`.

## Testes

Para rodar os testes:

```powershell
$env:DJANGO_SECRET_KEY="teste-local"
python manage.py test produtos
```

## Estrutura principal

```text
loja/                 Configuracoes do projeto Django
produtos/             App principal de catalogo
templates/            Templates HTML
static/               Arquivos estaticos
media/                Uploads de imagens
```

## Proximos passos

- Melhorar a galeria com troca de foto ao clicar na miniatura.
- Adicionar download de modelo CSV no admin.
- Permitir importacao por Excel (`.xlsx`).
