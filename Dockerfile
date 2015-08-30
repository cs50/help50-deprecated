FROM ubuntu:14.04.2

# TCP 80
EXPOSE 80

# https://github.com/monokrome/docker-wine/issues/3
ENV DEBIAN_FRONTEND noninteractive

# TMPDIR
WORKDIR /tmp

# apt
RUN apt-get update 

# install app
COPY . /src
WORKDIR /src

# start server
CMD ["bash"]
