import csv
import io

from django.core.checks import messages
from django.shortcuts import render, redirect
from django.template import context
from tablib import Dataset

from .models import Add_Data, Upload_File
from .forms import Add_DataFrom
import csv
import io
from django.shortcuts import render, redirect
from django.contrib import messages



# Create your views here.

def index(request):
    return render(request, 'dashboard/index.html')


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








def upload_file(request):
    if request.method == 'POST':
        new_uploaded_file = request.FILES.get('myfile')  # Use get() instead of indexing

        if not new_uploaded_file.name.endswith('csv'):
            messages.info(request, 'Please upload a CSV file only')
            return redirect('upload_file')  # Redirect to the same page

        data_set = new_uploaded_file.read().decode('UTF-8')
        io_string = io.StringIO(data_set)
        next(io_string)
        # Assuming CSV file has two columns: Country and Population
        for column in csv.reader(io_string, delimiter=',', quotechar='|'):
            # Using get_or_create instead of update_or_create
            created, _ = Upload_File.objects.get_or_create(
                CountryName=column[0],
                CountryCode= column[1],
                Year_2022=column[2],
            )

        messages.success(request, 'File successfully uploaded')  # Use success instead of info
        return redirect('upload_file')  # Redirect to the same page after processing the file

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

    # return render(request, 'dashboard/upload_file.html')

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
