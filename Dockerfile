FROM ubuntu:14.04.2

# TCP 80
EXPOSE 80

# https://github.com/monokrome/docker-wine/issues/3
ENV DEBIAN_FRONTEND noninteractive

# TMPDIR
WORKDIR /tmp

# apt
RUN apt-get update 

#
RUN apt-get install -y nginx php5-cli php5-fpm

# 
RUN rm -f /etc/nginx/sites-enabled/default
COPY ./etc /etc

# install app
COPY . /src
WORKDIR /src

# start server
CMD php5-fpm && nginx
