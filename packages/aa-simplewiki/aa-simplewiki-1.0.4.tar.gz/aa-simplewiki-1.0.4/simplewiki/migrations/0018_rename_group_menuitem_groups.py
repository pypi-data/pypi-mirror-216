# Generated by Django 4.0.10 on 2023-04-17 14:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('simplewiki', '0017_alter_sectionitem_content_alter_sectionitem_title'),
    ]

    operations = [
        migrations.RenameField(
            model_name='menuitem',
            old_name='group',
            new_name='groups',
        ),
    ]
