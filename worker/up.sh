#!/bin/bash

docker build -t worker --no-cache .

docker run -p 8084:8084 -d --name worker --network backend worker