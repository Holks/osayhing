#!/bin/bash

REGEX_PSWD=""

docker pull mysql/mysql-server:8.0
docker images
docker run --name=rehealune -d mysql/mysql-server:8.0
docker ps
docker logs rehealune

# var2=$(docker logs rehealune 2>&1 | grep -o 'PASSWORD:\K\w+')
# echo $var2
# read -sp 'Please provide new mysql password: \n' passvar
# echo $passvar
# docker exec -it rehealune mysql -uroot -p --user="$user" --password="$passvar" --database="$user" --execute="ALTER USER 'root'@'localhost' IDENTIFIED BY $passvar;"
# CREATE USER 'osayhing'@'localhost' IDENTIFIED BY 'password';
# CREATE DATABASE registry;
# CREATE USER 'osayhing'@'localhost' IDENTIFIED BY 'password';
# SHOW GRANTS FOR 'osayhing'@'localhost';