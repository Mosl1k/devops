# Networks — вопросы для собеседований

#devops #собес #networks #сети

---

## IP и основы

<details>
<summary>Что такое IP и маска подсети?</summary>

IP — числовой идентификатор узла в сети TCP/IP. Маска определяет, какая часть — сеть, какая — хост. Нужна для маршрутизации.
</details>

<details>
<summary>Что такое 127.0.0.1? Зачем нужен?</summary>

Loopback-адрес. Пакеты на 127.0.0.0/8 не покидают хост — возвращаются обратно. Используется для локальных сервисов.
</details>

<details>
<summary>Что такое 10.0.0.0/8, 192.168.0.0/16, 172.16.0.0/12?</summary>

Приватные подсети (RFC 1918). Не маршрутизируются в интернете. Используются в локальных сетях.
</details>

---

## TCP и UDP

<details>
<summary>Чем отличается TCP от UDP?</summary>

**TCP** — с установкой соединения, гарантия доставки, порядок, retransmit. **UDP** — без соединения, без гарантий. Лучше зависит от задачи: TCP — надёжность, UDP — скорость/стриминг.
</details>

<details>
<summary>Как TCP устанавливает соединение? (three-way handshake)</summary>

1. Клиент → SYN. 2. Сервер → SYN+ACK. 3. Клиент → ACK. После этого ESTABLISHED.
</details>

<details>
<summary>На каком уровне OSI работает TCP?</summary>

Транспортный (L4).
</details>

<details>
<summary>Почему DNS использует UDP?</summary>

Маленькие запросы/ответы. UDP быстрее — нет handshake. Если ответ не влезает в UDP — TC-флаг, повтор по TCP.
</details>

---

## URL и браузер

<details>
<summary>Что происходит при вводе yandex.ru в браузере?</summary>

1. Протокол (HSTS → HTTPS). 2. DNS: кэш браузера → hosts → ОС → роутер → провайдер → корневые NS → TLD → авторитативный NS. 3. TCP + TLS handshake. 4. HTTP-запрос (GET, Host, …). 5. Ответ, рендер.
</details>

---

## HTTP / HTTPS

<details>
<summary>Какие стандартные коды ответов веб-серверов?</summary>

2xx — успех; 3xx — редирект; 4xx — клиентская ошибка (404, 403); 5xx — серверная ошибка (502, 503).
</details>

<details>
<summary>Основные типы HTTP-запросов</summary>

GET, POST, PUT, PATCH, DELETE, HEAD, OPTIONS.
</details>

<details>
<summary>Что такое TLS и SSL?</summary>

Протоколы шифрования трафика. TLS — преемник SSL. Используются для HTTPS.
</details>

<details>
<summary>Симметричное vs асимметричное шифрование</summary>

**Симметричное** — один ключ для шифрования и расшифровки. **Асимметричное** — пара ключей: публичный шифрует, приватный расшифровывает.
</details>

<details>
<summary>Как работают сертификаты? Подтверждение HTTPS</summary>

Сервер отдаёт сертификат (подписан CA). Клиент проверяет подпись по списку доверенных CA. Далее — обмен ключами, симметричное шифрование сессии.
</details>

<details>
<summary>Что такое SNI?</summary>

Server Name Indification — расширение TLS. Позволяет на одном IP держать несколько HTTPS-сайтов (разные сертификаты).
</details>

---

## DNS

<details>
<summary>Как работает DNS? Зачем нужен?</summary>

Сопоставляет домены и IP. Иерархия: корневые → TLD → авторитативные NS. Нужен, чтобы не запоминать IP.
</details>

<details>
<summary>Какие DNS-записи бывают?</summary>

A, AAAA, CNAME, NS, MX, TXT, PTR, SOA, TTL. DKIM/DMARC — для почты.
</details>

<details>
<summary>Что такое authority в DNS?</summary>

Авторитативный сервер — хранит «источник правды» для зоны домена.
</details>

<details>
<summary>Рекурсивный vs нерекурсивный запрос</summary>

Рекурсивный — сервер сам ходит по цепочке до ответа. Нерекурсивный — возвращает ссылку на следующий сервер.
</details>

---

## ARP и сети

<details>
<summary>Что такое и зачем нужен ARP?</summary>

Address Resolution Protocol — сопоставление IP и MAC в L2. Широковещательный запрос «у кого IP X?», ответ «у меня, MAC Y».
</details>

<details>
<summary>Зачем нужен VLAN?</summary>

Логическое разделение L2-сети. Изоляция трафика, ограничение broadcast. Несколько сетей на одном физическом порту.
</details>

<details>
<summary>Как работает NAT? Зачем нужен?</summary>

Преобразование приватных IP в публичные. Несколько хостов за одним внешним IP. Сохранение пула публичных адресов.
</details>

<details>
<summary>На каком порту работает ping?</summary>

Ни на каком. Ping — ICMP (сетевой уровень), портов нет. Исключение — traceroute может использовать UDP.
</details>

---

## SSH

<details>
<summary>Как устанавливается SSH и авторизация по паролю и ключам?</summary>

**Пароль** — шифрованный канал, пароль передаётся по нему. **Ключи** — клиент отправляет подпись, сервер проверяет по публичному ключу. Публичный ключ шифрует, приватный расшифровывает.
</details>

<details>
<summary>На каком уровне OSI работает SSH?</summary>

Прикладной (L7). Транспорт — TCP.
</details>

---

## Ссылки

- [[Git]] | [[Linux]] | [[Containers]] | [[IaC]] | [[CI-CD]] | [[Monitoring]]
- [[README]]
