# CI/CD — вопросы для собеседований

#devops #собес #cicd

---

## Основы

<details>
<summary>Чем CI отличается от CD (Delivery и Deployment)?</summary>

**CI** — автоматическая сборка и тесты при коммите. **CD Delivery** — артефакт готов к деплою, но деплой ручной. **CD Deployment** — деплой тоже автоматический.
</details>

<details>
<summary>Основные этапы CI/CD</summary>

Сборка → тесты (unit, integration) → линтеры/анализ → сбор артефакта → деплой (staging → prod). В CI: build, test, artifact.
</details>

<details>
<summary>Пример процесса CI/CD после пуша в Git</summary>

Webhook → pipeline: checkout → install deps → build → test → (опционально) push image → deploy на stage/prod.
</details>

---

## GitLab CI

<details>
<summary>Что такое <code>when: always</code> в GitLab CI?</summary>

Job выполняется всегда, независимо от результата предыдущих stages. По умолчанию job не запускается, если failed на предыдущем stage.
</details>

<details>
<summary>Что делает <code>extends: .plan</code> в GitLab CI?</summary>

Наследование конфигурации от template- job. Переиспользование общих настроек.
</details>

<details>
<summary>Как сделать job только при ручном запуске?</summary>

`when: manual` — job появляется в pipeline, но не запускается автоматически.
</details>

<details>
<summary>5 проектов на одном языке. Как избежать дублирования конфига пайплайнов?</summary>

`include` из общего репозитория, `extends` от template- job, общие stages и variables.
</details>

<details>
<summary>before_script и after_script — в чём разница?</summary>

`before_script` — выполняется до `script` в той же сессии; переменные доступны в script.  
`after_script` — отдельная сессия, всегда выполняется (даже при fail); переменные из script недоступны.
</details>

<details>
<summary>Как запускать тесты только при MR?</summary>

`rules: - if: '$CI_PIPELINE_SOURCE == "merge_request_event"'`
</details>

<details>
<summary>Что такое кэширование в GitLab CI?</summary>

Сохранение директорий (node_modules, vendor) между job/pipeline. `cache: paths`, `key`, `policy` (pull-push, pull). Ускоряет сборку.
</details>

---

## Ссылки

- [[Git]] | [[Linux]] | [[Networks]] | [[Containers]] | [[IaC]] | [[Monitoring]]
- [[Hardware]] | [[Debug]] | [[Databases]] | [[Kubernetes]] | [[AWS]]
- [[README]]
