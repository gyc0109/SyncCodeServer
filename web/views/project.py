from django.shortcuts import render, redirect
from django.forms import ModelForm
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from web import models
from web.forms.project import ProjectModelForm


def project_list(request):
    queryset = models.Project.objects.all()
    return render(request, "project_list.html", {"queryset": queryset})


@csrf_exempt
def project_add(request):
    if request.method == "GET":
        form = ProjectModelForm()
        return render(request, 'form.html', {'form': form})
    # 接受用户提交的数据并进行验证
    form = ProjectModelForm(data=request.POST)
    # 验证通过后保存
    if form.is_valid():
        form.save()
        # /project/list/
        return redirect('/project/list/')
    else:
        return render(request, 'form.html', {'form': form})


@csrf_exempt
def project_edit(request, nid):
    project_object = models.Project.objects.filter(id=nid).first()
    if request.method == "GET":
        form = ProjectModelForm(instance=project_object)
        return render(request, 'form.html', {'form': form})
    form = ProjectModelForm(data=request.POST, instance=project_object)
    # 验证通过后保存
    if form.is_valid():
        form.save()
        return redirect('/project/list/')
    else:
        return render(request, 'form.html', {'form': form})


def project_delete(request, nid):
    models.Project.objects.filter(id=nid).delete()
    return JsonResponse({"status": True})
