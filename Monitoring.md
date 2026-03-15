# Monitoring — вопросы для собеседований

#devops #собес #monitoring #мониторинг

---

## Общие

<details>
<summary>Какие инструменты мониторинга бывают?</summary>

Метрики: Prometheus, Grafana, InfluxDB, Datadog. Логи: ELK, Loki, Splunk. Трейсы: Jaeger, Zipkin. APM: New Relic, Dynatrace.
</details>

<details>
<summary>Разница pull и push в мониторинге</summary>

**Pull** (Prometheus) — мониторинг сам забирает метрики по HTTP. **Push** (Graphite, StatsD) — агенты отправляют метрики на сервер.
</details>

<details>
<summary>Black box vs White box мониторинг</summary>

**Black box** — снаружи (доступность, latency). **White box** — метрики изнутри (CPU, память, логи приложения).
</details>

---

## ELK / Loki

<details>
<summary>Как устроен сбор логов? (Agent → collector → storage → UI)</summary>

Agent (Filebeat, Fluentd) собирает логи → Collector/Ingest (Logstash, Loki) обрабатывает → Storage (Elasticsearch, Loki) → UI (Kibana, Grafana).
</details>

<details>
<summary>Что такое Fluentd, Filebeat, Logstash?</summary>

**Filebeat** — лёгкий шipper (отправка логов). **Logstash** — обработка, парсинг, фильтрация. **Fluentd** — альтернатива, сбор и роутинг логов.
</details>

---

## Prometheus / Grafana

<details>
<summary>Как работает Prometheus?</summary>

Периодически скрапит targets (HTTP endpoints с метриками). Хранит time-series. PromQL для запросов. Alertmanager для алертов.
</details>

<details>
<summary>Что такое node_exporter, cAdvisor?</summary>

**node_exporter** — метрики хоста (CPU, память, диск, сеть). **cAdvisor** — метрики контейнеров (CPU, память, сеть per container).
</details>

<details>
<summary>Зачем нужен Alertmanager?</summary>

Обработка алертов от Prometheus: дедупликация, группировка, маршрутизация (email, Slack, PagerDuty).
</details>

---

## SLO, SLA, SLI

<details>
<summary>Что такое SLO, SLA, SLI?</summary>

- **SLI** (Service Level Indicator) — измеряемая метрика (uptime, latency, error rate)
- **SLO** (Service Level Objective) — целевое значение SLI (99.9% uptime)
- **SLA** (Service Level Agreement) — договор с клиентом, последствия при нарушении SLO
</details>

<details>
<summary>Привести примеры SLO и SLA</summary>

SLO: «Доступность API 99.9% в месяц», «Latency p99 &lt; 200 ms».  
SLA: «При простоях &gt; 0.1% — компенсация», «За нарушение бэкапов — возврат стоимости услуги».
</details>

---

## Метрики и логи

<details>
<summary>Какие метрики нужно собирать?</summary>

Golden signals: latency, traffic, errors, saturation. Плюс ресурсы (CPU, RAM, disk, network), специфичные метрики приложения.
</details>

<details>
<summary>Infrastructure vs application мониторинг</summary>

**Infrastructure** — хост, контейнеры, сеть. **Application** — RPS, latency, ошибки, бизнес-метрики.
</details>

---

## Ссылки

- [[Git]] | [[Linux]] | [[Networks]] | [[Containers]] | [[IaC]] | [[CI-CD]]
- [[Hardware]] | [[Debug]] | [[Databases]] | [[Python]] | [[Kubernetes]] | [[AWS]]
- [[README]]
