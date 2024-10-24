FROM openresty/openresty:alpine-fat
 
RUN mkdir /var/log/nginx \
 && apk add --no-cache openssl-dev \
 && apk add --no-cache git \
 && apk add --no-cache gcc \
 && luarocks install lua-resty-openidc \
 && mkdir /opt/lua

EXPOSE 80
 
ENTRYPOINT ["/usr/local/openresty/nginx/sbin/nginx", "-g", "daemon off;"]

