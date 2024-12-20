# Generated by Django 4.2.3 on 2024-09-06 07:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0004_alter_product_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='contactList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('topic', models.CharField(max_length=200)),
                ('email', models.CharField(max_length=100)),
                ('detail', models.TextField(blank=True, null=True)),
                ('complete', models.BooleanField(default=False)),
            ],
        ),
    ]
