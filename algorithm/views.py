from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

from .forms import NameForm
# Create your views here.

def index(request):
    return HttpResponse("Chao ca nha")

def insertionSort(nts):

    print("Just used insertion sort")

    for i in range(1, len(nts)):
        current_num = nts[i]
        p = i - 1

        while p >= 0 and nts[p] > current_num:
            nts[p + 1] = nts[p]
            p -= 1

        nts[p + 1] = current_num
    return nts

def bubbleSort(nts):

    print("Just used bubble sort")

    nts_len = len(nts)

    for i in range(nts_len):
        for p in range(nts_len - i - 1):
            if nts[p] > nts[p + 1]: # change to < for descending
                nts[p], nts[p + 1] = nts[p + 1], nts[p]
    return nts

def submitted(request):

    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = NameForm(request.POST)
        # check whether it's valid:
        if form.is_valid():

            x = request.POST['your_name']
            algorithm = request.POST['algorithm']

            y = x.split()

            map_object = map(int, y)

            list_of_integers = list(map_object)

            z = globals()[algorithm](list_of_integers)

            print(z)

    # if a GET (or any other method) we'll send the user back to the home page
    else:
        return HttpResponseRedirect('/')
    # need the .html to visualize the results
    return render(request, "", {'nts':z})