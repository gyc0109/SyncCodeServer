from django.forms import ModelForm


class BootStrapModelForm(ModelForm):
    # 排除掉此字段中的bootstrap样式
    exclude_bootstrap = []

    def __init__(self, *args, **kwargs):
        # 执行父类_init_方法
        super().__init__(*args, **kwargs)

        # 自定义功能, 为字段添加bootstrap样式
        # self.fields['hostname'].widget.attrs['class'] = 'form-control'
        for k, field in self.fields.items():
            if k in self.exclude_bootstrap:
                continue
            field.widget.attrs['class'] = 'form-control'
