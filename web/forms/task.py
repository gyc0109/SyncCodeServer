import datetime
from os import environ
from web.forms.base import BootStrapModelForm
from web import models
from django import forms


class TaskModelForm(BootStrapModelForm):
    exclude_bootstrap = [
        "before_download_template",
        "after_download_template",
        'before_deploy_template',
        'after_deploy_template'
    ]

    before_download_select = forms.ChoiceField(required=False, label='下载前')
    before_download_title = forms.CharField(required=False, label='模板名称')
    before_download_template = forms.BooleanField(required=False, widget=forms.CheckboxInput, label='是否保存为模板')

    after_download_select = forms.ChoiceField(required=False, label='下载后')
    after_download_title = forms.CharField(required=False, label='模板名称')
    after_download_template = forms.BooleanField(required=False, widget=forms.CheckboxInput, label='是否保存为模板')

    before_deploy_select = forms.ChoiceField(required=False, label='发布前')
    before_deploy_title = forms.CharField(required=False, label='模板名称')
    before_deploy_template = forms.BooleanField(required=False, widget=forms.CheckboxInput, label='是否保存为模板')

    after_deploy_select = forms.ChoiceField(required=False, label='下载后')
    after_deploy_title = forms.CharField(required=False, label='模板名称')
    after_deploy_template = forms.BooleanField(required=False, widget=forms.CheckboxInput, label='是否保存为模板')

    class Meta:
        model = models.DeployTask
        # fields = "__all__"
        exclude = ['uid', 'project', 'status']

    def __init__(self, project_object, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.project_object = project_object

        self.init_hook()

    def init_hook(self):
        before_download = [(0, '请选择'), ]
        before_download.extend(models.HookTemplate.objects.filter(hook_type=2).values_list('id', 'title'))
        self.fields['before_download_select'].choices = before_download

        after_download = [(0, '请选择'), ]
        after_download.extend(models.HookTemplate.objects.filter(hook_type=4).values_list('id', 'title'))
        self.fields['after_download_select'].choices = after_download

        before_deploy = [(0, '请选择'), ]
        before_deploy.extend(models.HookTemplate.objects.filter(hook_type=6).values_list('id', 'title'))
        self.fields['before_deploy_select'].choices = before_deploy

        after_deploy = [(0, '请选择'), ]
        after_deploy.extend(models.HookTemplate.objects.filter(hook_type=8).values_list('id', 'title'))
        self.fields['after_deploy_select'].choices = after_deploy

    def save(self, commit=True):
        # 保存: 当前任务发布单的表
        self.instance.uid = self.create_uid()
        self.instance.project_id = self.project_object.id
        super().save(commit)

        # 模板钩子
        if self.cleaned_data.get('before_download_template'):
            title = self.cleaned_data.get('before_download_title')
            content = self.cleaned_data.get('before_download_script')
            models.HookTemplate.objects.create(title=title, content=content, hook_type=2)

        if self.cleaned_data.get('after_download_template'):
            title = self.cleaned_data.get('after_download_title')
            content = self.cleaned_data.get('after_download_script')
            models.HookTemplate.objects.create(title=title, content=content, hook_type=4)

        if self.cleaned_data.get('before_deploy_template'):
            title = self.cleaned_data.get('before_deploy_title')
            content = self.cleaned_data.get('before_deploy_script')
            models.HookTemplate.objects.create(title=title, content=content, hook_type=6)

        if self.cleaned_data.get('after_deploy_template'):
            title = self.cleaned_data.get('after_deploy_title')
            content = self.cleaned_data.get('after_deploy_script')
            models.HookTemplate.objects.create(title=title, content=content, hook_type=8)

    def create_uid(self):
        title = self.project_object.title
        env = self.project_object.env
        tag = self.cleaned_data.get('tag')
        date = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        return "{0}-{1}-{2}-{3}".format(title, env, tag, date)

    def clean(self):
        if self.cleaned_data.get('before_download_template'):
            title = self.cleaned_data.get('before_download_title')
            if not title:
                self.add_error("before_download_title", '请输入模板名称')

        if self.cleaned_data.get('after_download_template'):
            title = self.cleaned_data.get('after_download_title')
            if not title:
                self.add_error("after_download_title", '请输入模板名称')

        if self.cleaned_data.get('before_deploy_template'):
            title = self.cleaned_data.get('before_deploy_title')
            if not title:
                self.add_error("before_deploy_title", '请输入模板名称')

        if self.cleaned_data.get('after_deploy_template'):
            title = self.cleaned_data.get('after_deploy_title')
            if not title:
                self.add_error("after_deploy_title", '请输入模板名称')
