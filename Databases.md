# СУБД — MySQL, PostgreSQL

#devops #собес #databases

Источник: [Swfuse/devops-interview](https://github.com/Swfuse/devops-interview/blob/main/interview.md)

---

## MySQL

<details>
<summary>Что такое индексы, зачем нужны?</summary>

Индекс — структура для быстрого поиска (B-tree, hash). Ускоряет SELECT, замедляет INSERT/UPDATE/DELETE. Аналогия: каталог в библиотеке вместо поиска по всем полкам.
</details>

<details>
<summary>Проблема большого числа индексов?</summary>

- Медленнее запись (обновление всех индексов)
- Дороже хранение и обслуживание
- Неактуальная статистика → плохие планы запросов

Плохи не сами индексы, а неиспользуемые.
</details>

<details>
<summary>Как настроить master-slave репликацию в MySQL?</summary>

1. На master: `server-id`, `log_bin`, `binlog_do_db`
2. Пользователь для репликации: `GRANT REPLICATION SLAVE ON *.* TO 'slave_user'@'%'`
3. `mysqldump --lock-all-tables` на master, импорт на slave
4. На slave: `server-id`, `relay-log`, `CHANGE MASTER TO` (MASTER_HOST, MASTER_LOG_FILE, MASTER_LOG_POS)
5. `START SLAVE`, `SHOW SLAVE STATUS`
</details>

<details>
<summary>Разница между TRUNCATE, DELETE и DROP?</summary>

- **DROP** — удаляет таблицу целиком (структуру). DDL, необратимо.
- **DELETE** — удаляет строки, можно с WHERE. DML, откатывается. Медленнее.
- **TRUNCATE** — удаляет все строки, сбрасывает счётчики. DDL, быстрее DELETE. Не откатывается в некоторых СУБД. Блокирует таблицу.
</details>

<details>
<summary>Почему не использовать mysqldump на большой активной базе? Альтернативы?</summary>

Блокирует таблицы, нагрузка на диск и сеть. Альтернативы:
- `mysqldump --single-transaction` (InnoDB)
- `mysqldump --skip-lock-tables` (есть риск несогласованности)
- Percona XtraBackup, mariabackup — без блокировок
</details>

---

## PostgreSQL

<details>
<summary>Что такое роли в PostgreSQL?</summary>

Роль — пользователь или группа. Управляет доступом к объектам БД, владением объектами. Роль может быть членом другой роли (наследование прав). В PostgreSQL «пользователь» и «группа» — это роли с разными флагами.
</details>

<details>
<summary>Что такое WAL и зачем он нужен?</summary>

**WAL** (Write-Ahead Logging) — журнал, в который записываются изменения до записи в основные файлы данных. Нужен для:
- восстановления при сбоях
- репликации
- point-in-time recovery
</details>

---

## Общие темы

<details>
<summary>ACID — расшифровка</summary>

- **A**tomicity — транзакция либо целиком, либо нет
- **C**onsistency — переход из одного согласованного состояния в другое
- **I**solation — транзакции изолированы друг от друга
- **D**urability — зафиксированные изменения сохраняются
</details>

<details>
<summary>Как безопасно удалить или изменить миллион строк?</summary>

1. Разбить на порции (например, по 1000) с паузой
2. Выполнять в транзакциях с лимитами
3. Делать в низкопиковое время
4. Предварительно делать бэкап
</details>
