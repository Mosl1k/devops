# Containers / Docker — вопросы для собеседований

#devops #собес #docker #контейнеры

---

## Основы

<details>
<summary>Что такое Docker и какие инструменты Linux в основе? Для чего используется?</summary>

Docker базируется на **namespaces**, **cgroups**, **capabilities**, **overlayFS**. Используется для упаковки приложений в изолированные контейнеры. Компоненты: daemon, CLI, Dockerfile, Image, Container, registry.
</details>

<details>
<summary>Что такое контейнеры и образы?</summary>

**Образ** — read-only шаблон (слои). **Контейнер** — запущенный образ с верхним read-write слоем. Образ = «установочный диск», контейнер = «установленная и работающая программа».
</details>

<details>
<summary>Виртуализация vs эмуляция vs контейнеризация</summary>

**Виртуализация** — гипервизор, отдельные гостевые ОС. **Эмуляция** — программная эмуляция железа. **Контейнеры** — общее ядро хоста, изоляция через namespaces и cgroups.
</details>

<details>
<summary>Разница между <code>docker stop</code> и <code>docker pause</code>?</summary>

**stop** — отправляет SIGTERM, контейнер завершается. **pause** — замораживает (cgroup freezer), процессы приостановлены, контейнер не удаляется.
</details>

---

## Образы и слои

<details>
<summary>В каком виде хранятся образы? Что такое overlayfs?</summary>

Слои (layers) — каждая инструкция Dockerfile создаёт слой. OverlayFS накладывает слои в единую ФС. Образ — логическая группировка слоёв + метаданные.
</details>

<details>
<summary>Какие команды порождают слои?</summary>

ADD, COPY, RUN. ENV, WORKDIR и др. меняют метаданные, но могут влиять на кэш.
</details>

<details>
<summary>Что за «dangling» образы в <code>docker images</code>?</summary>

Образы без тега (показаны как `<none>`). Появляются после пересборки или при промежуточных образах multi-stage build.
</details>

<details>
<summary>Что такое Docker squash?</summary>

Объединение всех слоёв в один. Уменьшает число слоёв и размер образа. `docker build --squash`.
</details>

<details>
<summary>Как уменьшить размер образа? Много COPY, RUN</summary>

Alpine/minimal base; объединять RUN; multi-stage build; не ставить лишние пакеты; чистить кэш (`rm -rf /var/cache/apt`); копировать только нужное.
</details>

<details>
<summary>Разница между ADD и COPY?</summary>

**COPY** — простое копирование. **ADD** — может распаковывать архивы, скачивать по URL. Для файлов предпочтительнее COPY.
</details>

---

## Изоляция (namespaces, cgroups)

<details>
<summary>Как в Docker реализована изоляция? Какие средства Linux?</summary>

**Namespaces**: pid, net, ipc, mnt, uts — изоляция процессов, сети, ФС и т.д. **cgroups** — ограничение ресурсов (CPU, память, I/O).
</details>

<details>
<summary>Почему в контейнере видны только свои процессы?</summary>

PID namespace — контейнер имеет своё дерево процессов. PID 1 в контейнере — его init, а не хост-systemd.
</details>

<details>
<summary>Можно ли ограничить ресурсы (CPU, RAM, I/O) контейнера? Как?</summary>

Да. `--cpus`, `--memory`, `--memory-swap`, `--blkio-weight` и т.д. Реализовано через cgroups.
</details>

---

## Dockerfile

<details>
<summary>Что происходит при ENTRYPOINT?</summary>

Команда, которая всегда выполняется при запуске контейнера. Аргументы CMD или `docker run` передаются в неё как параметры.
</details>

<details>
<summary>Отличие CMD от ENTRYPOINT</summary>

**CMD** — команда по умолчанию, переопределяется аргументами `docker run`. **ENTRYPOINT** — «точка входа», аргументы run дополняют, а не заменяют. CMD подставляется после ENTRYPOINT.
</details>

---

## Хранение и сеть

<details>
<summary>В /var/lib/docker/ — как понять, какая папка к какому контейнеру?</summary>

`docker inspect` + `GraphDriver.Data.MergedDir` или `docker inspect $(docker ps -qa) | jq -r '...'`
</details>

<details>
<summary>Сетевое взаимодействие между контейнерами — как настроить?</summary>

Создать сеть `docker network create`, подключить контейнеры к ней. Они могут обращаться друг к другу по имени (внутренний DNS Docker).
</details>

---

## Docker Compose

<details>
<summary>Для чего применяется docker-compose?</summary>

Оркестрация нескольких контейнеров: единый конфиг, общие сети, volumes, переменные окружения. Удобно для dev/stage.
</details>

---

## Troubleshooting

<details>
<summary>Контейнер при запуске выдаёт <code>/bin/bash not found</code>. Как диагностировать?</summary>

Образ на Alpine или scratch — там может не быть bash. Использовать `sh` или добавить bash в образ. Проверить `docker run -it image sh`.
</details>

---

## Ссылки

- [[Git]] | [[Linux]] | [[Networks]] | [[IaC]] | [[CI-CD]] | [[Monitoring]]
- [[README]]
