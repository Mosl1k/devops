# Debug — диагностика и troubleshooting

#devops #собес #debug

Источник: [Swfuse/devops-interview](https://github.com/Swfuse/devops-interview/blob/main/interview.md)

---

<details>
<summary>Веб-сервер отдаёт 502 Bad Gateway. Как найти причину?</summary>

502 = вышестоящий сервер вернул некорректный ответ. Проверить:
- конфиги nginx (proxy_pass, логи)
- логи upstream-приложения (Apache, PHP-FPM и т.д.)
- доступность и статус backend-сервиса

`access_log` и `error_log` с уровнем `info` для деталей.
</details>

<details>
<summary>Файл с нечитаемым содержимым — как узнать формат и назначение?</summary>

`file <путь>`
`file -i -b <путь>` — MIME-тип.
</details>

<details>
<summary>Запуск исполняемого файла даёт «no such file or directory». Почему?</summary>

Возможные причины:
- 32-битный бинарник без нужных библиотек
- Файл — битая символическая ссылка
- Отсутствует интерпретатор (для скриптов)
- Несовпадение архитектуры (arm vs amd64)
</details>

<details>
<summary>Программа не находит конфиг. Как узнать, где ищет?</summary>

`strace -f <команда> 2>&1 | grep open` — видно какие файлы открываются.
Либо verbose-режим: `-vvv`, `--verbose --help`.
</details>

<details>
<summary>У chmod отняли права на исполнение (chmod -x chmod). Что делать?</summary>

Варианты:
1. `setfacl -m u::rwx,g::rx,o::x /usr/bin/chmod`
2. Запуск через динамический компоновщик: `/usr/lib64/ld-linux-x86-64.so.2 /usr/bin/chmod +x /usr/bin/chmod`
3. Скопировать исполняемые права: `cp --attributes-only /usr/bin/ls ./new_chmod; cat /usr/bin/chmod > ./new_chmod; ./new_chmod +x /usr/bin/chmod`
4. `install -m 755 /usr/bin/chmod ./new_chmod` и затем `./new_chmod +x /usr/bin/chmod`
</details>

<details>
<summary>База упирается в диск, сервер менять нельзя. Как ускорить?</summary>

Рискованно: отключить fsync — данные будут писаться асинхронно в буфер, при сбое возможна потеря. Только как временная мера в нереплицируемой среде.
</details>

<details>
<summary>df показывает 20 ГБ занято, du — 20 МБ. Почему?</summary>

Удалённый файл, но процесс его всё ещё держит открытым. Место освободится только после завершения процесса.

Найти: `lsof -a +L1 | grep <путь>` или `lsof | grep deleted`
</details>

<details>
<summary>no space left on device, df — место есть, root пишет. Почему?</summary>

Квоты пользователя. `quota -v <user>`, проверить `/etc/fstab` (usrquota, grpquota), `repquota`.
</details>

<details>
<summary>Почему available (2919) больше, чем free (843)?</summary>

`free` — полностью свободная память. `available` — сколько можно использовать под новые приложения, с учётом рекуперируемого cache и buffers. Кэш можно освободить, если понадобится.
</details>

<details>
<summary>Сервер тормозит (Cassandra, ELK). Сняли нагрузку — всё ещё медленно. Как искать причину?</summary>

1. `top` — высокий sys time, systemd жрёт CPU
2. `strace -c -p 1` — смотреть, какие syscall'ы
3. `watch -n 1 ps --ppid 1` — кто постоянно форкается
4. Искать подозрительные процессы (a.out, a.sh и т.п.), кроны, systemd timers
</details>

<details>
<summary>Бинарник падает сразу, файловые дескрипторы пустые. Как искать причину?</summary>

`strace ./binary 2>out.txt` — смотреть syscalls, например `open()` на несуществующий файл, segfault после.
</details>
