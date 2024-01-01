from django.core.checks import messages
from .forms import Add_DataFrom, sortingForm, DeleteForm_AddData
from django.shortcuts import render, redirect
from django.contrib import messages
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from .util import binary_search_range, quicksort, LinearRegressionCustom, readPredict, extract_data, generatePlot, \
    partition
from .models import Upload_File
from django.http import HttpResponse
from .models import Add_Data
from sklearn.preprocessing import StandardScaler

import os
import pandas as pd
import numpy as np
import matplotlib

matplotlib.use('agg')


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
            country = form.cleaned_data.get('country')

            if Add_Data.objects.filter(country=country).exists():
                messages.error(request, "Data for this country already exists. Please enter different data.")
            else:
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
    data_for_chart = Add_Data.objects.all()
    return render(request, 'dashboard/addData_algorithms.html', {'data': data_for_chart, 'form': form})


def delete_add_data(request):
    if request.method == 'POST':
        form = DeleteForm_AddData(request.POST)
        if form.is_valid():
            items_to_delete = form.cleaned_data['items_to_delete']
            items_to_delete.delete()  # Delete selected items

            # Redirect or perform any additional actions

            data_for_chart = Add_Data.objects.all()
            return render(request, 'dashboard/addData_algorithms.html',
                          {'data': data_for_chart, 'form': form})  # Redirect to success page
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

            # Check if attribute1 and attribute2 are valid
            if attribute1 not in data.columns or attribute2 not in data.columns:
                messages.warning(request, 'Please enter valid Attribute 1 and Attribute 2 present in the CSV file.')
                return render(request, "dashboard/upload_file.html")

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


def predict_data(request, *args, **kwargs):
    context = {}
    if request.method == 'POST':
        if request.method == 'POST':
            uploaded_file = request.FILES['document']
            if uploaded_file.name.endswith('csv'):
                uploaded_file = request.FILES['document']
                CountryName = request.POST.get('attribute1')
                fromYear = request.POST.get('from')
                toYear = request.POST.get('to')
                prediction = request.POST.get('prediction')
                if uploaded_file.name.endswith('csv'):
                    savefile = FileSystemStorage()
                    name = savefile.save(uploaded_file.name, uploaded_file)
                    file_directory = os.path.join(settings.MEDIA_ROOT, name)
                    df = readPredict(file_directory)

                    if fromYear not in df.columns or toYear not in df.columns:
                        messages.warning(request, '"From" or "To" was not found in the csv file\n')
                        return render(request, "dashboard/predict_data.html", context)
                    #check if CountryName present in the csv file
                    is_country_present = any(df[col].eq(CountryName).any() for col in df.columns)
                    if not is_country_present:
                        messages.warning(request, f'"{CountryName}" was not found in the csv file\n')
                        return render(request, "dashboard/predict_data.html", context)

                    # Check if 'Country Name' is a valid column in the DataFrame

                    result = extract_data(CountryName, fromYear, toYear)
                    X = result['X']
                    y = result['y']
                    # scaling data
                    scaler_X = StandardScaler()
                    scaler_y = StandardScaler()
                    X_scaled = scaler_X.fit_transform(X)
                    y_scaled = scaler_y.fit_transform(y)
                    # setup and train model
                    lin_model = LinearRegressionCustom(iterations=1000, learning_rate=0.01)
                    lin_model.fit(X_scaled, y_scaled)
                    # get scaling Predictions
                    train_predictions_scaled = lin_model.predict(X_scaled)
                    # back to original scale
                    train_predictions = scaler_y.inverse_transform(train_predictions_scaled)
                    # Scale the new input feature
                    scaled_new_year = scaler_X.transform([[prediction]])
                    # Predict the scaled output
                    scaled_prediction = lin_model.predict(scaled_new_year)
                    # Inverse transform to get the prediction in the original scale
                    predicted_population = scaler_y.inverse_transform(scaled_prediction)
                    print(f"Predicted population for the year {prediction}: {predicted_population[0, 0]}")
                    context['predicted_population'] = np.round(predicted_population[0, 0])
                    plot_filename = generatePlot(X, y, train_predictions)
                    context['plot_filename'] = 'plot.png'
                else:
                    context['plot_filename'] = None
            else:
                messages.warning(request, 'File was not uploaded, please use a CSV file extension\n')

    return render(request, "dashboard/predict_data.html", context)


# Hàm đọc dữ liệu từ tệp CSV và lưu vào biến toàn cục `data`
def readfile(filename):
    global data
    my_file = pd.read_csv(filename, sep='[:;,|_]', engine='python', header=0)
    data = pd.DataFrame(data=my_file, index=None)
    print(data)


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

        quicksort_(array, pi + 1, high)

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


def search_page_upload(request):
    # Initialize error_message with the default message
    error_message = "Please enter a value for 'a' less than 'b.'"
    no_values_found = False  # Initialize the variable

    if request.method == 'POST':
        try:
            # Lấy giá trị của 'value_a' và 'value_b' từ form
            value_a = int(request.POST.get('value_a'))
            value_b = int(request.POST.get('value_b'))

            # Kiểm tra nếu giá trị a lớn hơn hoặc bằng giá trị b
            if value_a >= value_b:
                return render(request, 'dashboard/search_page_upload.html',
                              {'error_message': error_message, 'value_a': value_a, 'value_b': value_b})

            # Truy vấn và sắp xếp dữ liệu từ cơ sở dữ liệu
            data_list = list(Upload_File.objects.values('attribute1', 'attribute2').order_by('attribute2'))

            # Sử dụng quicksort để sắp xếp data_list dựa trên 'attribute2'
            quicksort(data_list, 0, len(data_list) - 1, attribute_index='attribute2')

            # Tìm kiếm nhị phân giá trị trong khoảng xác định
            start_index = binary_search_range(data_list, 0, len(data_list) - 1, value_a, value_b,
                                              attribute_index='attribute2')

            if start_index == -1:
                no_values_found = True  # Set the variable to True
                return render(request, "dashboard/search_page_upload.html",
                              {'no_values_found': no_values_found, 'error_message': error_message, 'value_a': value_a,
                               'value_b': value_b})

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
            return render(request, "dashboard/search_page_upload.html",
                          {'listlabels': labels, 'listdatas': datas, 'selected_data': selected_data,
                           'error_message': error_message, 'value_a': value_a, 'value_b': value_b})

        except (ValueError, TypeError) as e:
            # Xử lý giá trị nhập không hợp lệ
            return HttpResponse(f"Lỗi: {e}")

    # Render form khi request là GET
    return render(request, 'dashboard/search_page_upload.html', {'error_message': error_message})


def search_add_data(request):
    if request.method == 'POST':
        try:
            # Lấy giá trị từ form
            value_a = int(request.POST.get('value_a'))
            value_b = int(request.POST.get('value_b'))

            if value_a > value_b:
                return render(request, "dashboard/search_add_data.html",
                              {'error_message': "Please enter a value for 'a' less than 'b'", 'show_chart': False})

            # Truy vấn và sắp xếp dữ liệu từ model Add_Data
            data_list = list(Add_Data.objects.values('country', 'population').order_by('population'))

            # Sử dụng quicksort để sắp xếp data_list dựa trên 'population'
            quicksort(data_list, 0, len(data_list) - 1, attribute_index='population')

            # Tìm kiếm nhị phân giá trị trong khoảng xác định
            start_index = binary_search_range(data_list, 0, len(data_list) - 1, value_a, value_b,
                                              attribute_index='population')

            if start_index == -1:
                no_values_message = f"No values found in the range from {value_a} to {value_b}."
                return render(request, "dashboard/search_add_data.html",
                              {'error_message': None, 'show_chart': False, 'no_values_message': no_values_message})

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
            return render(request, "dashboard/search_add_data.html",
                          {'listlabels': labels, 'listdatas': datas, 'selected_data': selected_data,
                           'show_chart': True})

        except (ValueError, TypeError) as e:
            # Xử lý khi giá trị nhập không hợp lệ
            return render(request, "dashboard/search_add_data.html",
                          {'error_message': f"Lỗi: {e}", 'show_chart': False})

    # Render form khi request là GET
    return render(request, 'dashboard/search_add_data.html', {'show_chart': False})


def processingUpload(request):
    data = Upload_File.objects.values('attribute2').values_list('attribute2', 'attribute1')
    listlabels, listdatas = processSort(data)
    return render(request, 'dashboard/upload_sort.html', {'listlabels': listlabels, 'listdatas': listdatas})


def processingAdd(request):
    data = Add_Data.objects.values('population').values_list('population', 'country')
    listlabels, listdatas = processSort(data)
    return render(request, 'dashboard/addData_sort.html', {'listlabels': listlabels, 'listdatas': listdatas})


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
