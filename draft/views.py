from django.core.files.storage import FileSystemStorage
from django.shortcuts import render, redirect
import os


def draft(request):
    context = {}

    if request.method == 'POST':
        uploaded_file = request.FILES['document']
        print(uploaded_file)

        if uploaded_file.name.endswith('csv'):
            savefile = FileSystemStorage()
            name = savefile.save(uploaded_file.name, uploaded_file)
            d = os.getcwd()
            file_directory = d + '\media\\' + name
            return redirect(mysecond)


    return render(request, 'draft/myfirst.html')


def mysecond(request):
    return render(request, 'mysecond.html')
