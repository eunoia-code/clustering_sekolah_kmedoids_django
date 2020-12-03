# Generated by Django 3.0.7 on 2020-08-31 07:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web_dcluster', '0005_auto_20200830_2042'),
    ]

    operations = [
        migrations.CreateModel(
            name='data_sekolah',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nama', models.CharField(max_length=50)),
                ('alamat', models.TextField()),
                ('lintang', models.FloatField(max_length=30)),
                ('bujur', models.FloatField(max_length=30)),
            ],
        ),
    ]
