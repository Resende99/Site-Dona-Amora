from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("produtos", "0008_alter_produto_preco_alter_variacao_estoque"),
    ]

    operations = [
        migrations.CreateModel(
            name="ProdutoImagem",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("arquivo", models.ImageField(upload_to="produtos/galeria/")),
                ("ordem", models.PositiveIntegerField(default=0)),
                (
                    "produto",
                    models.ForeignKey(on_delete=models.deletion.CASCADE, related_name="imagens_adicionais", to="produtos.produto"),
                ),
            ],
            options={
                "ordering": ("ordem", "id"),
            },
        ),
    ]
