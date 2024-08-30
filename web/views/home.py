from django.shortcuts import render, redirect

def home_show(request):
    return render(request, 'home_show.html')