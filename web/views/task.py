from django.shortcuts import HttpResponse, render, redirect
from web.forms.task import TaskModelForm
from django.http import JsonResponse
from django.urls import reverse
from web import models
from web.utils.pagination import Pagination


def task_list(request, project_id):
    queryset = models.DeployTask.objects.filter(project_id=project_id).all()
    project_object = models.Project.objects.filter(id=project_id).first()
    # 分页
    page_object = Pagination(request, queryset)
    context = {
        'project_object': project_object,
        'queryset': page_object.page_queryset,
        'page_string': page_object.html(),
    }

    return render(request, 'task_list.html', context)


def task_add(request, project_id):
    project_object = models.Project.objects.filter(id=project_id).first()

    if request.method == 'GET':
        form = TaskModelForm(project_object)
        return render(request, 'task_form.html', {'form': form, 'project_object': project_object})
    form = TaskModelForm(project_object, data=request.POST)
    if form.is_valid():
        # 重写了save方法
        form.save()
        # return redirect('/task/list/%s' % project_id)
        url = reverse('task_list', kwargs={'project_id': project_id})
        return redirect(url)
    return render(request, 'task_form.html', {'form': form, 'project_object': project_object})


def hook_template(request, tid):
    hook_template_object = models.HookTemplate.objects.filter(id=tid).first()
    return JsonResponse({'status': True, 'content': hook_template_object.content})


def deploy(request, task_id):
    task_object = models.DeployTask.objects.filter(id=task_id).first()

    return render(request, 'deploy.html', {'task_object': task_object})


def task_delete(request, nid):
    models.DeployTask.objects.filter(id=nid).delete()
    return JsonResponse({"status": True})
