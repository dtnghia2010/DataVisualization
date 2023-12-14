from django.http import HttpResponse
from django.core.checks import messages

from .models import Add_Data, Upload_File
from .forms import Add_DataFrom, sortingForm
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
def upload_file(request):
    global attribute1, attribute2

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
    my_file = pd.read_csv(filename, sep='[:;,|_]', engine='python')
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
    # Tạo một từ điển đếm số lần xuất hiện của mỗi nhãn
    my_labels = dict(Counter(labels))
    # Tạo một từ điển đếm số lần xuất hiện của mỗi dữ liệu
    my_datas = dict(Counter(datas))
    # Chuyển từ điển nhãn và dữ liệu thành danh sách không trùng lặp
    listlabels = list(my_labels.keys())
    listdatas = list(my_datas.keys())
    return listlabels, listdatas

def quicksort(array, low, high):
    array_len = len(array)

    if low < high:
        pi = partition(array, low, high)
        quicksort(array, low, pi - 1)

        quicksort(array, pi +1, high)

    return array


def partition(array, low, high):
    # choose the rightmost element as pivot
    pivot = array[high]

    # pointer for greater element
    i = low - 1

    # traverse through all elements
    # compare each element with pivot
    for j in range(low, high):
        if array[j] <= pivot:
            # If element smaller than pivot is found
            # swap it with the greater element pointed by i
            i = i + 1

            # Swapping element at i with element at j
            (array[i], array[j]) = (array[j], array[i])

    # Swap the pivot element with the greater element specified by i
    (array[i + 1], array[high]) = (array[high], array[i + 1])

    # Return the position from where partition is done
    return i + 1

def processing(request):
    if request.method == 'POST':
        form = sortingForm(request.POST)

        if form.is_valid():
            algorithm = request.POST['algorithm']

            data = Upload_File.objects.values('attribute2').values_list('attribute2','attribute1')

            data_Dict = dict(data)

            print(data_Dict)

            data_List = list(data_Dict.keys())

            data_sorted = globals()[algorithm](data_List, 0, len(data_List) - 1)

            Sorted_dict = {i: data_Dict[i] for i in data_sorted}

            attr1 = []
            attr2 = []
            for i in Sorted_dict:
                attr1.append(Sorted_dict[i])
                attr2.append(i)

            listlabels, listdatas = prepare_chart_data(attr1, attr2)

            return render(request, 'dashboard/Sorting.html', {'listlabels': listlabels, 'listdatas': listdatas})

            # z = globals()[algorithm](data, 0, len(data) - 1)
        else:
            return HttpResponse("form is not valid")
    else:
        return HttpResponse("It not POST method")