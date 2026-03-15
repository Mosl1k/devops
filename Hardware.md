# Железо — вопросы для собеседований

#devops #собес #hardware

Источник: [Swfuse/devops-interview](https://github.com/Swfuse/devops-interview/blob/main/interview.md)

---

## Доступ к серверу

<details>
<summary>Сервер не отвечает, как получить доступ к нему, не находясь в ЦОДе?</summary>

Через **IPMI** или **KVM over IP**, если они есть на сервере. Иначе — звонить дежурному инженеру ЦОДа.
</details>

<details>
<summary>Что такое KVM (не гипервизор)? Как его использовать?</summary>

**KVM over IP** — устройство для передачи видеосигнала и ввода с мыши/клавиатуры по сети. Позволяет перезагрузить сервер, зайти в BIOS. Работает независимо от ОС. Аббревиатура: Keyboard, Video, Mouse. Используется как последнее средство при сбое.
</details>

<details>
<summary>Что такое IPMI? Какие подсистемы включает?</summary>

**IPMI** (Intelligent Platform Management Interface) — интерфейс удалённого мониторинга и управления сервером. Модуль BMC (Board Management Controller) — отдельный контроллер на плате.

Подсистемы: доступ к консоли и BIOS; питание (вкл/выкл/перезагрузка); датчики (температура, напряжение, вентиляторы); подключение ISO-образов. BMC общается по шине IPMB (I2C).
</details>

<details>
<summary>Какие преимущества IPMI по сравнению с KVM?</summary>

IP-KVM: только консоль, нужен запрос в техподдержку, нет управления питанием и образами. **IPMI** даёт постоянный удалённый доступ, управление питанием, монтирование образов, мониторинг датчиков.
</details>

---

## Просмотр информации о железе

<details>
<summary>Как узнать модель процессора, число ядер, инструкции, режим работы?</summary>

- Модель: `cat /proc/cpuinfo`, `lscpu`
- Физические/логические ядра: `grep "cpu cores" /proc/cpuinfo`, `grep -c processor`
- Режим работы (governor): `cat /sys/devices/system/cpu/cpu*/cpufreq/scaling_governor` — powersave, ondemand, performance
- Инструкции: `lscpu` (Flags)
</details>

<details>
<summary>Как посмотреть типы памяти, модель материнки, версию BIOS?</summary>

`dmidecode --type memory`, `dmidecode --type baseboard`, `dmidecode --type BIOS`
</details>

<details>
<summary>Как посмотреть датчики напряжения, температуры, обороты вентиляторов?</summary>

`sensors` (lm-sensors). Для серверов — `ipmicfg -pminfo` или аналогичные IPMI-утилиты.
</details>

<details>
<summary>Как узнать тип сетевого адаптера и состояние интерфейсов?</summary>

`lspci | grep net`, `lshw -class network -short`, `ip a`, `ip link show`
</details>

<details>
<summary>Как посмотреть USB и PCI устройства?</summary>

`lspci`, `lsusb` (опционально `-vvv` для деталей)
</details>
