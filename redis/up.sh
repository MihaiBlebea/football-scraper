#!/bin/bash

docker run -p 6379:6379 -d --name redis --network backend redis