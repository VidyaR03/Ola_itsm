from django.shortcuts import render, redirect


def sayhi(request):
    return render(request, 'tool/dashboard.html')

    