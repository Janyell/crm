from django import forms
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, render
from multiuploader.forms import MultiUploadForm
from base_api.form import FileForm, ProductForm, UploadFileForm
from base_api.models import Order_Files, Orders


def my_view_up(request):
    # context = {
    # 'form': MultiUploadForm()
    # }
    # return render(request, "files.html", context)
    out = {}
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            # file is saved
            obj = form.save(commit=False)
            obj.order = Orders.objects.get(id=1)
            try:
                obj.save()
            except Exception as e:
                print e.message
            return HttpResponseRedirect('/')
    else:
        form = UploadFileForm()

    out.update({'form': form})
    out.update({'page_title': 'rtyui'})
    print(form.errors)
    return render(request, 'files.html', out)