"""
URL configuration for Server_Management project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from tkinter.font import names

from django.contrib import admin
from django.urls import path
from web.views import server, project, task, admin, account, home

urlpatterns = [
    # path("admin/", admin.site.urls),

    # 默认展示页面路径
    path("", home.home_show, name='home_show'),
    path("home/", home.home_show, name='home_show'),

    # 服务器管理
    path("server/list/", server.server_list, name='server_list'),
    path("server/add/", server.server_add, name='server_add'),

    # (?P<pk>\d+/$ 正则表达式, 用来匹配到url中的内容(ID)
    path("server/edit/<int:nid>/", server.server_edit, name='server_edit'),
    path("server/delete/<int:nid>/", server.server_delete, name='server_delete'),

    # 项目管理
    path("project/list/", project.project_list, name='project_list'),
    path("project/add/", project.project_add, name='project_add'),
    path("project/edit/<int:nid>/", project.project_edit, name='project_edit'),
    path("project/delete/<int:nid>/", project.project_delete, name='project_delete'),

    # 任务管理
    path("task/list/<int:project_id>/", task.task_list, name='task_list'),
    path("task/add/<int:project_id>/", task.task_add, name='task_add'),
    path("hook/template/<int:tid>/", task.hook_template, name='hook_template'),
    path("deploy/<int:task_id>/", task.deploy, name='deploy'),

    # 管理员
    path('admin/list/', admin.admin_list, name='admin_list'),
    path('admin/add/', admin.admin_add, name='admin_add'),
    path('admin/<int:nid>/edit/', admin.admin_edit, name='admin_edit'),
    path('admin/<int:nid>/delete/', admin.admin_delete, name='admin_delete'),
    path('admin/<int:nid>/reset/', admin.admin_reset, name='admin_reset'),

    # 登录
    path('login/', account.login, name='login'),
    path('logout/', account.logout, name='logout'),
    path('image/code/', account.image_code, name='image_code'),

]
