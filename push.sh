#!/bin/bash

docker-compose up --build -d

docker-compose down

docker-compose push