FROM cs50/server
EXPOSE 8080

# for development
ENV PATH /srv/www/opt/cs50/help50/bin:"$PATH"

# dependencies
RUN apt-get update && apt-get install -y libmysqlclient-dev
RUN pip3 install Flask-Migrate Flask-SQLAlchemy mysqlclient pytz
