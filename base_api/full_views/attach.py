from django.shortcuts import render
from base_api.form import FileForm


def my_view_up(request):
    context = {
        'form': FileForm()
    }
    return render(request, "files.html", context)