#!/bin/bash

#env spark scheduler:
#* default
#  - MASTER_TYPE='default'
#  - MASTER_URL='http://localhost:8080'
#
#
#global SPARK_TARGETS_PATH='/etc/prometheus/spark_targets.json'


docker run -itd \
    -p 9090:9090 \
    -e MASTER_TYPE='default' \
    -e MASTER_URL='http://localhost:8080' \
    -e SPARK_TARGETS_PATH='/etc/prometheus/spark_targets.json' \
    job-discover:latest /bin/bash /app/start.sh
