FROM ubuntu:14.04.2

# TCP 80
EXPOSE 80

# https://github.com/monokrome/docker-wine/issues/3
ENV DEBIAN_FRONTEND noninteractive

# apt
RUN apt-get update 

# install nginx, install PHP
RUN apt-get install -y nginx php5-cli php5-fpm

# install app
COPY . /src
WORKDIR /src

# enable configuration
RUN rm -f /etc/nginx/nginx.conf /etc/nginx/sites-enabled/default && \
    ln -s /src/etc/nginx/nginx.conf /etc/nginx/nginx.conf && \
    ln -s /src/etc/php5/fpm/conf.d/cs50.ini /etc/php5/fpm/conf.d/cs50.ini

# start php5-fpm in background, start nginx in foreground
CMD service php5-fpm start && nginx
