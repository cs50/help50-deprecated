FROM cs50/server
EXPOSE 8080

# dependencies
RUN apt-get update && apt-get install -y libmysqlclient-dev
RUN pip3 install mysqlclient
