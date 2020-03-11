#!/bin/bash

docker run --name db \
        -p 3306:3306 \
        --network backend \
        --env MYSQL_ROOT_PASSWORD=root \
        --env MYSQL_DATABASE=db \
        --env MYSQL_USER=admin \
        --env MYSQL_PASSWORD=pass \
        -d \
        -v ${PWD}/volume:/bitnami/mariadb \
        mariadb:latest