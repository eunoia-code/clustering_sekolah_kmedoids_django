from django.contrib import admin
from .models import upload_data, data_siswa, cluster_siswa, data_sekolah
from import_export.admin import ImportExportModelAdmin

# Register your models here.
admin.site.register(upload_data)
#admin.site.register(cluster_siswa)
# admin.site.register(data_sekolah)
@admin.register(data_siswa)
class DataSiswaAdmin(ImportExportModelAdmin):
    pass

@admin.register(data_sekolah)
class DataSekolahAdmin(ImportExportModelAdmin):
    pass

@admin.register(cluster_siswa)
class ClusterSiswaAdmin(ImportExportModelAdmin):
    pass