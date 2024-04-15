FROM python:3.11

RUN mkdir /app

# 設定工作目錄
WORKDIR /app

# 安裝 Prometheus
# 定義 Prometheus 版本和相關變數
ENV PROMETHEUS_VERSION 2.39.1

RUN curl -LO "https://github.com/prometheus/prometheus/releases/download/v${PROMETHEUS_VERSION}/prometheus-${PROMETHEUS_VERSION}.linux-amd64.tar.gz" && \
    tar -xvzf "prometheus-${PROMETHEUS_VERSION}.linux-amd64.tar.gz" -C /usr/local/bin/ --strip-components=1 && \
    rm "prometheus-${PROMETHEUS_VERSION}.linux-amd64.tar.gz"

RUN mkdir -p /etc/prometheus/logs
RUN mkdir -p /etc/prometheus/data

COPY prometheus.yml /etc/prometheus/prometheus.yml
COPY job_discover /app/job_discover
COPY start.sh /app/start.sh

RUN pip install --upgrade pip && pip install --no-cache-dir -r /app/job_discover/requirements.txt

#CMD ["/bin/bash /app/start.sh"]
