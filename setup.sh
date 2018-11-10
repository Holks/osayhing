docker pull mysql/mysql-server:8.0
docker images
docker run --name rehealune -d mysql/mysql-server:8.0
docker ps
docker logs rehealune
docker logs rehealune 2>&1 | grep GENERATED
#change root password accordingly NB!
docker exec -it rehealune mysql -uroot -p --connect-expired-password --execute="ALTER USER 'root'@'localhost' IDENTIFIED BY 'password';"
docker exec -it rehealune mysql -uroot -p --execute="CREATE USER 'osayhing'@'localhost' IDENTIFIED BY 'password';"
docker exec -it rehealune mysql -uroot -p --execute="CREATE DATABASE registry;"
docker exec -it rehealune mysql -uroot -p --execute="SHOW GRANTS FOR 'osayhing'@'localhost';"
docker exec -it rehealune mysql -uroot -p --execute="GRANT ALL PRIVILEGES ON registry.* TO 'osayhing'@'localhost';"
docker exec -it rehealune mysql -uroot -p --execute="FLUSH PRIVILEGES;"

docker pull rehealune/osayhing:latest
docker images
docker ps
docker run --name=osayhing -d -p 5000:8000 --rm --link mysql:dbserver docker qIk[3J4lbynomXYMijOheNAtyRuB --connect-expired-password 



docker run --name osayhing -d -p 5000:8000 --rm --link mysql/mysql-server:8.0 rehealune/osayhing:latest

docker exec -it rehealune mysql -uroot -p --connect-expired-password --execute="CREATE USER 'osayhing'@'localhost' IDENTIFIED BY 'password';CREATE DATABASE registry;SHOW GRANTS FOR 'osayhing'@'localhost';GRANT ALL PRIVILEGES ON registry.* TO 'osayhing'@'localhost';FLUSH PRIVILEGES;"

docker run --name osayhing -d -p 8000:5000 --rm --link mysql:db osayhing


docker run --name mysql -d -e MYSQL_RANDOM_ROOT_PASSWORD=yes -e MYSQL_DATABASE=registry -e MYSQL_USER=osayhing -e MYSQL_PASSWORD='password' mysql/mysql-server