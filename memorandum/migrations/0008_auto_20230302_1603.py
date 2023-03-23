# Generated by Django 3.2.9 on 2023-03-02 21:03

from django.db import migrations, models
import memorandum.models


class Migration(migrations.Migration):

    dependencies = [
        ('memorandum', '0007_alter_menorandum_archivos'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='menorandum',
            options={'permissions': (('can_download_file', 'Puede descargar archivos asociados'),), 'verbose_name': 'Memorandum', 'verbose_name_plural': 'Memorandums'},
        ),
        migrations.AlterField(
            model_name='menorandum',
            name='archivos',
            field=models.FileField(blank=True, null=True, upload_to=memorandum.models.user_directory_path),
        ),
    ]