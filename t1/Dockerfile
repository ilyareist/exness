FROM ubuntu:16.04

RUN apt-get update && apt-get install -y \
    nginx \
    haproxy \
    supervisor \
    socat

# Copying conf files
ADD conf/haproxy.cfg /etc/haproxy/haproxy.cfg
ADD conf/supervisord.conf /etc/supervisord.conf
ADD conf/get_haproxy_status.sh /root/get_haproxy_status.sh

RUN mkdir -p /var/log/supervisor
RUN mkdir -p /run/haproxy
RUN chmod +x /root/get_haproxy_status.sh

CMD ["/usr/bin/supervisord"]
