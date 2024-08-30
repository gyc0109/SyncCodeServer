# 使用django自带的随机值
from django.conf import settings
import hashlib


def md5(data_string):
    # 加言意，防止被盗取
    obj = hashlib.md5(settings.SECRET_KEY.encode('utf-8'))
    obj.update(data_string.encode('utf-8'))
    return obj.hexdigest()
