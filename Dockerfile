# 镜像基于python3.6环境
FROM python:3.6-slim
# 把Scrapy项目的requirements.txt和Scrapyd的配置文件复制到工作目录中
COPY requirements.txt scrapyd.conf /code/
WORKDIR /code
# 暴露Scrapyd服务的6800端口
EXPOSE 6800
# 安装Scrapy项目所需的依赖库
RUN pip3 install -r requirements.txt
# 启动Scrapyd服务
CMD scrapyd
