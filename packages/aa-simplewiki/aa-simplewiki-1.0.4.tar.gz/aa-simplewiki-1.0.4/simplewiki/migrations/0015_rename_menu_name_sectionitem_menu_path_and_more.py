# Generated by Django 4.0.10 on 2023-04-14 18:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('simplewiki', '0014_alter_menuitem_group_alter_menuitem_icon_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='sectionitem',
            old_name='menu_name',
            new_name='menu_path',
        ),
        migrations.AlterField(
            model_name='sectionitem',
            name='content',
            field=models.TextField(blank=True, help_text='Optional: This will be displayed as your main content of the section. You can use HTML.', null=True),
        ),
    ]
