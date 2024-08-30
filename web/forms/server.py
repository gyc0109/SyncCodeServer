from django.forms import ModelForm
from web import models
from web.forms.base import BootStrapModelForm

# 做表单验证, 引入ModelForm
# 1. 自动生成html标签
# 2. 表单验证
class ServerModelForm(BootStrapModelForm):
    class Meta:
        model = models.Server
        fields = "__all__"
