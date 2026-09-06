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
│   ├── api-secret.yaml
│   ├── api.yaml
│   ├── namespace.yaml
│   ├── postgres-secret.yaml
│   └── postgres.yaml
│
├── terraform/
├── monitoring/
├── .github/
│   └── workflows/
│       └── ci.yml
│
├── docs/
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

## CI/CD et Kubernetes

La chaîne actuelle du projet est :

```text
Git push
   ↓
GitHub Actions
   ├── Tests backend
   ├── Build Docker
   ├── Publication GHCR
   ├── Validation des manifests Kubernetes
   └── Validation de la configuration Terraform
            ↓
     Déploiement Kubernetes local
```

La validation des manifests Kubernetes est réalisée avec Kubeconform et ne nécessite pas d'accès au cluster Kubernetes local.

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

backend FastAPI ;
PostgreSQL ;
Docker ;
Docker Compose ;
tests automatisés ;
GitHub Actions ;
build Docker automatique ;
publication GHCR ;
Kubernetes ;
ConfigMaps ;
Secrets ;
PersistentVolumeClaim ;
readiness probes ;
liveness probes ;
resource requests et limits ;
validation des manifests Kubernetes dans la CI ;
Terraform ;
HCP Terraform ;
Terraform state distant ;
validation Terraform dans GitHub Actions ;
variables et outputs Terraform.

Les prochaines étapes du projet concernent notamment :

monitoring ;
observabilité ;
amélioration du déploiement ;
sécurisation et industrialisation de l'infrastructure ;
amélioration de la stratégie de déploiement.
