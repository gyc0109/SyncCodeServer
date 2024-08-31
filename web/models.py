from django.db import models


# Create your models here.

# 服务器表
class Server(models.Model):
    hostname = models.CharField(verbose_name='主机名', max_length=128)

    def __str__(self):
        return self.hostname


# 项目表
class Project(models.Model):
    title = models.CharField(verbose_name='项目名称', max_length=256)
    # 项目所在仓库 https://github.com/xxx/xxx
    repo = models.CharField(verbose_name='仓库地址', max_length=256)

    env_choices = (
        ('prod', '生产环境'),
        ('test', '测试环境'),
    )
    env = models.CharField(verbose_name='环境', max_length=128, choices=env_choices, default='test')

    path = models.CharField(verbose_name='线上项目路径', max_length=256)
    servers = models.ManyToManyField(verbose_name='关联服务器', to='Server')

    def __str__(self):
        return "%s-%s" % (self.title, self.get_env_display())


# 发布任务表
class DeployTask(models.Model):
    uid = models.CharField(verbose_name='标识', max_length=64)
    project = models.ForeignKey(verbose_name='项目环境', to='Project', on_delete=models.CASCADE)
    tag = models.CharField(verbose_name='版本号', max_length=128)

    status_choices = (
        (1, '待发布'),
        (2, '发布中'),
        (3, '成功'),
        (4, '失败'),
    )
    status = models.IntegerField(verbose_name='状态', choices=status_choices, default=1)

    before_download_script = models.TextField(verbose_name='下载前脚本', null=True, blank=True)
    after_download_script = models.TextField(verbose_name='下载后脚本', null=True, blank=True)
    before_deploy_script = models.TextField(verbose_name='发布前脚本', null=True, blank=True)
    after_deploy_script = models.TextField(verbose_name='发布后脚本', null=True, blank=True)


# 钩子模板
class HookTemplate(models.Model):
    title = models.CharField(verbose_name="标题", max_length=32)
    content = models.TextField(verbose_name='脚本内容')

    hook_type_choices = (
        (2, '下载前'),
        (4, '下载后'),
        (6, '发布前'),
        (8, '发布后'),
    )
    hook_type = models.IntegerField(verbose_name='钩子类型', choices=hook_type_choices)


# 发布节点
class Node(models.Model):
    task = models.ForeignKey(verbose_name='发布任务单', to='DeployTask', on_delete=models.CASCADE)

    text = models.CharField(verbose_name='节点文字', max_length=32)
    status_choices = [
        ("lightgray", '待发布'),
        ("green", '成功'),
        ("red", '失败'),
    ]
    status = models.CharField(verbose_name='状态', max_length=16, choices=status_choices, default='lightgray')
    parent = models.ForeignKey(verbose_name='父节点', to='self', null=True, blank=True, on_delete=models.CASCADE)
    server = models.ForeignKey(verbose_name='服务器', to='Server', null=True, blank=True, on_delete=models.CASCADE)


class Admin(models.Model):
    """ 管理员表 """
    username = models.CharField(verbose_name='用户名', max_length=32)
    password = models.CharField(verbose_name='密码', max_length=64)
    phone = models.CharField(verbose_name='手机号', max_length=32)
    email = models.CharField(verbose_name='邮箱', max_length=32)

    # 返回模型的字符串表示形式，即用户名
    # 当调用 str() 方法时，会返回管理员的用户名
    def __str__(self):
        return self.username
