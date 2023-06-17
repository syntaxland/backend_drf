
#!/usr/bin/bash

sudo systemctl daemon-reload
sudo rm -f /etc/nginx/sites-enabled/default

sudo cp /home/ubuntu/backend_drf/nginx/nginx.conf /etc/nginx/sites-available/backend_drf
sudo ln -s /etc/nginx/sites-available/backend_drf /etc/nginx/sites-enabled/
#sudo nginx -t
sudo gpasswd -a www-data ubuntu
sudo systemctl restart nginx

