from django.http import HttpResponse
from django.shortcuts import render

def main_page(request):
    return HttpResponse("<p> 666 </p>")
