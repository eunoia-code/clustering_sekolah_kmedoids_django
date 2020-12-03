# serializers
from rest_framework import serializers
from .models import data_siswa, cluster_siswa, data_sekolah


class SiswaSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = data_siswa
        fields = ["nama", "alamat", "sekolah", "lintang", "bujur"]

class SekolahSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = data_sekolah
        fields = ["nama", "lintang", "bujur"]

class ClusterSerializer(serializers.ModelSerializer):
    Siswa = SiswaSerializer(source='id_siswa', read_only=True)

    class Meta:
        model = cluster_siswa
        fields = '__all__'

class GroupClusterSerializer(serializers.ModelSerializer):
    total=serializers.IntegerField(read_only=True)
    class Meta:
        model = cluster_siswa
        fields = ["cluster", "total"]