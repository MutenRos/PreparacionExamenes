sudo apt install -y php-dev php-pear

phpize --version

sudo pecl install mongodb

echo "extension=mongodb" | sudo tee /etc/php/*/mods-available/mongodb.ini
sudo phpenmod mongodb


sudo mkdir -p /etc/php/8.3/mods-available
echo "extension=mongodb.so" | sudo tee /etc/php/8.3/mods-available/mongodb.ini

sudo phpenmod -v 8.3 mongodb


sudo systemctl restart apache2



