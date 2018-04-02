# -*- coding: utf-8 -*-

import os
import multiprocessing

# logdir = "/tmp"
logdir = "/var/log/pulsewallet"

# bind = "127.0.0.1:5000"
bind = "unix:/tmp/pulsewallet_gunicorn.socket"

# Recommended value for 'workers' parameter is in 2-4 x $(NUM_CORES) range
workers = multiprocessing.cpu_count() * 2 + 1
# workers = 2
keepalive = 5

# user = "pulsewallet"
# group = "pulsewallet"

# accesslog = logdir + "/gunicorn-access.log"
accesslog = None  # see nginx's accesslog if needed
errorlog = logdir + "/gunicorn-error.log"

loglevel = "info"
proc_name = "pulsewallet-gunicorn"
timeout = 600
pidfile = "/tmp/pulsewallet-gunicorn.pid"
# pidfile = "/tmp/my-gunicorn.pid"
