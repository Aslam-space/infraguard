import shutil

NGINX_CONF = "/home/ubuntu/infraguard/nginx/nginx.conf"
shutil.copy(NGINX_CONF, NGINX_CONF + ".bak3")

new_config = """upstream infraguard {
    server infraguard-app:8080;
}
upstream grafana {
    server infraguard-grafana:3000;
}
upstream prometheus {
    server infraguard-prometheus:9090;
}
server {
    listen 80;
    server_name goat777asm.duckdns.org;
    return 301 https://$host$request_uri;
}
server {
    listen 443 ssl;
    server_name goat777asm.duckdns.org;
    ssl_certificate     /etc/letsencrypt/live/goat777asm.duckdns.org/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/goat777asm.duckdns.org/privkey.pem;
    location /grafana/ {
        proxy_pass http://grafana/grafana/;
        proxy_set_header Host $host;
    }
    location /prometheus/ {
        proxy_pass http://prometheus/;
        proxy_set_header Host $host;
    }
    location / {
        proxy_pass http://infraguard;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
    }
}
"""

with open(NGINX_CONF, "w") as f:
    f.write(new_config)
print("Done!")
