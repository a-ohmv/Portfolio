# Durcissement du pare-feu Proxmox et sauvegardes automatiques des VM

## Contexte

Mon homelab Proxmox (4 VM : Debian, pfSense, Kali Linux, Metasploitable2) tourne sur mon réseau domestique, partagé avec un colocataire qui travaille lui-même en cybersécurité. Ce modèle de menace particulier — un acteur techniquement compétent sur le même réseau local — m'a poussé à aller plus loin que les réglages par défaut sur deux points : la sauvegarde des VM et la restriction d'accès à l'interface d'administration Proxmox.

*Note : j'ai utilisé Claude (Anthropic) comme assistant tout au long de ce projet, pour m'expliquer les concepts, me guider pas à pas dans la configuration, et m'aider à diagnostiquer les problèmes rencontrés. Je garde la main sur chaque commande et chaque choix — l'IA m'aide à comprendre et à raisonner, pas à faire à ma place.*

## 1. Sauvegardes automatiques des VM

**Objectif :** pouvoir restaurer rapidement une VM en cas de casse, de mauvaise manipulation ou de compromission (notamment sur ma VM cible volontairement vulnérable).

**Mise en place :**
- Stockage de sauvegarde en SMB/CIFS, pointant vers un dossier partagé sur le SSD de mon PC Windows
- Job de sauvegarde planifié automatiquement chaque semaine, avec rétention des 3 dernières sauvegardes
- Durcissement du partage réseau côté Windows : permissions resserrées (partage + NTFS), accès limité à la seule IP de mon serveur Proxmox via le pare-feu Windows, partage protégé par mot de passe

**Détail important : profil réseau Windows (Privé vs Public).** Windows active ou désactive des jeux de règles de pare-feu entiers selon le profil réseau choisi. En profil **Public**, le partage de fichiers (SMB) est bloqué par défaut, quoi qu'on configure par ailleurs dans le pare-feu — c'est ce qui m'a bloqué au départ : Proxmox n'arrivait pas à joindre le dossier partagé, alors que toutes mes règles semblaient correctes. Il a fallu passer ce PC en profil **Privé** pour que le partage fonctionne, ce qui élargit en théorie la confiance accordée au réseau local — d'où l'importance de compenser ça avec une restriction par IP sur la règle de pare-feu concernée, plutôt que de se reposer uniquement sur le profil réseau.

**Résultat :** sauvegarde hebdomadaire automatique, testée avec succès, sans exposer le partage au reste du réseau local.

## 2. Restriction de l'interface web Proxmox

**Objectif :** limiter l'accès à l'interface d'administration (port 8006) et au SSH du serveur à mon seul PC principal, plutôt qu'à l'ensemble du réseau local.

**Ce que j'ai découvert en le faisant :**

Proxmox embarque un mécanisme interne qui autorise automatiquement *tout le réseau local détecté* sur ses ports de gestion — une fonctionnalité pensée pour éviter de se bloquer soi-même par erreur, mais qui devient un angle mort de sécurité dès qu'on veut restreindre l'accès à une seule machine sur ce même réseau. Il n'existe pas de réglage simple pour désactiver proprement ce comportement : il m'a fallu ajouter mes propres règles de pare-feu (autorisation explicite pour mon PC, puis blocage explicite du reste du réseau), et comprendre que l'**ordre d'évaluation des règles** est déterminant — une règle de blocage placée avant une règle d'autorisation plus spécifique l'emporte toujours.

J'ai d'ailleurs fait l'erreur une fois (règles dans le mauvais ordre), ce qui m'a coupé l'accès à mon propre serveur — rattrapé de justesse grâce à une session déjà connectée. Bonne leçon : toujours garder une connexion active ouverte avant de modifier un pare-feu à distance sur un serveur sans écran.

**Découverte annexe :** j'ai aussi appris à ouvrir une session SSH directement vers mon node Proxmox depuis PowerShell (`ssh root@<ip>`), plutôt que de passer systématiquement par le terminal web intégré à l'interface — plus pratique, et surtout indispensable comme filet de sécurité pendant ce genre de manipulation.

**Validation :** accès confirmé fonctionnel depuis mon PC, et bloqué (timeout) depuis deux sources externes testées (un autre appareil physique sur le réseau, et une VM de mon homelab sortant via NAT) — preuve par capture de paquets à l'appui, pas seulement par supposition.

## Ce que je retiens

- Un réglage de sécurité "par défaut" n'est pas toujours celui qu'on croit — il faut vérifier ce qui est réellement appliqué, pas ce qu'affiche l'interface
- L'ordre des règles de pare-feu change tout : premier match, premier servi
- Toujours garder un accès de secours avant de modifier un pare-feu à distance
- Documenter un vrai problème rencontré (et pas juste le résultat final) a plus de valeur qu'un tutoriel sans accroc
