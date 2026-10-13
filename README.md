# DevOps Deploy Platform

Plateforme DevOps de portfolio reproduisant progressivement une chaîne de déploiement moderne autour de **FastAPI, PostgreSQL, Docker, GitHub Actions, Kubernetes, Terraform, Prometheus, Grafana et Trivy**.

Le projet est construit par étapes afin de comprendre chaque couche avant de l'intégrer dans une chaîne complète : développement, tests, conteneurisation, CI/CD, orchestration, Infrastructure as Code, observabilité et sécurité.

---

## Présentation

**DevOps Deploy Platform** est un projet de portfolio réalisé dans une démarche orientée **automatisation, fiabilité, observabilité et sécurité**.

L'objectif est de démontrer la capacité à construire et sécuriser une petite plateforme applicative de bout en bout, depuis le code jusqu'au runtime Kubernetes.

Le projet est exécuté localement dans **WSL** avec **Docker Desktop et Kubernetes**, tandis que le state Terraform est conservé à distance dans **HCP Terraform**.

---

## Objectif portfolio

Ce dépôt a vocation à servir de projet de portfolio pour illustrer une démarche DevOps complète :

```text
Développer
   ↓
Tester
   ↓
Conteneuriser
   ↓
Automatiser
   ↓
Déployer
   ↓
Observer
   ↓
Sécuriser
```

L'intérêt du projet réside autant dans les technologies utilisées que dans la progression vers une chaîne cohérente, automatisée et sécurisée.

---

## Compétences démontrées

Ce projet met en pratique :

- Linux et environnement WSL
- Git et GitHub
- développement d'une API FastAPI
- PostgreSQL et SQLAlchemy
- Docker et Docker Compose
- CI/CD avec GitHub Actions
- GitHub Container Registry (GHCR)
- Kubernetes
- Infrastructure as Code avec Terraform
- HCP Terraform et gestion du state
- observabilité avec Prometheus et Grafana
- alerting avec Grafana Alerting
- analyse des vulnérabilités avec Trivy
- détection des secrets avec Gitleaks
- RBAC et principe du moindre privilège
- durcissement des conteneurs et du runtime Kubernetes

---

## Technologies

| Domaine | Technologies |
|---|---|
| Backend | FastAPI, Python, SQLAlchemy |
| Base de données | PostgreSQL |
| Conteneurisation | Docker, Docker Compose |
| CI/CD | GitHub Actions |
| Registry | GitHub Container Registry (GHCR) |
| Orchestration | Kubernetes |
| Infrastructure as Code | Terraform, HCP Terraform |
| Monitoring | Prometheus, Grafana, Alertmanager |
| Exporters / instrumentation | prometheus-fastapi-instrumentator, postgres_exporter |
| Sécurité | Trivy, Gitleaks, Kubernetes SecurityContext, RBAC |
| Validation | pytest, Kubeconform, Terraform validation |

---

## Architecture

La chaîne globale du projet est structurée ainsi :

Les diagrammes détaillés de la plateforme, du pipeline CI/CD et du runtime Kubernetes sont disponibles dans [`docs/architecture.md`](docs/architecture.md).

Le guide pratique de démarrage, de vérification et de dépannage est disponible dans [`docs/guide-exploitation.md`](docs/guide-exploitation.md).

```text
                    Développement
                         │
                         ▼
                    Git & GitHub
                         │
                         ▼
                 GitHub Actions
              ┌──────────┼───────────┐
              │          │           │
              ▼          ▼           ▼
            Tests      Docker     Validations
                         │          Kubeconform
                         ▼          Terraform
                       Trivy
                         │
              ┌──────────┴──────────┐
              │                     │
         Pull Request          push sur main
              │                     │
              ▼                     ▼
       validation complète      Publication GHCR
                                    │
                                    ▼
                              Kubernetes local
                               ┌──────┴──────┐
                               │             │
                               ▼             ▼
                            FastAPI      PostgreSQL
                               │             │
                               └──────┬──────┘
                                      ▼
                            Prometheus / Grafana
```

---

## Structure du projet

```text
devops-project/
│
├── frontend/
├── backend/
│   ├── app/
│   ├── tests/
│   ├── Dockerfile
│   └── requirements.txt
│
├── database/
│   └── init.sql
│
├── docker/
│   └── docker-compose.yml
│
├── kubernetes/
│   ├── api-config.yaml
│   ├── api-serviceaccount.yaml
│   ├── api.yaml
│   ├── namespace.yaml
│   ├── postgres.yaml
│   └── monitoring/
│       ├── api-servicemonitor.yaml
│       └── postgres-exporter-servicemonitor.yaml
│
├── terraform/
│   ├── backend.tf
│   ├── configmap.tf
│   ├── namespace.tf
│   ├── outputs.tf
│   ├── provider.tf
│   ├── service.tf
│   ├── variables.tf
│   ├── versions.tf
│   └── terraform.tfvars.example
│
├── .github/
│   └── workflows/
│       └── ci.yml
│
├── docs/
│   ├── architecture.md
│   └── guide-exploitation.md
│
├── .env.example
├── .gitignore
└── README.md
```

---

## Progression du projet

### Phase A — Fondations

Mise en place de l'environnement Linux/WSL, de Git/GitHub, de l'organisation du dépôt et de la première documentation.

### Phase B — Backend et base de données

Création de l'API FastAPI connectée à PostgreSQL avec SQLAlchemy.

L'API expose notamment des opérations CRUD sur les applications : création, lecture, modification et suppression.

### Phase C — CI/CD

Mise en place d'une première chaîne GitHub Actions comprenant :

- installation des dépendances ;
- démarrage d'un PostgreSQL de test ;
- initialisation de la base ;
- tests d'intégration PostgreSQL ;
- tests API avec pytest ;
- build de l'image Docker ;
- publication sur GHCR ;
- validation des manifests Kubernetes avec Kubeconform.

Image publiée :

```text
ghcr.io/sara-aitaami/devops-deploy-platform
```

### Phase D — Kubernetes

Déploiement de la plateforme sur un cluster Kubernetes local avec :

- namespace dédié ;
- Deployment FastAPI ;
- Deployment PostgreSQL ;
- Services FastAPI et PostgreSQL ;
- PersistentVolumeClaim PostgreSQL ;
- ConfigMaps et Secrets ;
- readiness et liveness probes ;
- resource requests et limits.

La persistance PostgreSQL a été vérifiée après suppression puis recréation du Pod.

### Phase E — Infrastructure as Code avec Terraform

Gestion progressive de l'infrastructure Kubernetes avec Terraform.

La configuration comprend notamment :

```text
terraform/
├── backend.tf
├── configmap.tf
├── namespace.tf
├── outputs.tf
├── provider.tf
├── service.tf
├── variables.tf
├── versions.tf
└── terraform.tfvars.example
```

Ressources actuellement gérées par Terraform :

- namespace `devops` ;
- ConfigMap `terraform-info` ;
- Service `devops-api`.

Le state est stocké dans **HCP Terraform**. Les opérations Terraform nécessitant l'accès au cluster restent exécutées localement depuis WSL.

### Phase F — Monitoring & Observabilité

Mise en place d'une stack Prometheus/Grafana pour observer la plateforme.

**API**

- `/metrics` avec `prometheus-fastapi-instrumentator` ;
- suivi des requêtes, codes HTTP, débit et latence.

**Prometheus**

- déploiement via `kube-prometheus-stack` ;
- découverte de l'API par `ServiceMonitor` ;
- observation de PostgreSQL via `postgres_exporter` et `ServiceMonitor`.

**Grafana**

Dashboards configurés :

- `API - Disponibilité`
- `Kubernetes - Supervision`
- `PostgreSQL - Supervision`

**Health checks**

- `/health` pour la liveness ;
- `/ready` pour la readiness avec vérification de PostgreSQL.

**Alerting**

Règles configurées pour détecter notamment :

- l'indisponibilité de l'API ;
- l'indisponibilité de PostgreSQL ;
- un taux élevé de réponses HTTP 5xx ;
- l'absence de Pod API Ready.

Un contact point Webhook a également été configuré pour tester la livraison des notifications.

### Phase G — Sécurité

La sécurité est traitée en défense en profondeur.

#### G1 — Scan des images Docker

Trivy analyse les paquets système et bibliothèques Python de l'image Docker pour les vulnérabilités `HIGH` et `CRITICAL`.

Le pipeline échoue lorsqu'une vulnérabilité corrigible de ce niveau est détectée ; les vulnérabilités sans correctif disponible sont ignorées avec `ignore-unfixed`.

#### G2 — Gestion des secrets

Les credentials sensibles ne sont pas stockés dans les manifests Kubernetes versionnés.

Les Secrets Kubernetes sont créés séparément et injectés via `secretKeyRef`. Les variables locales Docker Compose sont conservées dans `.env`, ignoré par Git, avec un `.env.example` versionné.

Le backend n'utilise plus de mot de passe PostgreSQL par défaut : `DB_PASSWORD` doit être fourni explicitement lorsque `DATABASE_URL` n'est pas utilisée.

Les fichiers Terraform sensibles (`*.tfvars`, `*.tfstate`) et les fichiers `.env` sont exclus du suivi Git.

Les credentials présents dans la CI sont limités à l'environnement PostgreSQL temporaire utilisé pour les tests automatisés.

#### G3 — RBAC Kubernetes

L'API dispose d'un `ServiceAccount` dédié nommé `devops-api`.

Aucun `Role`, `RoleBinding` ou `ClusterRoleBinding` n'est attribué à l'application, car elle n'a pas besoin d'interagir avec l'API Kubernetes.

Le montage automatique du token est désactivé avec `automountServiceAccountToken: false`.

Les contrôles `kubectl auth can-i` donnent `no` pour les accès testés aux Pods, Secrets et Deployments.

#### G4.1 — Audit des secrets avec Gitleaks

Un audit Gitleaks du dépôt Git a porté sur 31 commits et n'a détecté aucun secret selon les règles actives.

Un contrôle historique séparé a toutefois montré que des credentials de démonstration utilisés par la CI avaient existé dans d'anciens commits. L'historique Git n'a pas été réécrit pendant cette phase.

#### G4.2 — Durcissement de GitHub Actions

Les permissions du workflow suivent le principe du moindre privilège :

```yaml
permissions:
  contents: read
```

Le job Docker ajoute uniquement :

```yaml
permissions:
  contents: read
  packages: write
```

Les actions sont épinglées sur des SHA complets et la publication GHCR est autorisée uniquement lors d'un `push` sur `main`.

Les Pull Requests exécutent les contrôles de validation sans publier d'image sur GHCR.

#### G4.3 — Durcissement du runtime Docker et Kubernetes

L'image Docker utilise un utilisateur système non privilégié :

```dockerfile
USER 10001:10001
```

Le runtime Kubernetes applique notamment :

```yaml
runAsNonRoot: true
runAsUser: 10001
runAsGroup: 10001
fsGroup: 10001
seccompProfile:
  type: RuntimeDefault
allowPrivilegeEscalation: false
capabilities:
  drop:
    - ALL
readOnlyRootFilesystem: true
automountServiceAccountToken: false
```

Ces contrôles réduisent les possibilités d'escalade de privilèges et limitent l'impact potentiel d'une compromission du conteneur.

#### G4.4 — Synthèse DevSecOps et validation finale

La chaîne de protection est organisée ainsi :

```text
Code / Git
    ↓
Gitleaks
    ↓
GitHub Actions durci
    ↓
Build Docker
    ↓
Trivy
    ↓
Image non-root
    ↓
Kubernetes durci
    ↓
RBAC minimal
    ↓
Validation runtime
```

Validation finale de la Phase G :

| Contrôle | Résultat |
|---|---|
| Gitleaks | Aucun leak détecté selon les règles actives |
| Trivy | 0 vulnérabilité détectée sur les paquets Debian et Python analysés |
| Kubeconform | 10 ressources valides, 0 invalide |
| Kubernetes runtime | UID 10001, `/health` HTTP 200, non-root, seccomp RuntimeDefault, capacités supprimées, filesystem racine en lecture seule |
| RBAC | Aucune permission applicative sur les accès testés aux Pods et Secrets |

---

## CI/CD

Le comportement du pipeline diffère selon le contexte d'exécution :

```text
Git push / Pull Request
          │
          ▼
   GitHub Actions
          │
   ┌──────┼───────────────┐
   │      │               │
 Tests  Docker       Validations
          │          Kubeconform
          │          Terraform
          ▼
        Trivy
          │
   ┌──────┴───────────────┐
   │                      │
Pull Request         push sur main
   │                      │
   ▼                      ▼
Validation          Publication GHCR
complète                  │
                          ▼
                    Kubernetes local
```

Les validations Kubernetes et Terraform sont réalisées dans la CI sans dépendre du cluster local.

La validation Terraform utilise Terraform 1.16.1 et contrôle notamment le formatage et la validité de la configuration sans initialiser le backend distant.

---

## Tests et validation

Les tests automatisés du backend utilisent **pytest**.

Les contrôles de la plateforme comprennent notamment :

- tests API ;
- tests d'intégration PostgreSQL ;
- build Docker ;
- scan Trivy ;
- validation Kubeconform ;
- validation Terraform ;
- audit Gitleaks ;
- vérification des `SecurityContext` Kubernetes ;
- vérification de l'identité et des permissions RBAC du Pod.

La Phase G a été validée avec les résultats suivants :

```text
Gitleaks   = 0
Trivy      = 0
Kubeconform = 0
```

Le runtime de l'API a également été vérifié en conditions réelles avec l'UID `10001` et un endpoint `/health` retournant HTTP 200.

---

## État actuel

La plateforme dispose actuellement de :

- une API FastAPI fonctionnelle ;
- PostgreSQL avec persistance ;
- Docker et Docker Compose ;
- une CI GitHub Actions ;
- publication d'image sur GHCR ;
- déploiement Kubernetes local ;
- ConfigMaps et Secrets hors Git ;
- readiness et liveness probes ;
- `/health` et `/ready` ;
- Prometheus, Grafana et Alertmanager ;
- instrumentation FastAPI et `postgres_exporter` ;
- ServiceMonitors API et PostgreSQL ;
- dashboards et règles d'alerting ;
- Terraform avec state distant HCP Terraform ;
- validation Kubernetes et Terraform dans la CI ;
- ServiceAccount dédié pour FastAPI ;
- RBAC minimal et token Kubernetes non monté automatiquement ;
- audit Gitleaks ;
- scan Trivy ;
- GitHub Actions durci avec permissions minimales et actions épinglées ;
- image Docker exécutée en non-root avec l'UID `10001` ;
- filesystem racine en lecture seule ;
- capacités Linux supprimées ;
- `allowPrivilegeEscalation: false` ;
- profil seccomp `RuntimeDefault`.

---

## Limites actuelles et prochaines évolutions

Le projet reste volontairement focalisé sur une plateforme locale de démonstration. Les évolutions possibles incluent notamment :

- centralisation des logs avec une solution dédiée ;
- stratégie GitOps ;
- intégration d'un gestionnaire de secrets externe ;
- stratégie de déploiement progressive ;
- autoscaling ;
- exposition via Ingress ;
- supervision et alerting plus avancés.

---
