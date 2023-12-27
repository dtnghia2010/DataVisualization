
from django.contrib.admin.templatetags.admin_list import results
from django.core.checks import messages

from .models import Add_Data, Upload_File
from .forms import Add_DataFrom, sortingForm, DeleteForm_AddData
import os
from collections import Counter
from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
from django.contrib import messages
import pandas as pd
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.db.models.functions import Cast
from django.shortcuts import render
from django.http import HttpResponse
from .models import Upload_File
from .util import binary_search_range, quicksort


# Hàm view cho trang chủ
def index(request):
    return render(request, 'dashboard/index.html')


# Hàm view cho việc add_data quốc gia và dân số
def add_data(request):
    global data_for_chart, form


    data = Add_Data.objects.all()
    formSort = sortingForm()

    if request.method == 'POST':
        form = Add_DataFrom(request.POST)
        if form.is_valid():
            new_data = form.save()
            new_data.refresh_from_db()

            # Thực hiện các bước vẽ biểu đồ với dữ liệu mới
            data_for_chart = Add_Data.objects.all()
            return redirect(addData_algorithms)
    else:
        form = Add_DataFrom()

    context = {
        'data': data,
        'form': form,
        'formSorting': sortingForm,
    }

    return render(request, 'dashboard/add_data.html', context)


def addData_algorithms(request):
    return render(request, 'dashboard/addData_algorithms.html', {'data': data_for_chart, 'form': form})


def delete_add_data(request):
    if request.method == 'POST':
        form = DeleteForm_AddData(request.POST)
        if form.is_valid():
            items_to_delete = form.cleaned_data['items_to_delete']
            items_to_delete.delete()  # Delete selected items

            # Redirect or perform any additional actions

            data_for_chart = Add_Data.objects.all()
            return render(request, 'dashboard/addData_algorithms.html', {'data': data_for_chart, 'form': form})  # Redirect to success page
    else:
        form = DeleteForm_AddData()

    context = {
        'form': form,
    }
    return render(request, 'dashboard/delete.html', context)


# Hàm view cho việc tải lên tệp CSV và lưu trữ dữ liệu vào database
def upload_file(request):
    global attribute1, attribute2

    listlabels, listdatas = None, None
    formSorting = sortingForm()
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
            return redirect(uploadFile_algorithms)
        else:
            messages.warning(request, 'File was not uploaded, please use a CSV file extension')
    return render(request, "dashboard/upload_file.html")


def uploadFile_algorithms(request):
    for index, row in data.iterrows():
        Upload_File.objects.create(
            attribute1=row[attribute1],
            attribute2=row[attribute2]
        )

    labels, datas = process_data(attribute1, attribute2)
    listlabels, listdatas = prepare_chart_data(labels, datas)
    return render(request, 'dashboard/uploadFile_algorithms.html', {'listlabels': listlabels, 'listdatas': listdatas})


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



def quicksort_(array, low, high):
    array_len = len(array)

    if low < high:
        pi = partition_(array, low, high)
        quicksort_(array, low, pi - 1)

        quicksort_(array, pi +1, high)

    return array


def partition_(array, low, high):
    # choose the rightmost element as pivot
    pivot = array[high]

    # pointer for greater element
    i = low - 1
    pivot = array[high]

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




# def upload_sort(request):
#     # Lấy dữ liệu từ database
#     data_upload_file = Upload_File.objects.all()
#
#     # Chuyển dữ liệu thành danh sách để sử dụng trong thuật toán quicksort
#     data_list = [(item.attribute2, item.attribute1) for item in data_upload_file]
#
#     # Kiểm tra xem data_list có giữ nguyên dữ liệu hay không
#     if data_list:
#         # Thực hiện Quick Sort
#         quicksort(data_list, 0, len(data_list) - 1, attribute_index=0)
#
#         # Chuẩn bị dữ liệu cho biểu đồ
#         labels, datas = zip(*data_list)
#
#         # In ra giá trị của labels và datas
#         print("Labels:", labels)
#         print("Datas:", datas)
#     else:
#         # Xử lý trường hợp khi data_list rỗng
#         labels, datas = [], []
#
#     # Render template với dữ liệu đã sắp xếp
#     return render(request, "dashboard/upload_sort.html", {'listlabels': labels, 'listdatas': datas})
#



import pandas as pd
from .models import Upload_File
from .views import  prepare_chart_data
from . util import quicksort, partition
def search_page_upload(request):
    if request.method == 'POST':
        try:
            # Lấy giá trị của 'value_a' và 'value_b' từ form
            value_a = int(request.POST.get('value_a'))
            value_b = int(request.POST.get('value_b'))

            # Truy vấn và sắp xếp dữ liệu từ cơ sở dữ liệu
            data_list = list(Upload_File.objects.values('attribute1', 'attribute2').order_by('attribute2'))

            # Sử dụng quicksort để sắp xếp data_list dựa trên 'attribute2'
            quicksort(data_list, 0, len(data_list) - 1, attribute_index='attribute2')

            # Tìm kiếm nhị phân giá trị trong khoảng xác định
            start_index = binary_search_range(data_list, 0, len(data_list) - 1, value_a, value_b, attribute_index='attribute2')

            if start_index == -1:
                return HttpResponse("Không tìm thấy giá trị trong khoảng xác định.")

            end_index = start_index
            selected_data = []

            # Thu thập dữ liệu trong khoảng xác định vào danh sách selected_data
            while end_index < len(data_list) and data_list[end_index]['attribute2'] <= value_b:
                selected_data.append(data_list[end_index])
                end_index += 1

            # Chuẩn bị dữ liệu cho biểu đồ
            labels = [item['attribute1'] for item in selected_data]
            datas = [item['attribute2'] for item in selected_data]

            # In attribute1 và attribute2 cho từng item trong selected_data ra terminal
            for item in selected_data:
                print(f"Attribute1: {item['attribute1']}, Attribute2: {item['attribute2']}")

            # Render HTML response với dữ liệu đã chọn
            return render(request, "dashboard/search_page_upload.html", {'listlabels': labels, 'listdatas': datas, 'selected_data': selected_data})

        except (ValueError, TypeError) as e:
            # Xử lý giá trị nhập không hợp lệ
            return HttpResponse(f"Lỗi: {e}")

    # Render form khi request là GET
    return render(request, 'dashboard/search_page_upload.html')






from django.shortcuts import render
from django.http import HttpResponse
from .models import Add_Data
from .util import binary_search_range, quicksort
def search_add_data(request):
    if request.method == 'POST':
        try:
            # Lấy giá trị từ form
            value_a = int(request.POST.get('value_a'))
            value_b = int(request.POST.get('value_b'))

            # Truy vấn và sắp xếp dữ liệu từ model Add_Data
            data_list = list(Add_Data.objects.values('country', 'population').order_by('population'))

            # Sử dụng quicksort để sắp xếp data_list dựa trên 'population'
            quicksort(data_list, 0, len(data_list) - 1, attribute_index='population')

            # Tìm kiếm nhị phân giá trị trong khoảng xác định
            start_index = binary_search_range(data_list, 0, len(data_list) - 1, value_a, value_b, attribute_index='population')

            if start_index == -1:
                return HttpResponse("Không có giá trị nằm trong khoảng xác định.")

            end_index = start_index
            selected_data = []

            # Thu thập dữ liệu trong khoảng xác định vào danh sách selected_data
            while end_index < len(data_list) and data_list[end_index]['population'] <= value_b:
                selected_data.append(data_list[end_index])
                end_index += 1

            # Điều chỉnh start_index để bao gồm tất cả các phần tử trong khoảng xác định
            while start_index > 0 and data_list[start_index - 1]['population'] >= value_a:
                start_index -= 1
                selected_data.insert(0, data_list[start_index])

            # In country và population cho từng phần tử trong selected_data ra terminal
            for item in selected_data:
                print(f"Country: {item['country']}, Population: {item['population']}")

            # Chuẩn bị dữ liệu cho biểu đồ
            labels = [item['country'] for item in selected_data]
            datas = [item['population'] for item in selected_data]

            # Render HTML response với dữ liệu đã chọn
            return render(request, "dashboard/search_add_data.html", {'listlabels': labels, 'listdatas': datas, 'selected_data': selected_data})

        except (ValueError, TypeError) as e:
            # Xử lý khi giá trị nhập không hợp lệ
            return HttpResponse(f"Lỗi: {e}")

    # Render form khi request là GET
    return render(request, 'dashboard/search_add_data.html')


def processingUpload(request):
    # if request.method == 'POST':
    #     form = sortingForm(request.POST)
    #
    #     if form.is_valid():
    #         algorithm = request.POST['algorithm']

            data = Upload_File.objects.values('attribute2').values_list('attribute2','attribute1')
            listlabels, listdatas = processSort(data)
            return render(request, 'dashboard/uploadFile_algorithms.html', {'listlabels':listlabels, 'listdatas':listdatas})




#
# from django.shortcuts import render
# from .models import Upload_File
# from .views import quicksort, partition, prepare_chart_data
#
# def upload_sort_and_print(request):
#     # Lấy dữ liệu từ database
#     data_upload_file = Upload_File.objects.all()
#
#     # Chuyển dữ liệu thành danh sách để sử dụng trong thuật toán quicksort
#     data_list = [(item.attribute2, item.attribute1) for item in data_upload_file]
#
#     # Kiểm tra xem data_list có giữ nguyên dữ liệu hay không
#     if data_list:
#         # Thực hiện Quick Sort
#         quicksort(data_list, 0, len(data_list) - 1, attribute_index=0)
#
#         # In ra giá trị của attribute1 và attribute2
#         print("Danh sách đã sắp xếp:")
#         for item in data_list:
#             print(f"Attribute1: {item[0]}, Attribute2: {item[1]}")
#
#         # Chuẩn bị dữ liệu cho biểu đồ (nếu cần)
#         labels, datas = prepare_chart_data(*zip(*data_list))
#
#         # Trả về danh sách đã sắp xếp để sử dụng cho binary search
#         return data_list
#     else:
#         # Xử lý trường hợp khi data_list rỗng
#         print("Dữ liệu rỗng.")
#         return []
# sorted_data_list = upload_sort_and_print(request)









# Import necessary libraries and modules

# def search_page_upload(request):
#     if request.method == 'POST':
#         try:
#             value_a = float(request.POST.get('value_a'))
#             value_b = float(request.POST.get('value_b'))
#
#             # Retrieve and sort data from the database
#             data_upload_file = Upload_File.objects.all()
#             data_list = [(item.attribute2, item.attribute1) for item in data_upload_file]
#             quicksort(data_list, 0, len(data_list) - 1, attribute_index=0)
#
#             # Binary search for values within the specified range
#             start_index = binary_search_range(data_list, 0, len(data_list) - 1, value_a, value_b, attribute_index=0)
#
#             if start_index == -1:
#                 return HttpResponse("No values found in the specified range.")
#
#             end_index = start_index
#             while end_index < len(data_list) and data_list[end_index][0] <= value_b:
#                 end_index += 1
#
#             # Prepare data for chart
#             labels, datas = prepare_chart_data(*zip(*data_list[start_index:end_index]))
#
#             return render(request, "dashboard/search_page_upload.html", {'listlabels': labels, 'listdatas': datas})
#
#         except (ValueError, TypeError) as e:
#             # Handle invalid input values
#             return HttpResponse(f"Error: {e}")
#
#     return render(request, 'dashboard/search_page_upload.html')


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


def processingAdd(request):
    # if request.method == 'POST':
    #     form = sortingForm(request.POST)

        # if form.is_valid():
        #     algorithm = request.POST['algorithm']

            data = Add_Data.objects.values('population').values_list('population','country')
            listlabels, listdatas = processSort(data)
            return render(request, 'dashboard/upload_sort.html', {'listlabels':listlabels, 'listdatas':listdatas})

def processSort(data):
    data_Dict = dict(data)

    print(data_Dict)

    data_List = list(data_Dict.keys())

    data_sorted = quicksort_(data_List, 0, len(data_List) - 1)

    Sorted_dict = {i: data_Dict[i] for i in data_sorted}

    attr1 = []
    attr2 = []
    for i in Sorted_dict:
        attr1.append(Sorted_dict[i])
        attr2.append(i)

    listlabels, listdatas = prepare_chart_data(attr1, attr2)

    return listlabels, listdatas

