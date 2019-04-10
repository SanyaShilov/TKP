sudo cp run_apps.conf /etc/supervisor/conf.d/run_apps.conf
sudo supervisorctl reread
sudo supervisorctl restart all
