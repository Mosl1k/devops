# Linux — вопросы для собеседований

#devops #собес #linux

---

## Основы

<details>
<summary>Что такое POSIX?</summary>

Стандарт интерфейса для Unix-подобных ОС. Определяет API для работы с процессами, файлами, сокетами. Облегчает переносимость программ между Linux, macOS, BSD.
</details>

<details>
<summary>Что такое уровни выполнения (runlevels)?</summary>

Уровень 0 — выключение; 1 — single-user; 2 — multi-user без NFS; 3 — multi-user с сетью; 5 — графический режим; 6 — перезагрузка. В systemd заменены на targets.
</details>

<details>
<summary>Какие основные части включает система на базе дистрибутива Linux?</summary>

GRUB (загрузчик), ядро, init/systemd, демоны, shell, утилиты, при необходимости X/DE. Ядро управляет железом, init — сервисами.
</details>

<details>
<summary>Что такое BIOS, UEFI? Основы и различия</summary>

**BIOS** — устаревшая прошивка, MBR, диск до 2.1 ТБ, 16-бит. **UEFI** — современный стандарт, GPT, Secure Boot, 64-bit, быстрее, поддержка сети.
</details>

<details>
<summary>Что такое PXE? Как загрузиться по сети?</summary>

PXE — загрузка по сети. Сетевая карта запрашивает образ с TFTP-сервера. В BIOS включить LAN Boot. Полезно для массовой установки ОС.
</details>

<details>
<summary>Что такое ядро, initramfs, загрузчик?</summary>

**Ядро** — низкоуровневый код, работа с железом. **initramfs** — временная ФС в RAM до монтирования root. **Загрузчик** (GRUB) — выбор и загрузка ядра.
</details>

---

## Система инициализации

<details>
<summary>Зачем нужна система инициализации? Какие системы используются? (systemd, init…)</summary>

Нужна для монтирования ФС, запуска сервисов, перехода в нужный режим. Варианты: SysV init, systemd, Upstart, OpenRC.
</details>

<details>
<summary>Что такое systemd и init? В чём преимущество systemd?</summary>

Оба — системы инициализации. systemd даёт: параллельный запуск, unit-файлы вместо длинных bash-скриптов, автоперезапуск, journald, меньше разбросанных конфигов.
</details>

<details>
<summary>Как понять, используется ли в системе systemd?</summary>

`stat /sbin/init` — должен быть симлинк на systemd. Или `ls /run/systemd/`, `readlink /proc/1/exe`.
</details>

---

## Процессы

<details>
<summary>Что происходит (с точки зрения процессов) при выполнении команды в консоли, например <code>ls -l</code>?</summary>

fork() → создаётся дочерний процесс; exec() → выполняется ls; wait() — shell ждёт; при завершении дочерний шлёт SIGCHLD.
</details>
<details>
<summary>Что такое процесс? Что такое тред? В чём главные отличия?</summary>

**Процесс** — экземпляр программы, своё адресное пространство. **Тред** — поток внутри процесса, общая память. Процессы изолированы, треды делят память.
</details>

<details>
<summary>Где в Linux хранится информация о процессах?</summary>

В виртуальной ФС `/proc` — подкаталоги по PID, файлы `/proc/self`, `/proc/1/exe`, и т.д.
</details>

<details>
<summary>Что означает каждая запись в выводе <code>top</code>?</summary>

PID, USER, %CPU, %MEM, TIME, COMMAND… Load average — средние за 1, 5, 15 мин. S — статус (R/S/D/Z и т.д.).
</details>

<details>
<summary>Что показывает статус процессов? Какие статусы есть в Linux?</summary>

R — running, S — sleeping, D — uninterruptible sleep, Z — zombie, T — stopped. См. `ps` или `top`.
</details>

<details>
<summary>Что такое зомби-процесс? Как его создать?</summary>

Процесс завершён, но родитель не сделал wait(). Родитель создаёт дочерний, тот exit(), родитель не вызывает wait() — дочерний становится зомби.
</details>

<details>
<summary>Чем опасны зомби-процессы?</summary>

Занимают slot в таблице процессов (ограниченный ресурс). Много зомби = «out of processes», нельзя создать новые.
</details>

---

## Сигналы

<details>
<summary>Что делает команда <code>kill</code>?</summary>

Отправляет процессу сигнал (по умолчанию SIGTERM). `kill -9` — SIGKILL, нельзя перехватить.
</details>
<details>
<summary>Для чего нужны сигналы? Какие чаще всего? (5–10)</summary>

Управление процессами: завершение, пауза, возобновление. SIGTERM(15), SIGKILL(9), SIGINT(2/Ctrl+C), SIGSTOP, SIGCHLD, SIGHUP…
</details>

<details>
<summary>Чем отличается SIGTERM от SIGKILL?</summary>

SIGTERM можно перехватить и корректно завершить. SIGKILL нельзя перехватить — ядро убивает процесс принудительно.
</details>

<details>
<summary>Какой сигнал при Ctrl+C?</summary>

SIGINT (2). Отправляется foreground-процессу терминалом.
</details>

---

## Load Average

<details>
<summary>Что такое Load Average? В каких единицах?</summary>

Средняя загрузка (процессы в R+D) за 1, 5 и 15 минут. «Единицей» считается одно ядро CPU.
</details>
<details>
<summary>LA = 900, 900, 900, сервер почти нормально работает. Нормально ли это?</summary>

ДА. На многоядерных машинах LA может быть > 1 на ядро. 900 при сотнях ядер — нормально. Смотреть на утилизацию CPU и наличие проблем.
</details>

<details>
<summary>Почему load average состоит из трёх значений?</summary>

Средние за 1, 5 и 15 минут. Показывают краткосрочную и долгосрочную нагрузку.
</details>

---

## Память

<details>
<summary>Что такое физическая память?</summary>

Оперативная память (RAM). Адресуется напрямую процессором.
</details>
<details>
<summary>Что такое виртуальная память?</summary>

Абстракция: каждый процесс видит своё адресное пространство. Ядро мапит виртуальные адреса на физическую RAM/swap.
</details>

<details>
<summary>Где посмотреть потребление памяти?</summary>

`free -h`, `cat /proc/meminfo`, `htop`.
</details>

<details>
<summary>Как работает OOM Killer?</summary>

При нехватке памяти ядро выбирает процесс (по oom_score) и убивает его, чтобы освободить RAM.
</details>

<details>
<summary>Что такое buffer/cache память?</summary>

Буферы — метаданные, кэш — данные с диска. Могут быть освобождены при необходимости (reclaimable).
</details>

---

## Kernel space / Userspace

<details>
<summary>Что такое userspace и kernelspace? Чем отличаются?</summary>

**Userspace** — код приложений, ограниченный доступ. **Kernelspace** — код ядра, полный доступ к железу. Обмен через системные вызовы.
</details>
<details>
<summary>Что такое системные вызовы? Зачем нужны? Какие знаешь? (5–10)</summary>

Интерфейс userspace → kernel. read, write, open, close, fork, exec, mmap, brk… Документация: `man 2 syscalls`, `strace`.
</details>

---

## Файлы и дескрипторы

<details>
<summary>Что такое файловый дескриптор?</summary>

Целое число — handle на открытый файл, сокет, pipe. 0=stdin, 1=stdout, 2=stderr.
</details>
<details>
<summary>Как посмотреть время последней модификации файла?</summary>

`stat файл` или `stat --format=%y файл`
</details>

<details>
<summary>Что такое inode?</summary>

Структура на диске: метаданные файла (права, размер, указатели на блоки). Имена хранятся в каталогах, ссылаются на inode.
</details>

<details>
<summary>Hard link vs soft link (symlink)</summary>

**Hard link** — ещё одно имя того же inode, нельзя на каталоги/другой раздел. **Symlink** — отдельный файл с путём к цели.
</details>

<details>
<summary>Как удалить файл с именем <code>-rf</code>?</summary>

`rm -- -rf` или `rm ./-rf`
</details>

---

## Диски и RAID

<details>
<summary>Как посмотреть нагрузку на диски?</summary>

`iostat -x`, `iotop`, `dstat`, `vmstat`
</details>
<details>
<summary>Что такое RAID? Какие массивы бывают?</summary>

RAID 0 — striping, RAID 1 — mirror, RAID 5 — parity, RAID 6 — два parity. RAID 6 выдерживает отказ 2 дисков.
</details>

---

## Bash и переменные

<details>
<summary>Разница между <code>export VAR="VALUE"</code> и <code>VAR="VALUE"</code>?</summary>

С export переменная наследуется дочерними процессами. Без export — только в текущем shell.
</details>
<details>
<summary>Что значит <code>$@</code> в bash?</summary>

Все аргументы скрипта как отдельные строки. Есть ещё `$?` — код возврата, `$!` — PID последнего фонового процесса, `$$` — PID текущего shell.
</details>

<details>
<summary>Как вывести только STDERR, игнорируя STDOUT?</summary>

`cmd 2>&1 >/dev/null | grep pattern` или `cmd 2>/dev/stderr` в зависимости от задачи.
</details>
<details>
<summary>Как остановить скрипт при ошибке? Что значит <code>set -euo pipefail</code>?</summary>

`set -e` — выход при ненулевом коде, `-u` — ошибка при обращении к необъявленной переменной, `-o pipefail` — ошибка в пайпе приводит к выходу.
</details>

<details>
<summary><code>a=5; (true && a=10;)</code> — чему равно a?</summary>

5. Подоболочка `( )` — отдельный процесс, изменения не видны родителю.
</details>
---

## sudo и аутентификация

<details>
<summary>Как работает sudo? Для чего используется?</summary>

Запуск команды от другого пользователя (по умолчанию root). Читает /etc/sudoers. `sudo -u user cmd`.
</details>
---

## Файловая система

<details>
<summary>Где информация о смонтированных ФС?</summary>

`/proc/mounts`, `mount`, `findmnt`, `/etc/mtab`
</details>

---

## Взаимодействие процессов и виртуализация

<details>
<summary>Как процессы взаимодействуют?</summary>

Сокеты, pipes, FIFO, shared memory, сигналы, файлы.
</details>
<details>
<summary>Что такое QEMU? KVM? qemu-kvm?</summary>

**QEMU** — эмулятор/виртуализатор. **KVM** — модуль ядра для аппаратной виртуализации. **qemu-kvm** — QEMU с акселерацией через KVM.
</details>

---

## iowait

<details>
<summary>Что такое iowait и почему он появляется?</summary>

Процент времени CPU в ожидании завершения I/O (диск, сеть). Высокий iowait — CPU простаивает, пока ждёт диск.
</details>

---

## Ссылки

- [[Git]] — связанная тема
- [[README]] — оглавление
