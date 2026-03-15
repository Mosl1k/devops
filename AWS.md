# AWS — облако и сервисы

#devops #собес #aws #cloud

Источник: [Swfuse/devops-interview](https://github.com/Swfuse/devops-interview/blob/main/interview.md)

---

## Основные сервисы

<details>
<summary>EC2 — что это?</summary>

Виртуальные сервера. Модели оплаты: On-Demand, Reserved (скидка), Spot (дешевле, могут забрать). Типы: General Purpose (T3, M5), Compute (C5), Memory (R5), Storage (I3), GPU (P4, G5).
</details>

<details>
<summary>VPC — что это?</summary>

Виртуальная приватная сеть. Subnets (public/private), Internet Gateway, NAT Gateway, Route Tables. Изоляция сетей в облаке.
</details>

<details>
<summary>Security Group — что это?</summary>

Виртуальный файрвол на уровне инстанса. Только Allow-правила. По умолчанию блокируется весь входящий трафик. Один ресурс может быть в нескольких Security Groups.
</details>

<details>
<summary>S3 — что это?</summary>

Object storage. Высокая долговечность. Бакет — уникальное глобальное имя. Классы хранения: Standard, IA, Glacier.
</details>

<details>
<summary>Route 53 — что это?</summary>

Управляемый DNS-сервис. Регистрация доменов, DNS-записи, health checks, маршрутизация трафика.
</details>

<details>
<summary>EKS — что это?</summary>

Управляемый Kubernetes от AWS. Control plane управляется AWS. Worker nodes — EC2 или Fargate. Интеграция с IAM, CloudWatch, ELB, ECR.
</details>

---

## Концепции

<details>
<summary>Как устроен доступ из private subnet в интернет?</summary>

NAT Gateway в public subnet. В route table приватной подсети — 0.0.0.0/0 → NAT Gateway. NAT подменяет source IP на свой и шлёт через Internet Gateway.
</details>

<details>
<summary>EKS Anywhere vs EKS</summary>

EKS — в AWS. EKS Anywhere — тот же API/инструменты, но на bare-metal или on-prem, с интеграцией сервисов AWS.
</details>
