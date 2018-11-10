Osaühingute registri kasutamiseks vajalik tarkvara
- Docker CE (18.06.1.19507)

skritpi töö testitud:
- win7 64bit

Vajalik installida Docker CE vastavalt tarkvara juhistele.
Laadida alla setup.sh https://github.com/Holks/osayhing.git

Rakendus käivitamisek vajalik Dockeri käsud järjekorras
docker pull mysql/mysql-server:8.0
docker run --name mysql -d -e MYSQL_RANDOM_ROOT_PASSWORD=yes \
    -e MYSQL_DATABASE=registry -e MYSQL_USER=osayhing \
    -e MYSQL_PASSWORD='password' \
    mysql/mysql-server:8.0

docker pull rehealune/osayhing:latest
Enne kui järgmist käivitada võiks ära oodata mysql konteineri ülesseadmise
mysql konteineri logi käsuga "docker logs mysql"
docker run --name osayhing -d -p 8000:5000 --rm --link mysql:db rehealune/osayhing:latest


rakenduse konteineri logi käsuga "docker logs osayhing"