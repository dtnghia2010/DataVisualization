
from django.contrib.admin.templatetags.admin_list import results
from django.core.checks import messages
from django.shortcuts import render, redirect
from django.template import context
from tablib import Dataset
from .models import Add_Data, Upload_File
from .forms import Add_DataFrom, Upload_FileForm
import os
from collections import Counter
from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
from django.contrib import messages
import pandas as pd
from django.conf import settings
from django.core.files.storage import FileSystemStorage


# Hàm view cho trang chủ
def index(request):
    return render(request, 'dashboard/index.html')


# Hàm view cho việc add_data quốc gia và dân số
def add_data(request):
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


# Hàm view cho việc tải lên tệp CSV và lưu trữ dữ liệu vào database

def upload_file(request, *args, **kwargs):
    global attribute1, attribute2
    context = {}
    listlabels, listdatas = None, None

    Upload_File.objects.all().delete()

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


# Hàm đọc dữ liệu từ tệp CSV và lưu vào biến toàn cục `data`
def readfile(filename):
    global data
    my_file = pd.read_csv(filename, sep='[:;,|_]', engine='python', header=0)
    data = pd.DataFrame(data=my_file, index=None)
    print(data)




# Hàm xử lý dữ liệu từ DataFrame và trả về danh sách nhãn và dữ liệu

def process_data(attribute1, attribute2):
    labels = []
    datas = []
    for x in data[attribute1]:  # name
        labels.append(x)

    for y in data[attribute2]:  # price
        datas.append(y)

    return labels, datas




def prepare_chart_data(labels, datas):
    # Chuyển danh sách về danh sách Python thông thường
    listlabels = labels
    listdatas = datas

    return listlabels, listdatas




# Trong views.py
# Trong views.py
def partition(arr, low, high, attribute_index):
    i = low - 1
    pivot = arr[high][attribute_index]

    for j in range(low, high):
        if arr[j][attribute_index] <= pivot:
            i = i + 1
            arr[i], arr[j] = arr[j], arr[i]

    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1

def quicksort(arr, low, high, attribute_index):
    if low < high:
        pi = partition(arr, low, high, attribute_index)
        quicksort(arr, low, pi - 1, attribute_index)
        quicksort(arr, pi + 1, high, attribute_index)

def upload_sort(request):
    # Lấy dữ liệu từ database
    data_upload_file = Upload_File.objects.all()

    # Chuyển dữ liệu thành danh sách để sử dụng trong thuật toán quicksort
    data_list = [(item.attribute2, item.attribute1) for item in data_upload_file]

    # Kiểm tra xem data_list có giữ nguyên dữ liệu hay không
    if data_list:
        # Thực hiện Quick Sort
        quicksort(data_list, 0, len(data_list) - 1, attribute_index=0)

        # Chuẩn bị dữ liệu cho biểu đồ
        labels, datas = zip(*data_list)

        # In ra giá trị của labels và datas
        print("Labels:", labels)
        print("Datas:", datas)
    else:
        # Xử lý trường hợp khi data_list rỗng
        labels, datas = [], []

    # Render template với dữ liệu đã sắp xếp
    return render(request, "dashboard/upload_sort.html", {'listlabels': labels, 'listdatas': datas})


# def upload_file(request, *args, **kwargs):
#     global attribute1, attribute2
#     context = {}
#     listlabels, listdatas = None, None
#
#     if request.method == 'POST':
#         uploaded_file = request.FILES['document']
#         attribute1 = request.POST.get('attribute1')
#         attribute2 = request.POST.get('attribute2')
#
#         if uploaded_file.name.endswith('csv'):
#             savefile = FileSystemStorage()
#             name = savefile.save(uploaded_file.name, uploaded_file)
#
#             file_directory = os.path.join(settings.MEDIA_ROOT, name)
#             readfile(file_directory)
#
#             labels, datas = process_data(attribute1, attribute2)
#             listlabels, listdatas = prepare_chart_data(labels, datas)
#
#         else:
#             messages.warning(request, 'File was not uploaded, please use a CSV file extension')
#
#     return render(request, "dashboard/upload_file.html", {'listlabels': listlabels, 'listdatas': listdatas})


#     form = UploadFileForm(request.POST, request.FILES)
#     if form.is_valid():
#         uploaded_file = form.save(commit=False)
#
#         # Đọc dữ liệu từ file CSV
#         csv_data = read_csv(uploaded_file.file.path)
#
#         # Lưu trữ dữ liệu vào cơ sở dữ liệu
#         for row in csv_data:
#             # Tạo một bản ghi mới cho mỗi dòng trong CSV
#             new_record = CountryData(attribute1=uploaded_file.attribute1, attribute2=uploaded_file.attribute2, country=row[0], population=row[1])
#             new_record.save()
#
#         uploaded_file.save()
#
#         return redirect('upload_file')
# else:
#     form = UploadFileForm()
#
# uploaded_files = UploadedFile.objects.all()

# return render(request, 'dashboard/upload_file.html')

# from django.shortcuts import render, redirect
# from .models import UploadedFile
# from .forms import UploadFileForm
#
# def upload_file(request):
#     if request.method == 'POST':
#         form = UploadFileForm(request.POST, request.FILES)
#         if form.is_valid():
#             uploaded_file = form.save(commit=False)
#             uploaded_file.save()
#
#             # Cập nhật biểu đồ ở đây (sử dụng uploaded_file)
#
#             return redirect('upload_file')  # Hoặc chuyển hướng đến trang khác nếu cần
#     else:
#         form = UploadFileForm()
#
#     uploaded_files = UploadedFile.objects.all()
#
#     return render(request, 'dashboard/upload_file.html', {'form': form, 'uploaded_files': uploaded_files})
#
