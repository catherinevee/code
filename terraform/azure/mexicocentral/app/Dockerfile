# Use an official PHP image as the base image
FROM php:7.4-apache

# Install required dependencies and LibreNMS
RUN apt-get update && apt-get install -y \
    git \
    curl \
    libapache2-mod-php \
    mariadb-client \
    fping \
    snmp \
    rrdtool \
    python3 \
    python3-pip \
    libssl-dev \
    librrd-dev \
    libnet-snmp-perl \
    libdbi-perl \
    libxml2-dev \
    libjpeg-dev \
    libpng-dev \
    libicu-dev \
    libjpeg8-dev \
    libmysqlclient-dev \
    libmcrypt-dev \
    unzip \
    && apt-get clean

# Enable necessary Apache modules
RUN a2enmod rewrite headers

# Set up the LibreNMS installation directory
WORKDIR /var/www/html

# Clone the LibreNMS repository
RUN git clone https://github.com/librenms/librenms.git .

# Set correct file permissions for LibreNMS
RUN chown -R www-data:www-data /var/www/html

# Install Composer (dependency manager for PHP)
RUN curl -sS https://getcomposer.org/installer | php -- --install-dir=/usr/local/bin --filename=composer

# Install PHP dependencies using Composer
RUN composer install --no-dev --optimize-autoloader

# Configure LibreNMS environment
RUN cp .env.example .env

# Expose port 80 for web access
EXPOSE 80

# Configure the entrypoint to run Apache in the foreground
CMD ["apache2-foreground"]
