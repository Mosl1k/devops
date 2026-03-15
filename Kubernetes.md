# Kubernetes — вопросы для собеседований

#devops #собес #kubernetes

Источник: [Swfuse/devops-interview](https://github.com/Swfuse/devops-interview/blob/main/interview.md)

---

## Основы

<details>
<summary>Что такое Kubernetes?</summary>

Система оркестрации контейнеров. Управляет запуском, масштабированием, балансировкой контейнеров на множестве узлов.
</details>

<details>
<summary>Какую проблему решает Kubernetes?</summary>

Масштабирование контейнеров на множество хостов, балансировка, самоизлечение, декларативное описание желаемого состояния. Service discovery, логирование, CI/CD.
</details>

<details>
<summary>Что такое minikube?</summary>

Локальный кластер Kubernetes для разработки и экспериментов.
</details>

<details>
<summary>Опиши архитектуру Kubernetes-кластера.</summary>

**Control plane:** API server, etcd, scheduler, controller-manager. **Worker nodes:** kubelet, kube-proxy, container runtime (CRI). Для отказоустойчивости — несколько master-нод, нечётное число для кворума.
</details>

<details>
<summary>Что такое Pod?</summary>

Минимальная единица деплоя. Один или несколько контейнеров, общий network namespace, volumes. Pod получает IP в кластере.
</details>

<details>
<summary>Разница между Pod и контейнером?</summary>

Pod — обёртка; внутри — один или несколько контейнеров. Pod — единица планирования и размещения.
</details>

<details>
<summary>Может ли Pod запуститься на двух разных нодах?</summary>

Нет. Pod всегда размещается на одной ноде.
</details>

---

## Рабочие нагрузки

<details>
<summary>Deployment vs ReplicaSet vs StatefulSet</summary>

- **ReplicaSet** — поддерживает заданное число подов
- **Deployment** — управляет ReplicaSet, rolling update, rollback
- **StatefulSet** — stateful-приложения, стабильные имена, отдельный PVC на под
</details>

<details>
<summary>Что такое Service? Типы.</summary>

Абстракция доступа к подам. Типы: ClusterIP (внутри кластера), NodePort, LoadBalancer, ExternalName. Держит стабильный ClusterIP, маршрутизирует на эндпоинты (поды).
</details>

<details>
<summary>Что такое Ingress?</summary>

Правила входящего HTTP/HTTPS-трафика. Маршрутизация по host/path на сервисы. Нужен Ingress Controller (nginx, traefik).
</details>

<details>
<summary>Readiness, Liveness, Startup — в чём отличие?</summary>

- **Liveness** — жив ли контейнер; при fail — перезапуск
- **Readiness** — готов ли принимать трафик; при fail — убирается из endpoints
- **Startup** — первичная готовность; пока не пройдена — liveness/readiness не проверяются
</details>

<details>
<summary>Job vs CronJob</summary>

Job — одноразовая задача. CronJob — Job по расписанию (cron).
</details>

---

## Хранение и конфигурация

<details>
<summary>ConfigMap и Secret — для чего?</summary>

ConfigMap — некритичные настройки (ключ-значение). Secret — пароли, токены. Могут монтироваться как env или volumes.
</details>

<details>
<summary>PersistentVolume и PersistentVolumeClaim</summary>

PV — кусок хранилища. PVC — запрос под него (размер, access mode). StorageClass — динамическое создание PV.
</details>

---

## Размещение и лимиты

<details>
<summary>Requests и Limits. QoS-классы.</summary>

Requests — зарезервировано для пода. Limits — максимум. QoS: Guaranteed (limits=requests), Burstable (limits>requests), BestEffort (не заданы). При нехватке ресурсов BestEffort утилизируется первым.
</details>

<details>
<summary>Что будет при превышении лимита памяти/CPU?</summary>

Память — OOMKill. CPU — throttling (CFS), падение проб, возможные рестарты.
</details>

<details>
<summary>DaemonSet — зачем?</summary>

По одному поду на каждую ноду. Сбор логов, мониторинг, сетевые плагины (CNI).
</details>

<details>
<summary>Taints и Tolerations</summary>

Taint — «запрет» размещения подов на ноде. Toleration — разрешение поду быть на этой ноде. NoSchedule, PreferNoSchedule, NoExecute.
</details>

<details>
<summary>Что такое оператор?</summary>

Расширение Kubernetes. Следит за кастомными ресурсами (CRD), управляет состоянием сложных приложений (БД, очереди).
</details>

---

## Сеть и безопасность

<details>
<summary>Через что реализованы сети в Kubernetes?</summary>

CNI-плагины: Calico, Flannel, Cilium. Выдают IP подам, маршрутизация между нодами (BGP или overlay). kube-proxy — iptables/IPVS для Service.
</details>

<details>
<summary>RBAC. Role vs ClusterRole?</summary>

RBAC — права доступа по ролям. Role — в рамках namespace. ClusterRole — кластер-широкий или доступ к кластерным ресурсам (nodes).
</details>

---

## Прочее

<details>
<summary>CRI, CSI, CNI — что это?</summary>

- **CRI** — интерфейс контейнерной среды (containerd, CRI-O)
- **CSI** — интерфейс хранилища
- **CNI** — интерфейс сети
</details>

<details>
<summary>Что такое Helm?</summary>

Пакетный менеджер для Kubernetes. Шаблоны (charts), переменные, зависимости, версионирование.
</details>
