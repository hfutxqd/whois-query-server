#!/usr/bin/env bash

nohup redis-server &
python server.py
