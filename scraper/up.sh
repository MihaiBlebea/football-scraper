#!/bin/bash

docker build -t scraper --no-cache .

docker run -p 8083:8083 -d --name scraper --network backend scraper