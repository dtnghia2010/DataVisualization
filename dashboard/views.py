import csv
import io

from django.core.checks import messages
from django.shortcuts import render,redirect
from tablib import Dataset

from .models import CountryData, UploadedFile
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



from .models import CountryData
from .forms import UploadFileForm
from django.shortcuts import render, redirect

# views.py
def upload_file(request):
    if request.method == 'POST':
        UploadedFile_resource = request.FILES('myfile')
        dataset = Dataset()
        new_UploadedFile = request.FILES('myfile')

        if not new_UploadedFile.name.endswith('csv'):
            messages.info(request,'Please Upload the CSV File only')
            return render(
                request,'upload_file.html'
            )
        else:messages.info(request,'File successfully uploaded')
        data_set=new_UploadedFile.read().decode('UTF-8')
        io_string=io.StringIO(data_set)
        next(io_string)
        for column in csv.reader(io_string, delimiter=',', quotechar="|"):
            created = UploadedFile.object.update_or_create(
                Country = column[0],
                Population=column[1],

            )
        return render(request, 'dashboard/upload_file.html')
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

    return render(request, 'dashboard/upload_file.html')


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

# your_app/views.py
