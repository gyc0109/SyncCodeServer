from django.shortcuts import render, redirect
from django.forms import ModelForm
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from web import models
from web.forms.project import ProjectModelForm
from web.utils.pagination import Pagination


def project_list(request):
    # 构造搜索
    data_dict = {}
    search_data = request.GET.get('q', "")
    if search_data:
        data_dict["title__contains"] = search_data

    queryset = models.Project.objects.filter(**data_dict)

    # 分页
    page_object = Pagination(request, queryset)
    context = {
        'queryset': page_object.page_queryset,
        'page_string': page_object.html(),
        'search_data': search_data
    }

    return render(request, "project_list.html", context)


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
