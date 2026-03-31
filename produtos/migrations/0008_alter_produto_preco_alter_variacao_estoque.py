# Generated manually to keep deploy deterministic.

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("produtos", "0007_produto_categoria"),
    ]

    operations = [
        migrations.AlterField(
            model_name="produto",
            name="preco",
            field=models.DecimalField(
                decimal_places=2,
                default=0,
                max_digits=8,
                validators=[django.core.validators.MinValueValidator(0)],
            ),
        ),
        migrations.AlterField(
            model_name="variacao",
            name="estoque",
            field=models.PositiveIntegerField(default=0),
        ),
    ]
