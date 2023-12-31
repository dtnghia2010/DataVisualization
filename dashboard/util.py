# Trong utils.py
import os

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from datavisual import settings


def generatePlot(X, y, train_predictions):
    plt.clf()
    plt.style.use("fivethirtyeight")
    plt.scatter(X, y, color='black', label='Actual data')
    plt.plot(X, train_predictions, color='blue', linewidth=3, label='Regression line')
    print( np.round(train_predictions.ravel()))
    plot_filename = os.path.join(settings.PLOT_ROOT, 'plot.png')
    plt.savefig(plot_filename)
    return plot_filename
def readPredict(filename):
    global df
    df = pd.read_csv(filename)
    return df

def extract_data(CountryName, fromYear, toYear):
    global train_data, X, y
    populations = df.loc[df['Country Name'] == CountryName, fromYear:toYear].values.flatten()
    years = df.loc[df['Country Name'] == CountryName, fromYear:toYear].columns.tolist()
    train_data = {
        "Population": populations,
        "Year": years
    }
    train_data = pd.DataFrame(train_data)
    print(train_data)
    train_data['Year'] = pd.to_numeric(train_data['Year'], errors='coerce')
    X = train_data['Year'].values.reshape(-1, 1)
    y = train_data['Population'].values.reshape(-1, 1)
    result = {
        'X': X,
        'y': y,
    }
    return result

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



def binary_search_range(arr, low, high, target_low, target_high, attribute_index):
    while low <= high:
        mid = (low + high) // 2
        mid_value = arr[mid][attribute_index]
        print(f"Checking mid_value={mid_value} at index={mid}")
        if target_low <= mid_value <= target_high:
            print("Found within the range.")
            return mid
        elif mid_value < target_low:
            print("Moving to the right.")
            low = mid + 1
        else:
            print("Moving to the left.")
            high = mid - 1
    print("Value not found in the specified range.")
    return -1


# Hàm sắp xếp nhanh (quicksort) cho mảng dựa trên một thuộc tính cụ thể.
def quicksort(arr, low, high, attribute_index):
    if low < high:
        # Chia mảng thành các phần nhỏ và lấy chỉ số pivot.
        pi = partition(arr, low, high, attribute_index)

        # Đệ quy sắp xếp các phần nhỏ bên trái và bên phải của pivot.
        quicksort(arr, low, pi - 1, attribute_index)
        quicksort(arr, pi + 1, high, attribute_index)


# Hàm phân hoạch mảng trong quicksort để có thứ tự đúng và trả về chỉ số của pivot.
def partition(arr, low, high, attribute_index):
    i = low - 1
    pivot = arr[high][attribute_index]

    for j in range(low, high):
        if arr[j][attribute_index] <= pivot:
            i = i + 1
            # Hoán đổi vị trí giữa các phần tử để có thứ tự đúng.
            arr[i], arr[j] = arr[j], arr[i]

    # Đưa pivot về đúng vị trí và trả về chỉ số của pivot.
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1