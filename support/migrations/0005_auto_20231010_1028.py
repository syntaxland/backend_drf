# Generated by Django 3.2.20 on 2023-10-10 09:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('support', '0004_auto_20231010_0931'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='supportmessage',
            name='ticket',
        ),
        migrations.AddField(
            model_name='supportmessage',
            name='support_ticket',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='support_ticket', to='support.supportticket'),
        ),
    ]
