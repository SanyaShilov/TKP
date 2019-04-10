sudo cp app.conf /etc/supervisor/conf.d/app.conf
sudo supervisorctl reread
sudo supervisorctl restart all
