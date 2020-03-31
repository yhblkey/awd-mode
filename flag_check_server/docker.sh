#!/bin/sh
docker run -v `cd ./html;pwd`:/var/www/html -v `cd ./tmp;pwd`:/tmp -p 8080:80 -d  --net mynetwork --ip 172.60.0.5 --name flag_check_server -ti yhbl/awd_v3 /tmp/setup.sh
