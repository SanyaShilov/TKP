cd /home/sanyash/TKP
git checkout develop
git pull origin develop
git checkout master
git merge develop
git push origin master
./restart_nginx.sh
./restart_app.sh
./rebuild_docs.sh
