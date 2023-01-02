# FriendHub

![Lint](https://github.com/radu781/FriendHub/actions/workflows/format_and_lint.yml/badge.svg)
![Lint](https://github.com/radu781/FriendHub/actions/workflows/run_tests.yml/badge.svg)
![Lint](https://github.com/radu781/FriendHub/actions/workflows/deploy.yml/badge.svg)

Simple social media platform where you can share photos, chat and have fun with friends

## Automation and API

All API related information can be found at [https://friendhub.social/api](https://friendhub.social/api)

## Setup

If you want to self host this web app:

- install python 3.11
- install python requirements

    ```bash
    sudo apt-get install python3-pip
    pip3 install -r friendhub/config/requirements.txt
    ```

- edit [friendhub.wsgi](friendhub.wsgi) to use your project path
- edit [data.example.ini](friendhub/config/data.example.ini) and rename it to `data.example`
- set up web server (I used apache2), tutorial [here](https://www.youtube.com/watch?v=YFBRVJPhDGY). Fallback guide:
  - install apache

    ```bash
    sudo apt update
    sudo apt install apache2
    ```

  - configure firewall

    ```bash
    sudo ufw app list
    sudo ufw allow 'Apache'
    sudo systemctl status apache2
    ```

  - enable mod_wsgi and create flask app (it is recommended to never run pip install as root)

    ```bash
    sudo apt-get install libapache2-mod-wsgi-py3 python3-dev
    cd /var/www
    sudo mkdir appName
    cd appName
    ```

  - enable virtual host

    ```bash
    sudo cat << EOF > /etc/apache2/sites-available/appName.conf
    <VirtualHost *:80>
        ServerName ip
        ServerAdmin email@mywebsite.com
        WSGIScriptAlias / /var/www/appName/appName.wsgi
        <Directory /var/www/appName/appName/>
            Order allow,deny
            Allow from all
        </Directory>
        Alias /static /var/www/appName/appName/static
        <Directory /var/www/appName/appName/static/>
            Order allow,deny
            Allow from all
        </Directory>
        ErrorLog ${APACHE_LOG_DIR}/error.log
        LogLevel warn
        CustomLog ${APACHE_LOG_DIR}/access.log combined
    </VirtualHost>
    EOF

    sudo a2ensite appName
    systemctl reload apache2
    sudo service apache2 restart
    ```
