# IaC — Infrastructure as Code (Ansible, Terraform)

#devops #собес #iac #ansible #terraform

---

## Ansible

<details>
<summary>Для чего нужен ad-hoc в Ansible?</summary>

Быстрое выполнение одной команды на группе хостов без создания playbook. `ansible all -m ping -a "cmd"`
</details>

<details>
<summary>Что такое роли в Ansible? Пример</summary>

Структурированный набор задач, handlers, vars, templates. Повторно используемые куски конфигурации. Директории: tasks, handlers, vars, defaults, files, templates.
</details>

<details>
<summary>Что такое идемпотентность? Примеры</summary>

Повторное выполнение даёт тот же результат. Пример: `apt install` — если уже установлено, ничего не делает. Неидемпотентно: `echo >> file`.
</details>

<details>
<summary>Для чего нужны handlers (хендлеры)?</summary>

Действия, которые выполняются по уведомлению (notify) и только при реальном изменении. Например, перезапуск сервиса после смены конфига.
</details>

<details>
<summary>Разница pull и push модели</summary>

**Push** (Ansible) — управляющий хост запускает задания, пушит на целевые. **Pull** (Puppet, часть Chef) — агенты на хостах сами подтягивают конфиг.
</details>

<details>
<summary>Плюсы Ansible</summary>

Агентов нет (SSH), YAML, идемпотентность, модули под облака и ОС, community роли.
</details>

<details>
<summary>Отличие модуля от плагина</summary>

Модуль — выполняемая задача (apt, copy, template). Плагин — расширение поведения (inventory, connection, callback).
</details>

---

## Terraform

<details>
<summary>Чем Terraform отличается от Ansible?</summary>

**Terraform** — IaC, создание/управление инфраструктурой, state, инкрементальные изменения. **Ansible** — конфигурация уже существующих ресурсов, без state.
</details>

<details>
<summary>Что такое провайдер в Terraform?</summary>

Плагин для работы с API облака или сервиса (AWS, GCP, Kubernetes и т.д.).
</details>

<details>
<summary>Что такое tfstate? Зачем нужен?</summary>

Хранит актуальное состояние инфраструктуры. Нужен для plan/apply — Terraform сравнивает желаемое и фактическое.
</details>

<details>
<summary>Как удалить один ресурс из 20 без правки кода?</summary>

`terraform destroy -target=resource.type.name` — удалить только указанный ресурс.
</details>

<details>
<summary>У вас dev, stage, prod. Как один код для всех сред?</summary>

Workspaces, отдельные state-файлы, переменные (`tfvars`), remote backend с разными key.
</details>

<details>
<summary>Что такое lifecycle в Terraform? create_before_destroy</summary>

Правила жизненного цикла ресурса. `create_before_destroy` — сначала создаёт новый, потом удаляет старый. Уменьшает даунтайм.
</details>

---

## Ссылки

- [[Git]] | [[Linux]] | [[Networks]] | [[Containers]] | [[CI-CD]] | [[Monitoring]]
- [[README]]
