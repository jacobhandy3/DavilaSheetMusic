# Generated by Django 3.2.3 on 2021-06-03 22:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0002_auto_20210603_2237'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='productresources',
            options={'ordering': ['product', 'name'], 'verbose_name_plural': 'Product Resources'},
        ),
        migrations.AlterModelOptions(
            name='sheetmusic',
            options={'ordering': ['title'], 'verbose_name_plural': 'Sheet Music'},
        ),
    ]