
from django.contrib.admin.templatetags.admin_list import results
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
from django.db.models import Q


import numpy as np
from sklearn.preprocessing import StandardScaler
from matplotlib import pyplot as plt

# Hàm view cho trang chủ
def index(request):
    return render(request, 'dashboard/index.html')


# Hàm view cho việc add_data quốc gia và dân số
def add_data(request):
    global data_for_chart, form
    # if 'q' in request.GET:
    #     q = request.GET['q']
    #     multiple_q = Q(Q(country__icontains=q) | Q(population__icontains=q))
    #     data = Add_Data.objects.filter(multiple_q)
    # else:

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


def predict_data(request, *args, **kwargs):
    context = {}
    if request.method == 'POST':
        uploaded_file = request.FILES['document']
        CountryName = request.POST.get('attribute1')
        predictYear = request.POST.get('attribute2')
        if uploaded_file.name.endswith('csv'):
            savefile = FileSystemStorage()
            name = savefile.save(uploaded_file.name, uploaded_file)
            file_directory = os.path.join(settings.MEDIA_ROOT, name)

            readPredict(file_directory)
            extract_data(CountryName)

            #scaling data
            scaler_X = StandardScaler()
            scaler_y = StandardScaler()

            X_scaled = scaler_X.fit_transform(X)
            y_scaled = scaler_y.fit_transform(y)

            #setup and train model
            lin_model = LinearRegressionCustom(iterations=1000, learning_rate=0.01)
            lin_model.fit(X_scaled, y_scaled)

            # get scaling Predictions
            train_predictions_scaled = lin_model.predict(X_scaled)

            #back to original scale
            train_predictions = scaler_y.inverse_transform(train_predictions_scaled)

            # Plotting
            plt.scatter(X, y, color='black', label='Actual data')
            plt.plot(X, train_predictions, color='blue', linewidth=3, label='Regression line')
            plt.xlabel('X-axis label')
            plt.ylabel('Y-axis label')
            plt.legend()
            plt.show()

            # Scale the new input feature
            scaled_new_year = scaler_X.transform([[predictYear]])

            # Predict the scaled output
            scaled_prediction = lin_model.predict(scaled_new_year)

            # Inverse transform to get the prediction in the original scale
            predicted_population = scaler_y.inverse_transform(scaled_prediction)

            print(f"Predicted population for the year {predictYear}: {predicted_population[0, 0]}")

    return render(request, "dashboard/predict_data.html", {})

# Hàm đọc dữ liệu từ tệp CSV và lưu vào biến toàn cục `data`
def readfile(filename):
    global data
    my_file = pd.read_csv(filename, sep='[:;,|_]', engine='python', header=0)
    data = pd.DataFrame(data=my_file, index=None)
    print(data)

def readPredict(filename):
    global df
    df = pd.read_csv(filename)

def extract_data(CountryName):
    global train_data, X, y
    populations = df.loc[df['Country Name'] == CountryName, '2014':'2022'].values.flatten()
    years = df.loc[df['Country Name'] == CountryName, '2014':'2022'].columns.tolist()
    train_data = {
        "Population": populations,
        "Year": years
    }
    train_data = pd.DataFrame(train_data)
    print(train_data)
    train_data['Year'] = pd.to_numeric(train_data['Year'], errors='coerce')
    X = train_data['Year'].values.reshape(-1, 1)
    y = train_data['Population'].values.reshape(-1, 1)

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

def processingUpload(request):
    # if request.method == 'POST':
    #     form = sortingForm(request.POST)
    #
    #     if form.is_valid():
    #         algorithm = request.POST['algorithm']

            data = Upload_File.objects.values('attribute2').values_list('attribute2','attribute1')
            listlabels, listdatas = processSort(data)
            return render(request, 'dashboard/uploadFile_algorithms.html', {'listlabels':listlabels, 'listdatas':listdatas})



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

    data_sorted = quicksort(data_List, 0, len(data_List) - 1)

    Sorted_dict = {i: data_Dict[i] for i in data_sorted}

    attr1 = []
    attr2 = []
    for i in Sorted_dict:
        attr1.append(Sorted_dict[i])
        attr2.append(i)

    listlabels, listdatas = prepare_chart_data(attr1, attr2)

    return listlabels, listdatas

class LinearRegressionCustom():
    def __init__(self, learning_rate, iterations):
        self.learning_rate = learning_rate
        self.iterations = iterations

    # Function for model training
    def fit(self, X, Y):
        # no_of_training_examples, no_of_features
        self.m, self.n = X.shape

        # weight initialization
        self.W = np.zeros(self.n)
        self.b = 0
        self.X = X
        self.Y = Y
        # print(X.shape)
        # print(Y.shape)
        # gradient descent learning
        for i in range(self.iterations):
            self.update_weights()

        return self

    # Helper function to update weights in gradient descent
    def update_weights(self):
        Y_pred = self.predict(self.X)

        # calculate gradients
        dW = - (2 * (self.X.T).dot(self.Y - Y_pred)) / self.m
        db = - 2 * np.sum(self.Y - Y_pred) / self.m
        # print(dW.shape)
        # update weights
        self.W = self.W - self.learning_rate * dW
        self.b = self.b - self.learning_rate * db

        return self

    # Hypothetical function h(x)
    def predict(self, X):
        return X.dot(self.W) + self.b


