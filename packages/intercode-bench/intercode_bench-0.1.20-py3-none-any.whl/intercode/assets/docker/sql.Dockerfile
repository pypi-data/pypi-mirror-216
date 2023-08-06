FROM mysql

ENV MYSQL_ROOT_PASSWORD="password"

ADD ../datasets/spider_dev.sql /docker-entrypoint-initdb.d