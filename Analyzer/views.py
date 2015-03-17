from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.


def index(request):
    context_dict={'boldmessage':" świecie"}
    return render(request, 'analyzer/analyzer_main.html', context_dict)
