FROM registry.cn-hangzhou.aliyuncs.com/marvelsystem/django:1.10.4

# make directory
RUN mkdir /app
RUN mkdir /app/bin
RUN mkdir /app/config
RUN mkdir /app/logs

# change current work directory
WORKDIR /app/bin

# copy all files to /app/bin
ADD . /app/bin

# install package
RUN pip install -r /app/bin/packages.txt -i http://pypi.douban.com/simple --trusted-host pypi.douban.com

# make start.sh executable
RUN chmod +x start.sh


