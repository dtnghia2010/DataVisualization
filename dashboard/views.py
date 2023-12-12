# views.py

import os
from collections import Counter

import pandas as pd
from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
from django.contrib import messages
from django.conf import settings
from .models import Add_Data, Upload_File
from .forms import Add_DataFrom, Upload_FileForm


def index(request):
    # Hàm view cho trang chủ
    return render(request, 'dashboard/index.html')


def add_data(request):
    # Hàm view cho việc thêm dữ liệu quốc gia và dân số
    data = Add_Data.objects.all()

    if request.method == 'POST':
        form = Add_DataFrom(request.POST)
        if form.is_valid():
            new_data = form.save()
            new_data.refresh_from_db()

            # Thực hiện các bước vẽ biểu đồ với dữ liệu mới
            data_for_chart = Add_Data.objects.all()

            # Truyền dữ liệu biểu đồ vào context để sử dụng trong template
            context = {
                'data': data_for_chart,
                'form': form,
            }
            # Render template với context đã cập nhật
            return render(request, 'dashboard/add_data.html', context)
    else:
        form = Add_DataFrom()

    context = {
        'data': data,
        'form': form,
    }

    return render(request, 'dashboard/add_data.html', context)


def upload_file(request, *args, **kwargs):
    # Hàm view cho việc tải lên tệp CSV và lưu trữ dữ liệu vào database
    global attribute1, attribute2
    context = {}
    listlabels, listdatas = None, None

    if request.method == 'POST':
        uploaded_file = request.FILES['document']
        attribute1 = request.POST.get('attribute1')
        attribute2 = request.POST.get('attribute2')

        if uploaded_file.name.endswith('csv'):
            savefile = FileSystemStorage()
            name = savefile.save(uploaded_file.name, uploaded_file)

            file_directory = os.path.join(settings.MEDIA_ROOT, name)
            readfile(file_directory)

            # Lặp qua dữ liệu và tạo hoặc cập nhật bản ghi trong mô hình
            for index, row in data.iterrows():
                Upload_File.objects.create(
                    attribute1=row[attribute1],
                    attribute2=row[attribute2]
                )

            labels, datas = process_data(attribute1, attribute2)
            listlabels, listdatas = prepare_chart_data(labels, datas)

        else:
            messages.warning(request, 'File was not uploaded, please use a CSV file extension')

    return render(request, "dashboard/upload_file.html", {'listlabels': listlabels, 'listdatas': listdatas})


def readfile(filename):
    # Hàm đọc dữ liệu từ tệp CSV và lưu vào biến toàn cục `data`
    global data
    my_file = pd.read_csv(filename, sep='[:;,|_]', engine='python')
    data = pd.DataFrame(data=my_file, index=None)


def process_data(attribute1, attribute2):
    # Hàm xử lý dữ liệu từ DataFrame và trả về danh sách nhãn và dữ liệu
    labels = []
    datas = []
    for x in data[attribute1]:  # name
        labels.append(x)
