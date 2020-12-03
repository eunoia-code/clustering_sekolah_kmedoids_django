from django import forms
from .models import upload_data,data_siswa


class Upload_dataForm(forms.ModelForm):

    class Meta:
        model = upload_data
        fields = [
            'isi',

        ]


class DataForm(forms.ModelForm):

    class Meta:
        model = data_siswa
        fields = [
            'nama',
            'alamat',
            'sekolah',
            'lintang',
            'bujur',
        ]
