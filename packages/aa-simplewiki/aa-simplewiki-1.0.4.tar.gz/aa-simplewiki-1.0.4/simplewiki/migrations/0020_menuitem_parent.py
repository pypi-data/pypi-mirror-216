# Generated by Django 4.0.10 on 2023-04-20 07:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('simplewiki', '0019_alter_general_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='menuitem',
            name='parent',
            field=models.CharField(blank=True, help_text='Optional: Write the path of the parent menu. If you want this menu to be the parent leave this field empty.', max_length=255, null=True),
        ),
    ]
