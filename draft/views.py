from django.core.files.storage import FileSystemStorage
from django.shortcuts import render, redirect
import os
from django.contrib import messages
import pandas as pd
from collections import Counter


def home_view(request, *args, **kwargs):
    # global attributeid1, attributeid2
    context={}
    if request.method == 'POST':
        uploaded_file = request.FILES['document']
        # attributeid1 = request.POST.get('attributeid1')
        # attributeid2 = request.POST.get('attributeid2')

        # print(uploaded_file)
        if uploaded_file.name.endswith('csv'):
            # save the file in media folder
            savefile = FileSystemStorage()
            name = savefile.save(uploaded_file.name, uploaded_file)
            #know where to save the file
            d = os.getcwd() #get the current directory
            file_directory = d+'/media/'+name
            # getOptions(request)
            readfile(file_directory)
            return redirect(options)
        else:
            messages.warning(request, 'File was not uploaded, please use csv file extension')
    return render(request, "draft/myfirst.html", {})

def options(request):
    global attributeid1, attributeid2
    if request.method == 'POST':
        attributeid1 = request.POST.get('attributeid1')
        attributeid2 = request.POST.get('attributeid2')
        print(attributeid1)
        print(attributeid2)
        return redirect(results)
    return render(request, "draft/options.html", {})

def readfile(filename):
    global data
    my_file = pd.read_csv(filename, sep='[:;,|_]', engine='python')
    data = pd.DataFrame(data = my_file, index=None)
    print(data)

def results(request):
    #split into keys and values based on the attribute input
    labels = []
    datas = []
    for x in data[attributeid1]: #name
        labels.append(x)

    for y in data[attributeid2]: #price
        datas.append(y)

    my_labels = dict(Counter(labels))
    my_datas = dict(Counter(datas))
    print('my dashboard ', my_labels)
    labels = my_labels.keys()
    datas = my_datas.keys()
    # values = my_dashboard.values()

    listlabels = []
    listdatas = []
    # listvalues = []
    for x in labels:
        listlabels.append(x)

    for y in datas:
        listdatas.append(y)

    print(listlabels)
    print(listdatas)

    # for y in values:
    #     listvalues.append(y)

    context = {
        'listlabels':listlabels,
        'listdatas':listdatas,
        # 'listvalues':listvalues,
    }

    return render(request, "draft/results.html", context)
####
# def draft(request):
#     context = {}
#
#     if request.method == 'POST':
#         uploaded_file = request.FILES['document']
#         print(uploaded_file)
#
#         if uploaded_file.name.endswith('csv'):
#             savefile = FileSystemStorage()
#             name = savefile.save(uploaded_file.name, uploaded_file)
#             d = os.getcwd()
#             file_directory = d + '/media/' + name
#             return redirect(mysecond)
#
#
#     return render(request, 'draft/myfirst.html')
#

# def mysecond(request):
#     return render(request, 'mysecond.html')
#
#
#
#
#
#



















