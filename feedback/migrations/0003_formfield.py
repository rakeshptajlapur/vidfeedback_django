# Generated by Django 5.1.6 on 2025-03-06 10:55

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feedback', '0002_feedbackform_slug'),
    ]

    operations = [
        migrations.CreateModel(
            name='FormField',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=100)),
                ('field_type', models.CharField(choices=[('text', 'Text Input'), ('textarea', 'Text Area'), ('video', 'Video Upload'), ('rating', 'Star Rating'), ('checkbox', 'Checkbox'), ('email', 'Email Input')], max_length=20)),
                ('required', models.BooleanField(default=True)),
                ('order', models.PositiveIntegerField(default=0)),
                ('form', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='fields', to='feedback.feedbackform')),
            ],
            options={
                'ordering': ['order'],
            },
        ),
    ]
