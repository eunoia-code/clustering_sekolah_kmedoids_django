from django.db import models
import os
from uuid import uuid4
# Create your models here.


def path_and_rename(instance, filename):
    upload_to = 'data'
    ext = filename.split('.')[-1]
    # get filename
    if instance.pk:
        filename = '{}.{}'.format(instance.pk, ext)
    else:
        # set filename as random string
        filename = '{}.{}'.format(uuid4().hex, ext)
    # return the whole path to the file
    return os.path.join(upload_to, filename)

class upload_data(models.Model):
    isi = models.FileField(upload_to='documents\\')


class data_siswa(models.Model):
    nama = models.CharField(max_length=50)
    alamat = models.TextField()
    sekolah = models.CharField(max_length=100)
    lintang = models.FloatField(max_length=30)
    bujur = models.FloatField(max_length=30)


class data_sekolah(models.Model):
    nama = models.CharField(max_length=50)
    lintang = models.FloatField(max_length=30)
    bujur = models.FloatField(max_length=30)

class cluster_siswa(models.Model):
    id_siswa = models.ForeignKey(data_siswa, on_delete=models.CASCADE)
    cluster = models.IntegerField()


