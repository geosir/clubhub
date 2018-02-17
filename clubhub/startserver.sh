chown -R www-data:www-data /opt/media

ln -s /opt/clubhub/bower_components/ /opt/clubhub/static/meta/
echo "yes" | python3 manage.py collectstatic

tail -f /var/log/apache2/* &
apachectl -DFOREGROUND
