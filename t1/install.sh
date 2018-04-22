#!/bin/bash

# Checking if software is installed
which docker >/dev/null 2>&1
[ $? -ne 0 ] && {
	echo "Error: Docker engine is not installed"
	exit 1
}

which docker-compose >/dev/null 2>&1
[ $? -ne 0 ] && {
        echo "Error: Docker-compose is not installed"
	echo 'You can download it with: "curl -L https://github.com/docker/compose/releases/download/1.21.0/docker-compose-$(uname -s)-$(uname -m)"'
        exit 1
}

which curl >/dev/null 2>&1
[ $? -ne 0 ] && {
        echo "Error: curl is not installed"
        exit 1
}


# Deploying conteiners with docker-compose.yml file
printf "Deploying containers...\n"
docker-compose up -d

s1Response=`curl --write-out "%{http_code}\n" --silent --output /dev/null localhost:8081`
s2Response=`curl --write-out "%{http_code}\n" --silent --output /dev/null localhost:8082`


i=0
until [ $i -ge 5 ] 
do
	printf "Chicking status...\n"
	[ $s1Response == '200' ] &&  [ $s2Response == '200' ] && printf "Conteiners are running\n" && break
	i=$[$i+1]
	printf "No answer.Retrying in 3 sec...\n"
	sleep 3
	s1Response=`curl --write-out "%{http_code}\n" --silent --output /dev/null localhost:8081`
	s2Response=`curl --write-out "%{http_code}\n" --silent --output /dev/null localhost:8082`
done

printf "Checking haproxy backends...\n"

printf "Haproxy1:\n"
docker exec -ti haproxy1 /bin/bash -c "/root/get_haproxy_status.sh"

printf "Haproxy2:\n"
docker exec -ti haproxy2 /bin/bash -c "/root/get_haproxy_status.sh"

