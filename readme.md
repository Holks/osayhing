#!/bin/sh
## Osaühingute registri kasutamiseks vajalik tarkvara
## - Docker CE (18.06.1.19507)

## skripti tööd katsetatud:
## - win7 64bit

## vajalik installida Docker CE vastavalt tarkvara juhistele sobivas keskkonnas

## cd ~
## mkdir apps
## cd apps
## lähtekood
## git clone https://github.com/Holks/osayhing.git
## cd osayhing
docker pull rehealune/osayhing:latest
## vajadusel (NB! reavahetused LF-ks):
##docker build -t rehealune/osayhing:latest .

## Rakendus käivitamisek vajalik Dockeri käsud järjekorras
docker pull mysql/mysql-server:8.0
## vajadusel muuta parooli/kasutajat järgmisel real ja config failis
docker run --name mysql -d -e MYSQL_RANDOM_ROOT_PASSWORD=yes \
    -e MYSQL_DATABASE=registry -e MYSQL_USER=osayhing \
    -e MYSQL_PASSWORD='password' \
    mysql/mysql-server:8.0
## kas konteiner käivitus
docker ps
docker inspect mysql
## enne kui järgmist käivitada võiks ära oodata mysql konteineri
## ülesseadmise kui ei kasuta automaatskripti
## mysql konteineri logi käsuga:
docker logs mysql
## kasutada build-itud image-t
docker run --name osayhing -d -p 8000:5000 --rm --link mysql:db \
    rehealune/osayhing:latest

## kontrollida, et mõlemad konteinerid käivitusid:
docker ps

## kui rakendus ei saa ühendust, siis vaadata üle IP ja pordid.

## rakenduse konteineri logi saadav käsuga
docker logs osayhing
## kui logist nähtub, et ei saanud ühendust mysql-ga, siis
## mysql pole veel ennast üles seadnud
## andmebaasis mängimiseks [parool sama, mis eespool]:
## docker exec -it mysql mysql -u osayhing -p
