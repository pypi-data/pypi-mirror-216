FROM mysql

ENV MYSQL_ROOT_PASSWORD="password"

ADD ./data/spider_dev.sql /docker-entrypoint-initdb.d