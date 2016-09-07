#!/bin/sh
docker rm -v $(docker ps -a -q -f status=exited) > /dev/null
docker rmi -f $(docker images -f "dangling=true" -q) > /dev/null
