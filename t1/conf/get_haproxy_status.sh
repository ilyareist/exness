echo "show stat" | socat unix-connect:/var/run/haproxy/admin.sock stdio | grep haproxy | cut -f2,18 -d","
