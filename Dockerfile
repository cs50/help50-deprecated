FROM ubuntu:14.04.2

# TCP 80
EXPOSE 80

# https://github.com/monokrome/docker-wine/issues/3
ENV DEBIAN_FRONTEND noninteractive

# apt
RUN apt-get update 

# install curl, nginx, PHP
RUN apt-get install -y curl nginx php5-cli php5-fpm

# install composer
RUN curl -sS https://getcomposer.org/installer | php -- --install-dir=/usr/local/bin --filename=composer

# install app
COPY . /src
WORKDIR /src

# enable configuration
RUN rm -f /etc/nginx/nginx.conf /etc/nginx/sites-enabled/default && \
    ln -s /src/etc/nginx/nginx.conf /etc/nginx/nginx.conf && \
    ln -s /src/etc/php5/fpm/conf.d/cs50.ini /etc/php5/fpm/conf.d/cs50.ini

# start container
CMD ./start.sh
