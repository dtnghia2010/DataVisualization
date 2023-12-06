import os
from collections import Counter

from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
from django.contrib import messages
import pandas as pd
# Create your views here.
def home_view(request, *args, **kwargs):
    global attributeid1, attributeid2
    context={}
    if request.method == 'POST':
        uploaded_file = request.FILES['document']
        attributeid1 = request.POST.get('attributeid1')
        attributeid2 = request.POST.get('attributeid2')

        # print(uploaded_file)
        print(attributeid1)
        print(attributeid1)
        if uploaded_file.name.endswith('csv'):
            # save the file in media folder
            savefile = FileSystemStorage()
            name = savefile.save(uploaded_file.name, uploaded_file)

            #know where to save the file
            d = os.getcwd() #get the current directory
            file_directory = d+'/media/'+name
            readfile(file_directory)
            return redirect(results)
        else:
            messages.warning(request, 'File was not uploaded, please use csv file extension')
    return render(request, "index.html", {})

def readfile(filename):
    global data
    my_file = pd.read_csv(filename, sep='[:;,|_]', engine='python')
    data = pd.DataFrame(data=my_file, index=None)
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

    # for y in values:
    #     listvalues.append(y)

    context = {
        'listlabels':listlabels,
        'listdatas':listdatas,
        # 'listvalues':listvalues,
    }

    return render(request, "results.html", context)