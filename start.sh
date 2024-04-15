#!/bin/bash

prometheus --config.file=/etc/prometheus/prometheus.yml \
           --storage.tsdb.path=/etc/prometheus/data \
           --storage.tsdb.retention.time=21d >> /etc/prometheus/logs/prometheus.log 2>&1 &

cd /app/job_discover
python3 ./main.py
