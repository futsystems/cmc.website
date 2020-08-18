FROM marvelsystem/ubuntu1804:python

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

# copy config file
COPY ./ms_platform_config.cfg /app/config

# make start.sh executable
RUN chmod +x start.sh


