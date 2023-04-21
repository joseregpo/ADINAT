#!/bin/bash

source config.conf
ip=$ip
port=$port

python client.py "$ip:$port"
