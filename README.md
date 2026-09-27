# DevOps Deploy Platform

## Présentation

**DevOps Deploy Platform** est un projet de portfolio conçu pour reproduire une chaîne DevOps moderne utilisée en entreprise.

L'objectif est de construire progressivement une plateforme de déploiement moderne en utilisant les outils et les bonnes pratiques employés en entreprise.

Chaque étape du projet est réalisée manuellement afin de comprendre le rôle de chaque technologie avant de les intégrer dans une infrastructure complète.

---

## Objectif du projet

Ce projet a pour objectif de démontrer mes compétences en :

- Linux
- Git & GitHub
- Docker
- Docker Compose
- GitHub Actions
- Kubernetes
- PostgreSQL
- FastAPI
- CI/CD
- Infrastructure as Code
- Bonnes pratiques DevOps

À terme, ce dépôt constituera un projet de portfolio destiné à illustrer mes compétences lors de recherches d'alternance ou d'opportunités professionnelles.

---

## Technologies

Les technologies sont intégrées progressivement au cours du projet.

- Linux
- Git
- GitHub
- Docker
- Docker Compose
- GitHub Actions
- GitHub Container Registry (GHCR)
- Kubernetes
- PostgreSQL
- FastAPI
- Terraform
- Prometheus
- Grafana
- Trivy
- Monitoring

---

## Architecture du projet

La plateforme suit progressivement cette chaîne :

```text
Développement
     ↓
Git & GitHub
     ↓
GitHub Actions
     ├── Tests automatiques
     ├── Build Docker
     ├── Publication de l'image sur GHCR
     └── Validation des manifests Kubernetes
              ↓
          Kubernetes
          ├── FastAPI
          └── PostgreSQL
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
├── .github/
│   └── workflows/
│       └── ci.yml
│
├── docs/
│
├── .env.example
├── .gitignore
└── README.md
```

---

## Phase A — Fondations du projet

La première phase a permis de mettre en place les bases du projet :

Linux et environnement de développement
Git et GitHub
organisation du dépôt
première documentation

---

## Phase B — Backend et base de données

Le backend repose sur FastAPI et communique avec une base PostgreSQL.

L'API expose notamment des opérations CRUD sur les applications :

création ;
lecture ;
modification ;
suppression.

Le backend utilise SQLAlchemy pour communiquer avec PostgreSQL.

---

## Phase C — CI/CD

La Phase C a permis de mettre en place une première chaîne CI/CD professionnelle.

Le pipeline GitHub Actions réalise automatiquement :

l'installation des dépendances ;
le démarrage d'un service PostgreSQL de test ;
l'initialisation de la base de données ;
les tests d'intégration PostgreSQL ;
les tests API avec pytest ;
la construction de l'image Docker ;
la publication automatique de l'image sur GitHub Container Registry ;
la validation des manifests Kubernetes avec Kubeconform.

L'image Docker publiée est disponible sur :

ghcr.io/sara-aitaami/devops-deploy-platform

---

## Phase D — Kubernetes

La Phase D permet de déployer la plateforme sur un cluster Kubernetes local.

Les ressources Kubernetes mises en place comprennent notamment :

un namespace dédié ;
un Deployment FastAPI ;
un Deployment PostgreSQL ;
un Service FastAPI ;
un Service PostgreSQL ;
un PersistentVolumeClaim pour PostgreSQL ;
des ConfigMaps ;
des Secrets ;
des readiness probes ;
des liveness probes ;
des resource requests et limits.

L'application FastAPI utilise le Service Kubernetes postgres pour communiquer avec PostgreSQL.

La persistance des données PostgreSQL a également été vérifiée en supprimant puis en recréant le Pod PostgreSQL sans perdre les données stockées sur le volume persistant.

---

## Phase E — Infrastructure as Code avec Terraform

La Phase E permet de gérer progressivement l'infrastructure Kubernetes du projet avec Terraform.

Les éléments mis en place comprennent :

- le provider Kubernetes ;
- la gestion du namespace Kubernetes ;
- la gestion d'un ConfigMap ;
- la gestion du Service FastAPI ;
- les variables Terraform ;
- les validations des variables ;
- les outputs Terraform ;
- l'import de ressources Kubernetes existantes ;
- la gestion du Terraform state ;
- le stockage distant du state avec HCP Terraform ;
- la séparation des ressources Terraform par fichiers ;
- la validation Terraform dans GitHub Actions.

Le state Terraform est stocké dans HCP Terraform, tandis que les opérations Terraform sont exécutées localement sur l'environnement WSL contre le cluster Kubernetes Docker Desktop.

La configuration Terraform utilise notamment :

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
Les ressources actuellement gérées par Terraform sont :

- le namespace `devops` ;
- le ConfigMap `terraform-info` ;
- le Service `devops-api`.

---

## Phase F — Monitoring & Observabilité

La plateforme intègre une stack d'observabilité basée sur Prometheus et Grafana.

### Instrumentation de l'API

L'API FastAPI expose `/metrics` grâce à
`prometheus-fastapi-instrumentator`.

Les métriques HTTP permettent notamment de suivre :

- le nombre de requêtes ;
- les codes HTTP ;
- le débit de requêtes ;
- la latence des requêtes.

### Prometheus

Prometheus est déployé avec `kube-prometheus-stack`.

L'API est découverte via un `ServiceMonitor` Kubernetes.

PostgreSQL est observé via `postgres_exporter`, lui-même découvert par un `ServiceMonitor`.

### Grafana

Trois dashboards ont été configurés :

- `API - Disponibilité`
- `Kubernetes - Supervision`
- `PostgreSQL - Supervision`

Ils permettent de visualiser la disponibilité, le trafic HTTP,
les erreurs, la latence, l'état Kubernetes et les métriques PostgreSQL.

### Health checks

L'API expose :

- `/health` pour la liveness ;
- `/ready` pour la readiness, avec vérification de PostgreSQL.

Kubernetes utilise ces endpoints avec des `livenessProbe`
et `readinessProbe`.

### Logs

Les logs applicatifs FastAPI sont accessibles via Kubernetes avec
`kubectl logs`.

Des messages applicatifs sont également générés pour les événements
importants, notamment les erreurs métier et les contrôles de santé.

### Alerting

Grafana Alerting surveille notamment :

- l'indisponibilité de l'API ;
- l'indisponibilité de PostgreSQL ;
- un taux élevé de réponses HTTP 5xx ;
- l'absence de pod API Ready.

Un contact point Webhook a été configuré pour tester la livraison
des notifications.

---

## Phase G — Sécurité

### Scan des images Docker

Les images Docker sont analysées avec Trivy dans GitHub Actions avant leur publication sur GitHub Container Registry.

Le scan couvre :
- les paquets du système ;
- les bibliothèques Python ;
- les vulnérabilités `HIGH` et `CRITICAL`.

Les vulnérabilités pour lesquelles aucun correctif n'est disponible sont ignorées avec `ignore-unfixed`.

Le pipeline échoue si une vulnérabilité `HIGH` ou `CRITICAL` corrigible est détectée.

La chaîne Docker est donc :

```text
Build Docker
    ↓
Scan Trivy
    ↓
Tag de l'image
    ↓
Publication GHCR
```

### Gestion des secrets

Les credentials sensibles ne sont plus stockés dans les manifests Kubernetes versionnés.

Les Secrets Kubernetes `api-secret` et `postgres-secret` sont créés séparément avec `kubectl` et injectés dans les workloads.

Les variables locales utilisées avec Docker Compose sont stockées dans un fichier `.env` ignoré par Git.

Un fichier `.env.example` est fourni pour documenter les variables nécessaires sans contenir de credential réel.

Le backend ne possède plus de mot de passe PostgreSQL par défaut dans le code : `DB_PASSWORD` doit être fourni explicitement lorsque `DATABASE_URL` n'est pas utilisé.

Les fichiers Terraform sensibles (`*.tfvars`, `*.tfstate`) ainsi que les fichiers `.env` sont exclus du suivi Git.

Les credentials de test utilisés dans GitHub Actions correspondent à l'environnement PostgreSQL temporaire de la CI et ne sont pas utilisés comme secrets de production.

Les ressources Kubernetes continuent d'utiliser les `Secret` via `secretKeyRef`, tandis que les Secrets eux-mêmes restent hors du dépôt Git.

### RBAC Kubernetes

L'API FastAPI dispose d'un `ServiceAccount` Kubernetes dédié nommé `devops-api`.

L'application n'ayant pas besoin d'interagir avec l'API Kubernetes, aucun `Role`, `RoleBinding` ou `ClusterRoleBinding` ne lui est attribué.

Le montage automatique du token Kubernetes est également désactivé avec `automountServiceAccountToken: false`.

Cette configuration applique le principe du moindre privilège : le Pod FastAPI possède une identité Kubernetes dédiée mais aucune permission applicative sur les ressources Kubernetes.

Les permissions ont été vérifiées avec `kubectl auth can-i` pour les Pods, Secrets et Deployments, avec un résultat `no` dans les trois cas.

---

## CI/CD et Kubernetes

La chaîne actuelle du projet est :

```text
Git push
   ↓
GitHub Actions
   ├── Tests backend
   ├── Build Docker
   ├── Scan de vulnérabilités avec Trivy
   ├── Publication GHCR
   ├── Validation des manifests Kubernetes
   └── Validation de la configuration Terraform
            ↓
     Déploiement Kubernetes local
```

La validation des manifests Kubernetes est réalisée avec Kubeconform et ne nécessite pas d'accès au cluster Kubernetes local.

Le scan de sécurité des images Docker est réalisé avec Trivy avant leur publication sur GitHub Container Registry.

La validation Terraform utilise Terraform 1.16.1 et vérifie notamment le formatage et la validité de la configuration sans initialiser le backend distant.

Le state Terraform est stocké dans HCP Terraform.

Les opérations Terraform nécessitant un accès au cluster Kubernetes restent actuellement exécutées localement depuis l'environnement WSL.

Le déploiement Kubernetes local est actuellement réalisé avec kubectl.

---

## Tests

Les tests automatisés du backend utilisent pytest.

Les tests actuels couvrent notamment :

l'endpoint principal ;
la récupération des applications ;
la gestion d'une application inexistante.

Les tests sont exécutés localement et dans GitHub Actions.

---

## État actuel

Les éléments suivants sont actuellement fonctionnels :

- backend FastAPI ;
- PostgreSQL ;
- Docker ;
- Docker Compose ;
- tests automatisés ;
- GitHub Actions ;
- build Docker automatique ;
- scan des images Docker avec Trivy ;
- publication GHCR ;
- Kubernetes ;
- ConfigMaps ;
- Secrets Kubernetes gérés hors Git ;
- fichier .env.example ;
- PersistentVolumeClaim ;
- readiness probes ;
- liveness probes ;
- `/health` et `/ready` ;
- Prometheus ;
- Grafana ;
- Alertmanager ;
- `prometheus-fastapi-instrumentator` ;
- `postgres_exporter` ;
- ServiceMonitors pour l'API et PostgreSQL ;
- dashboards Grafana API, Kubernetes et PostgreSQL ;
- règles d'alerting ;
- contact point Webhook ;
- validation des manifests Kubernetes dans la CI ;
- Terraform ;
- HCP Terraform ;
- Terraform state distant ;
- validation Terraform dans GitHub Actions;
- ServiceAccount Kubernetes dédié pour FastAPI ;
- principe du moindre privilège appliqué ;
- token Kubernetes non monté automatiquement ;

---

## Pistes d'amélioration

Le projet peut ensuite évoluer vers une industrialisation plus poussée, par exemple :

- centralisation des logs avec une solution dédiée ;
- stratégie GitOps ;
- intégration d'un gestionnaire de secrets externe ;
- stratégie de déploiement progressive ;
- autoscaling ;
- exposition via Ingress ;
- supervision et alerting plus avancés.
