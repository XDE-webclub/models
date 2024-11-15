# 使用自带 Python 3 的 Ubuntu 基础镜像
FROM python

# 设置工作目录
WORKDIR /app

# 复制项目文件到容器中
COPY . /app

# 创建虚拟环境并安装项目依赖
RUN pip install -r requirements.txt 

# 暴露应用程序端口
EXPOSE 3000
EXPOSE 8000
# 确保在 /app 目录下执行命令
WORKDIR /app

CMD ["python", "-m", "reflex", "run"]

