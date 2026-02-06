FROM python:3.9-slim

WORKDIR /app

# 更新apt源并安装必要的基础包
RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates \
    gnupg \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
# 设置pip使用国内镜像
RUN pip3 config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple

# 安装Java
RUN apt-get update && apt-get install -y --no-install-recommends default-jre-headless && apt-get clean && rm -rf /var/lib/apt/lists/*
ENV JAVA_HOME=/usr/lib/jvm/java-21-openjdk-amd64

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["python", "app.py"]