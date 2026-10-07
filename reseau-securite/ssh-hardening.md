30/09/2026

# Durcissement de l'accès SSH sur un serveur Debian (homelab)

## Contexte

Dans le cadre de mon homelab personnel (Proxmox VE), j'ai mis en place et sécurisé 
l'accès SSH à une VM Debian 13 (`debian-01`), en remplaçant l'authentification par 
mot de passe par une authentification par clé publique/privée.

## Objectif

- Comprendre le fonctionnement de l'authentification par clé SSH
- Déployer une clé publique/privée depuis un poste Windows vers un serveur Linux
- Désactiver l'authentification par mot de passe côté serveur
- Vérifier concrètement que la nouvelle configuration fonctionne comme prévu

## Démarche

1. **Génération de la paire de clés** (`ssh-keygen`, algorithme ed25519) sur le poste client
2. **Copie de la clé publique** sur le serveur dans `~/.ssh/authorized_keys` :
```powershell
   type $env:USERPROFILE\.ssh\id_ed25519.pub | ssh user@10.0.0.XXX "cat >> ~/.ssh/authorized_keys"
```
3. **Retrait de la passphrase** de la clé privée (choix pour cette VM de lab, la clé 
   restant strictement locale à mon poste) :
```powershell
   ssh-keygen -p -f $env:USERPROFILE\.ssh\id_ed25519
```
4. **Vérification de la connexion par clé**, sans mot de passe demandé
5. **Désactivation de l'authentification par mot de passe** côté serveur,
   dans `/etc/ssh/sshd_config` :

```
   PasswordAuthentication no
```

   puis redémarrage du service :

```bash
   sudo systemctl restart sshd
```
6. **Vérification finale**, en forçant le client à ignorer la clé pour confirmer 
   que le mot de passe est bien rejeté :
```powershell
   ssh -o PubkeyAuthentication=no user@10.0.0.XXX
```
   Résultat obtenu : `Permission denied (publickey)`, sans invite de mot de passe — 
   confirme que seule l'authentification par clé est désormais acceptée.

## Difficultés rencontrées

- **Confusion entre passphrase et mot de passe du compte** : lors du retrait de la 
  passphrase, j'ai initialement cru qu'on me demandait de changer le mot de passe 
  système. Ce sont deux secrets totalement indépendants : la passphrase protège 
  le fichier de clé privée en local, le mot de passe protège le compte utilisateur.
- **Précaution méthodologique** : avant de redémarrer le service SSH avec la nouvelle 
  configuration, j'ai gardé une session SSH déjà ouverte active, pour pouvoir corriger 
  une erreur de configuration sans me retrouver bloqué hors du serveur.

## Résultat

Accès SSH à `debian-01` désormais strictement limité à l'authentification par clé, 
la clé privée ne quittant jamais mon poste. L'authentification par mot de passe, 
vulnérable au brute-force en ligne, est totalement désactivée côté serveur.

## Prochaines étapes

- Étendre le même durcissement aux autres VMs du homelab où c'est pertinent (Kali)
- Mettre en place un gestionnaire de mots de passe pour stocker une éventuelle 
  passphrase