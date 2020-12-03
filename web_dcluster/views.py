from django.core import serializers
from django.http import HttpResponse, JsonResponse
from django.db.models import Count

from .serializersss import SiswaSerializer, ClusterSerializer, SekolahSerializer,GroupClusterSerializer
from rest_framework import routers, serializers, viewsets

from django.shortcuts import render, redirect
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.preprocessing import LabelEncoder
import numpy as np
from tablib import Dataset

from .k_medoids import k_medoids
import csv,io
import json
# Create your views here.
from django.shortcuts import render
from django.contrib import messages

from django.contrib.auth import authenticate, login
from .forms import Upload_dataForm,DataForm
from .models import upload_data, data_siswa, data_sekolah,cluster_siswa
from .resources import DataSiswaResource
from .LazyEncoder import LazyEncoder
import os
from django.conf import settings
from django_filters.rest_framework import DjangoFilterBackend

class SiswaViewSet(viewsets.ModelViewSet):
    serializer_class = SiswaSerializer
    queryset = data_siswa.objects.all()

class SekolahViewSet(viewsets.ModelViewSet):
    serializer_class = SekolahSerializer
    queryset = data_sekolah.objects.all()

class ClusterViewSet(viewsets.ModelViewSet):
    serializer_class = ClusterSerializer
    queryset = cluster_siswa.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['cluster', 'id']

class AllClusterViewSet(viewsets.ModelViewSet):
    serializer_class = ClusterSerializer
    queryset = cluster_siswa.objects.all()

class GroupClusterViewSet(viewsets.ModelViewSet):
    serializer_class = GroupClusterSerializer
    queryset = cluster_siswa.objects.values('cluster').annotate(total=Count('cluster')).order_by('cluster')

def index2(request):
    # cluster_siswa.objects.all().delete()
    # Upload_data = upload_data.objects.filter(id=1).values_list('isi')[0]
    # Upload_data = Upload_data[0]
    dat = open(os.path.join(settings.MEDIA_ROOT, 'documents/sas1_2y8EKxJ.csv'))
    df = pd.read_csv(dat, delimiter=';', encoding='utf-8')
    df = df.dropna()
    df.columns = ['Date', 'nama', 'kelamin', 'asal', 'jurusan', 'semester', 'info', 'dorogan', 'alasan', 'pendapat',
                  'peluang']
    
    df_jurusan = df.groupby(['jurusan']).size().reset_index(name='value')
    nama_jurusan=df_jurusan.jurusan.tolist()
    jml_jurusan=df_jurusan.value.tolist()

    df_JK = df.groupby(['kelamin']).size().reset_index(name='value')
    nama_JK = df_JK.kelamin.tolist()
    jml_JK = df_JK.value.tolist()
    le = LabelEncoder()
    df_encoded = df.apply(le.fit_transform)
    df_encoded
    X = np.array(df_encoded)

    k = 23
    model = k_medoids(k)
    # print('Centers found by your model:')
    
    model.fit(X)
    m = model.fit(X)
    context={
        'nama_JK':nama_JK,
        'jml_JK': jml_JK,
        'jml_jurusan':jml_jurusan,
        'nama_jurusan':nama_jurusan
    }
    return render(request, 'home2.html', context)

def cluster():
    sekolah = data_sekolah.objects.all()
    df_sekolah = pd.DataFrame(list(sekolah.values()))
    df_sekolah = df_sekolah[["id","nama","lintang","bujur"]]
    id_siswa = data_siswa.objects.all()
    df_siswa = pd.DataFrame(list(id_siswa.values()))
    df_siswa1=df_siswa.iloc[-1:]
    df_siswa = df_siswa1[["id","nama", "lintang", "bujur"]]
    frames=[df_sekolah,df_siswa]
    df = pd.concat(frames)
    le = LabelEncoder()
    df_encoded = df.apply(le.fit_transform)
    df_encoded
    X = np.array(df_encoded)
    
    #k = 23
    k = data_sekolah.objects.count()
    model = k_medoids(k)
    # print('Centers found by your model:')
    model.fit(X)

    pred = model.predict(X)
    # gambar(X, pred)
    X = X.tolist()
    pred = pred.tolist()
    mahasiswa = df.values.tolist()
    df['pred']=pred
    last = df_siswa1.iloc[-1:]
    last1 = df.iloc[-1:]
    pk=last['id'].values[-1]
    nama_last = last['nama'].values[-1]
    lintang_last = last['lintang'].values[-1]
    bujur_last = last['bujur'].values[-1]
    alamat_last = last['alamat'].values[-1]
    sekolah_last = last['sekolah'].values[-1]
    c=last1['pred'].values[-1]
    cluster_siswas = cluster_siswa()
    cluster_siswas.id_siswa = data_siswa.objects.get(nama=nama_last,alamat=alamat_last,sekolah=sekolah_last,bujur=bujur_last,lintang=lintang_last)
    cluster_siswas.cluster = c
    cluster_siswas.save()


def cluster_update(id):
    pk = int(id)
    sekolah = data_sekolah.objects.all()
    df_sekolah = pd.DataFrame(list(sekolah.values()))
    df_sekolah = df_sekolah[["id", "nama", "lintang", "bujur"]]
    id_siswa = data_siswa.objects.all()
    df_siswa = pd.DataFrame(list(id_siswa.values()))
    
    df_siswa = df_siswa[["id", "nama", "lintang", "bujur"]]
    df_siswa1 = df_siswa.loc[df_siswa['id'] == pk]
    frames = [df_sekolah, df_siswa1]
    df = pd.concat(frames)
    le = LabelEncoder()
    df_encoded = df.apply(le.fit_transform)
    df_encoded
    X = np.array(df_encoded)

    #k = 23
    k = data_sekolah.objects.count()
    model = k_medoids(k)
    # print('Centers found by your model:')
    model.fit(X)

    pred = model.predict(X)
    # gambar(X, pred)
    X = X.tolist()
    pred = pred.tolist()
    mahasiswa = df.values.tolist()
    df['pred'] = pred
    last = df_siswa1
    last1 = df.iloc[-1:]
    nama_last = df_siswa1['nama'].values[0]
    lintang_last = df_siswa1['lintang'].values[0]
    bujur_last = df_siswa1['bujur'].values[0]
    c = last1['pred'].values[-1]
    #cluster_siswas = cluster_siswa.objects.get(id_siswa=pk)
    cluster_siswas = cluster_siswa()
    cluster_siswas.id_siswa = data_siswa.objects.get(
        nama=nama_last, bujur=bujur_last, lintang=lintang_last)
    cluster_siswas.cluster = c
    cluster_siswas.save()
    
    

def create_data(request):
    if request.method == 'POST':
        form = DataForm(request.POST)
        if form.is_valid():
            form.save()
            cluster()
            return redirect('data')
    else:
        form = DataForm()
    return render(request, 'upload_form.html', {
        'form': form
    })

def update(request, id):
    data_siswas = data_siswa.objects.get(id=id)
    if request.method == 'POST':
        form = DataForm(
            request.POST,instance=data_siswas)
        
        if form.is_valid():
            form.save()
            cluster_update(id)
            
            return redirect('data')
    else:
        form = DataForm(instance=data_siswas)
        return render(request, 'upload_form.html', {'form': form})


def delete(request, id):
    id = int(id)
    try:
        siswa = data_siswa.objects.get(id=id)
    except data_siswa.DoesNotExist:
        return redirect('data')
    siswa.delete()
    return redirect('data')


def data_list(request):
    # Data_siswa = data_siswa.objects.all()
    context = {
        # 'rows': Data_siswa,
    }
    return render(request, 'data.html', context)


def cluster_list(request):
    siswa_cluster = data_siswa.objects.all()

    df_c = pd.DataFrame(list(siswa_cluster.values()))
    df_c = df_c[["id", "nama", "lintang", "bujur"]]
    df_id=df_c.id
    for i in range(len(df_id)):
        cluster_update(df_id[i])

    #df = pd.DataFrame(list(data_siswa.objects.all().values()))
    #le = LabelEncoder()
    #df_encoded = df.apply(le.fit_transform)
    #df_encoded
    #X = np.array(df_encoded)

    #k = 23
    #k = data_sekolah.objects.count()
    #model = k_medoids(k)
    # print('Centers found by your model:')
    #model.fit(X)
    #pred = model.predict(X)
    # gambar(X, pred)
    #X = X.tolist()
    #pred = pred.tolist()
    #mahasiswa = df.values.tolist()
    #df['pred']=pred
    context = {
        # 'columns': df.columns,
        #'rows': df.to_dict('records'),
        'rows': siswa_cluster,
        #'test': df,
        #'mahasiswa': mahasiswa,
        #'data': X,
        # 'cluster': pred,
        #'hello': 'hello world'
    }
    return render(request, 'cluster.html', context)


#def data_list(request):
#    Upload_data = upload_data.objects.all()
#    return render(request, 'data.html', {'Upload_data': Upload_data})


def login(request):
    return render(request, 'login.html', {})

def gambar(X, label):
    x1 = []
    K = np.amax(label) + 1
    for i in range(K):
        x1.append(i)
        x1[i] = X[label == i, :]

    # you can fix this dpi
    # print(K)
    plt.figure(dpi=120)
    colors = ['b^', 'go', 'rs', 'd']
    # print('koor')

    for i in range(len(x1)):
        plt.plot(x1[i][:, 0], x1[i][:, 1], colors[i], markersize=4, alpha=.8)

    plt.axis('equal')
    plt.plot()
    plt.show()

def index(request):
    # siswa = data_siswa.objects.all()
    # siswa = serializers.serialize('json', siswa, cls=LazyEncoder)
    # data = cluster_siswa.objects.all()
    # data = serializers.serialize('json', data, cls=LazyEncoder)
    #
    # context = {
    #     'rows' : data,
    #     'siswa' : siswa
    # }

    return render(request, 'home.html')

def csv(request):
    if request.method == 'POST':
        file_format = request.POST['file-format']
        s = DataSiswaResource()
        dataset = Dataset()
        n = request.FILES['importData']

        if file_format == 'CSV':
            imported_data = dataset.load(n.read().decode('utf-8'), format='csv')
            result = s.import_data(dataset, dry_run=True)
        elif file_format == 'JSON':
            imported_data = dataset.load(n.read().decode('utf-8'), format='json')
            # Testing data import
            result = s.import_data(dataset, dry_run=True)

        if not result.has_errors():
            # Import now
            s.import_data(dataset, dry_run=False)

    return render(request, 'profile_upload.html')
