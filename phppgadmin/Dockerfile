FROM ubuntu:24.04

RUN apt-get update && \
    apt-get install -y \
    apache2 \
    php \
    libapache2-mod-php \
    php-pgsql \
    php-xml \
    php-mbstring \
    git \
    wget \
    unzip && \
    apt-get clean

RUN wget https://github.com/phppgadmin/phppgadmin/archive/refs/heads/master.zip && \
    unzip master.zip && \
    mv phppgadmin-master /var/www/html/phppgadmin && \
    rm master.zip

COPY config.inc.php /var/www/html/phppgadmin/config.inc.php

RUN echo "ServerName localhost" >> /etc/apache2/apache2.conf && \
    a2enmod rewrite

EXPOSE 80

CMD ["apache2ctl", "-D", "FOREGROUND"]
