from django import forms

ALGORITHM_CHOICES= [
    ('bubbleSort', 'bubbleSort'),
    ('insertionSort', 'insertionSort'),
    ('quicksort', 'quicksort'),
    ]

class NameForm(forms.Form):
    your_name = forms.CharField(label='numbers', max_length=100)
    algorithm= forms.CharField(label='Select your algorithm', widget=forms.Select(choices=ALGORITHM_CHOICES))