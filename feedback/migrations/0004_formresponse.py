# Generated by Django 5.1.6 on 2025-03-06 11:53

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feedback', '0003_formfield'),
    ]

    operations = [
        migrations.CreateModel(
            name='FormResponse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.JSONField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('form', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='responses', to='feedback.feedbackform')),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
    ]
