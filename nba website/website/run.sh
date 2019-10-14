#!/bin/bash

rm nohup.out
nohup uwsgi --socket 127.0.0.1:7002 --wsgi-file 6-flask_svr.py --callable app --processes 4 --threads 2 --stats 127.0.0.1:7052 &
