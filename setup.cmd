docker pull mysql/mysql-server:8.0
docker images
docker run --name mysql -d mysql/mysql-server:8.0
docker ps
docker logs rehealune

docker run --name osayhing -d -p 8000:5000 --rm --link mysql:dbserver rehealune/osayhing:latest