from django.shortcuts import render,redirect
from . models import CountryData
from .forms import CountryDataFrom

# Create your views here.


def index(request):
    data = CountryData.objects.all()
    if request.method =='POST':
        form = CountryDataFrom(request.POST)
        if form.is_valid():
             form.save()
             return redirect('/')
    else:
        form= CountryDataFrom()
    context = {
        'data':data,
        'form': form,

    }
    return render(request, 'dashboard/index.html', context)



from django.shortcuts import render, redirect
from .models import UploadedFile
from .forms import UploadFileForm
from django.http import HttpResponse

from django.shortcuts import render, redirect
from .models import UploadedFile
from .forms import UploadFileForm

def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = form.save(commit=False)
            uploaded_file.save()

            # Cập nhật biểu đồ ở đây (sử dụng uploaded_file)

            return redirect('upload_file')  # Hoặc chuyển hướng đến trang khác nếu cần
    else:
        form = UploadFileForm()

    uploaded_files = UploadedFile.objects.all()

    return render(request, 'dashboard/upload_file.html', {'form': form, 'uploaded_files': uploaded_files})
