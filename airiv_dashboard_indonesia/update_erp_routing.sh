#!/bin/bash
echo ">>> Updating Nginx Server Block for erp.airiv.id routing <<<"

sudo tee /etc/nginx/sites-available/erp.airiv.id > /dev/null << 'CONFIG'
server {
    listen 80;
    server_name erp.airiv.id;

    access_log /var/log/nginx/erp.airiv.id.access.log;
    error_log /var/log/nginx/erp.airiv.id.error.log;

    proxy_read_timeout 720s;
    proxy_connect_timeout 720s;
    proxy_send_timeout 720s;

    proxy_set_header X-Forwarded-Host $host;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
    proxy_set_header X-Real-IP $remote_addr;

    location / {
        proxy_pass http://127.0.0.1:8069;
        proxy_redirect off;
    }

    location /web {
        proxy_pass http://127.0.0.1:8069/web;
        proxy_redirect off;
    }

    location /demo {
        proxy_pass http://127.0.0.1:8069/demo;
        proxy_redirect off;
    }

    location ~* /web/static/ {
        proxy_cache_valid 200 60m;
        proxy_buffering on;
        expires 864000;
        proxy_pass http://127.0.0.1:8069;
    }
}
CONFIG

sudo ln -sf /etc/nginx/sites-available/erp.airiv.id /etc/nginx/sites-enabled/
sudo nginx -t && sudo systemctl reload nginx
echo ">>> erp.airiv.id routing updated and active <<<"
