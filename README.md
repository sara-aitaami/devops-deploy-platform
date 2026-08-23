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

## CI/CD et Kubernetes

La chaîne actuelle du projet est :

```text
Git push
   ↓
GitHub Actions
   ├── Tests
   ├── Build Docker
   ├── Publication GHCR
   └── Validation des manifests Kubernetes
            ↓
     Déploiement Kubernetes local

La validation des manifests Kubernetes dans GitHub Actions est réalisée avec Kubeconform et ne nécessite pas d'accès au cluster Kubernetes local.

Le déploiement sur le cluster Kubernetes local est actuellement réalisé séparément à l'aide de kubectl.
```

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
validation des manifests Kubernetes dans la CI.

Les prochaines étapes du projet concernent notamment :

Terraform ;
monitoring ;
observabilité ;
amélioration du déploiement ;
finalisation de l'infrastructure.
