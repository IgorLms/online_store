# Generated by Django 4.2.7 on 2023-11-07 14:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('online_store_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, verbose_name='Категории товаров')),
                ('description', models.TextField(blank=True, max_length=500, null=True, verbose_name='Описание категории')),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Название товара')),
                ('description', models.TextField(blank=True, max_length=500, null=True, verbose_name='Описание товара')),
                ('price', models.DecimalField(decimal_places=2, max_digits=19, verbose_name='Цена товара')),
                ('quantity', models.PositiveIntegerField(verbose_name='Количество товара')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='online_store_app.category', verbose_name='Категория')),
            ],
        ),
        migrations.CreateModel(
            name='HistoryChanges',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_changes', models.DateTimeField(auto_now_add=True, verbose_name='Дата изменения товара')),
                ('quantity_old', models.PositiveIntegerField(verbose_name='Количество товара до изменения')),
                ('quantity_now', models.PositiveIntegerField(verbose_name='Количество товара после изменения')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='history', to='online_store_app.product', verbose_name='Название товара')),
            ],
        ),
    ]