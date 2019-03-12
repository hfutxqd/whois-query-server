#!/usr/bin/env bash

nohup redis-server &
python server.py

docker run -d -p8000:8000 -e CALLBACK_POST_URL=http://192.168.105.97:3000/v1/whoisFeedback whois-test