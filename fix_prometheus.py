NGINX_CONF = "/home/ubuntu/infraguard/nginx/nginx.conf"

with open(NGINX_CONF, "r") as f:
    content = f.read()

old = """    location /prometheus/ {
        proxy_pass http://prometheus/;
        proxy_set_header Host $host;
    }"""

new = """    location /prometheus/ {
        proxy_pass http://prometheus/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header Accept-Encoding "";
        sub_filter 'href="/' 'href="/prometheus/';
        sub_filter 'src="/' 'src="/prometheus/';
        sub_filter_once off;
    }"""

content = content.replace(old, new)
with open(NGINX_CONF, "w") as f:
    f.write(content)
print("Done!")
