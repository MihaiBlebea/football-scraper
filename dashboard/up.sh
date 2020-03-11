#!/bin/bash

docker build -t dashboard --no-cache .

docker run -p 8081:8081 -d --name dashboard --network backend dashboard