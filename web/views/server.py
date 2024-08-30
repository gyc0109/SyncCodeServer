from django.shortcuts import render, redirect
from django.forms import ModelForm
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from web import models
from web.forms.server import ServerModelForm


def server_list(request):
    queryset = models.Server.objects.all()
    return render(request, 'server_list.html', {'queryset': queryset})


@csrf_exempt
def server_add(request):
    if request.method == "GET":
        form = ServerModelForm()
        return render(request, 'form.html', {'form': form})
    # 接受用户提交的数据并进行验证
    form = ServerModelForm(data=request.POST)
    # 验证通过后保存
    if form.is_valid():
        form.save()
        # /server/list/
        return redirect('/server/list/')
    else:
        return render(request, 'form.html', {'form': form})


@csrf_exempt
def server_edit(request, nid):
    server_object = models.Server.objects.filter(id=nid).first()
    if request.method == "GET":
        form = ServerModelForm(instance=server_object)
        return render(request, 'form.html', {'form': form})
    form = ServerModelForm(data=request.POST, instance=server_object)
    # 验证通过后保存
    if form.is_valid():
        form.save()
        # /server/list/
        return redirect('/server/list/')
    else:
        return render(request, 'form.html', {'form': form})


def server_delete(request, nid):
    models.Server.objects.filter(id=nid).delete()
    return JsonResponse({"status": True})
