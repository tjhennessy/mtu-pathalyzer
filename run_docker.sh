#!/usr/bin/env bash

set -e

sudo docker build -t docker-mtu-pathalyzer .

docker run -it docker-mtu-pathalyzer bash
