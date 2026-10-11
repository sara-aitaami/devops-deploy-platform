# Diagrammes d’architecture — DevOps Deploy Platform

Ce document présente trois vues complémentaires de la plateforme :
l'architecture générale, le pipeline CI/CD et le runtime Kubernetes
avec ses composants de supervision.

Les diagrammes utilisent Mermaid afin de rester modifiables et versionnés
avec le code source. Ils peuvent être visualisés dans l'aperçu Markdown
de VS Code et directement sur GitHub.

---

## 1. Architecture générale

Cette vue présente le parcours du code jusqu'à l'application déployée,
ainsi que les composants Terraform et la supervision.

```mermaid
flowchart TB
    DEV["Développement local<br/>WSL"] --> GIT["Dépôt GitHub"]
    GIT --> ACTIONS["GitHub Actions"]

    ACTIONS --> TESTS["Tests pytest<br/>PostgreSQL de test"]
    ACTIONS --> BUILD["Build Docker"]
    ACTIONS --> KUBEVAL["Validation Kubeconform"]
    ACTIONS --> TFVAL["Validation Terraform"]

    BUILD --> TRIVY["Scan Trivy"]
    TESTS --> GATE{"Push sur main ?"}
    TRIVY --> GATE
    KUBEVAL --> GATE
    TFVAL --> GATE

    GATE -->|Oui| GHCR["GitHub Container Registry"]
    GATE -->|Non| PR["Contrôles sans publication"]

    GHCR -. "Image disponible pour un déploiement manuel" .-> K8S["Kubernetes local<br/>Docker Desktop"]

    WSL["Terraform depuis WSL"] -->|"Namespace devops,<br/>ConfigMap terraform-info,<br/>Service devops-api"| K8S
    WSL <-->|"State distant"| HCP["HCP Terraform"]

    K8S --> API["FastAPI"]
    K8S --> DB["PostgreSQL"]
    API -->|"Connexion SQL"| DB
    DB --> PVC[("Volume persistant")]

    API -->|"Métriques HTTP"| PROM["Prometheus"]
    EXP["postgres_exporter"] -->|"Métriques PostgreSQL"| PROM
    PROM --> GRAF["Grafana"]
    GRAF --> ALERT["Grafana Alerting<br/>Webhook"]
```

**À retenir :**

- Les Pull Requests exécutent les contrôles sans publier d'image sur GHCR.
- La publication sur GHCR est conditionnée à un push sur main.
- Le déploiement Kubernetes est réalisé manuellement avec kubectl.
- Terraform est exécuté depuis WSL et utilise HCP Terraform pour conserver son state distant.

---

## 2. Pipeline CI/CD

Ce diagramme détaille les principales étapes du workflow GitHub Actions.

```mermaid
flowchart TD
    EVENT["Push ou Pull Request"] --> WF["GitHub Actions"]

    WF --> TEST["Tests backend<br/>pytest et PostgreSQL de test"]
    WF --> BUILD["Build de l'image Docker"]
    WF --> KUBE["Validation Kubeconform"]
    WF --> TF["Validation Terraform"]

    BUILD --> TRIVY["Scan Trivy<br/>Vulnérabilités HIGH et CRITICAL"]

    TEST --> GATE{"Tous les contrôles requis réussissent ?"}
    TRIVY --> GATE
    KUBE --> GATE
    TF --> GATE

    GATE -->|Non| FAIL["Workflow en échec"]
    GATE -->|Oui| EVENTTYPE{"Push sur main ?"}

    EVENTTYPE -->|Oui| PUBLISH["Publication GHCR"]
    EVENTTYPE -->|Non| NO_PUBLISH["Aucune publication GHCR"]
```

**Règles du pipeline :**

- Les Pull Requests exécutent les contrôles sans publier d'image.
- Les pushes sur `main` peuvent publier l'image après les contrôles requis.
- Kubeconform valide les manifests sans nécessiter un accès au cluster local.
- Terraform valide la configuration dans la CI ; le workflow ne déploie pas les ressources Terraform dans le cluster.

---

## 3. Runtime Kubernetes et observabilité

Cette vue décrit les composants de l'application, les contrôles de sécurité
et la collecte des métriques.

```mermaid
flowchart TB
    subgraph APP["Namespace Kubernetes : devops"]
        USER["Accès client"]
        SVC["Service devops-api<br/>Port 8000 · NodePort 30080"]
        API["Pod FastAPI<br/>UID 10001"]
        CONFIG["ConfigMap"]
        SECRET["Secrets Kubernetes<br/>secretKeyRef"]
        SA["ServiceAccount devops-api<br/>Token non monté automatiquement"]
        SEC["Contrôles de sécurité<br/>Non-root · seccomp RuntimeDefault<br/>Capacités supprimées<br/>Filesystem racine en lecture seule<br/>allowPrivilegeEscalation false"]
        PGSVC["Service postgres"]
        PG["Pod PostgreSQL"]
        PVC[("PersistentVolumeClaim")]

        USER --> SVC
        SVC --> API
        CONFIG --> API
        SECRET --> API
        SA -. "Identité Kubernetes" .-> API
        SEC -. "SecurityContext" .-> API
        API -->|"Connexion SQL"| PGSVC
        PGSVC --> PG
        PG --> PVC
    end

    subgraph OBS["Observabilité"]
        SMAPI["ServiceMonitor API"]
        SMDB["ServiceMonitor exporter"]
        PROM["Prometheus"]
        EXP["postgres_exporter"]
        GRAF["Grafana"]
        ALERT["Règles Grafana Alerting"]
        WEBHOOK["Contact point Webhook"]

        SMAPI -. "Découverte de la cible" .-> PROM
        SMDB -. "Découverte de la cible" .-> PROM
        PROM -->|"Scrape /metrics"| API
        PROM -->|"Scrape des métriques"| EXP
        EXP -->|"Collecte PostgreSQL"| PG
        PROM --> GRAF
        GRAF --> ALERT
        ALERT --> WEBHOOK
    end
```

**Contrôles de sécurité représentés :**

- L'API tourne sans privilèges root, avec l'UID `10001`.
- Le token du `ServiceAccount` n'est pas monté automatiquement.
- Le système de fichiers racine est en lecture seule.
- Les capacités Linux sont supprimées et l'escalade de privilèges est désactivée.
- PostgreSQL conserve ses données sur un volume persistant.
- Prometheus collecte les métriques des cibles configurées et Grafana les présente.