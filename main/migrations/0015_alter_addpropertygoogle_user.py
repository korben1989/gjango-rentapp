# Generated by Django 4.2.4 on 2023-09-05 16:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0014_alter_addpropertygoogle_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='addpropertygoogle',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
