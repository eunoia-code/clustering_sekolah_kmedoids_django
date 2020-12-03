from import_export import resources
from .models import data_siswa

class DataSiswaResource(resources.ModelResource):
    class Meta:
        model = data_siswa