# Generated by Django 4.2.1 on 2023-06-24 17:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0005_wishlist'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wishlist',
            name='userwish',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.profile'),
        ),
    ]
