# Generated by Django 4.2.3 on 2024-08-30 07:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0002_product_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='instock',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='quantity',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]
