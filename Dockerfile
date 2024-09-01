# 使用 CentOS 作为基础镜像
FROM gyc0109/centos7py

# 设置工作目录
WORKDIR /app

# 将项目文件复制到工作目录
COPY . /app/

# 安装 Python 依赖
# 使用阿里云源
RUN pip3 install --no-cache-dir -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/

# 安装git
RUN yum install git -y

# 设置Django工作目录
WORKDIR /app/SyncCodeServer

# 检查项目目录
RUN ls -al /app/SyncCodeServer/web
RUN ls -al /app/SyncCodeServer/web/views
RUN ls -al /app/SyncCodeServer/web/views/server.py

# 初始化数据库
RUN python3 manage.py makemigrations
RUN python3 manage.py migrate

# 暴露应用端口
EXPOSE 8000

# 启动 Django 开发服务器
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]