# Scanner de ports TCP

Petit scanner de ports TCP en Python, écrit pour apprendre le fonctionnement des sockets et les bases du réseau.

## Fonctionnalités

- Scan d'une **plage de ports** sur une IP.
- Scan d'**un seul port** sur une IP.
- Scan d'une **liste de ports courants** : 21, 22, 23, 25, 53, 80, 443, 445, 3389.
- Contrôle des saisies : IP invalide, port hors de 0-65535, plage inversée.

## Utilisation

Aucune dépendance : seule la bibliothèque standard de Python 3 (`socket`) est utilisée.

```
python scanner.py
```

Un menu s'affiche : 1 (plage), 2 (un port), 3 (ports courants), 10 (quitter).

## Exemple

```
Entrer un numéro pour valider votre choix: 1
Entrer une IP : 192.168.0.XXX
Entrer le port de début : 20
Entrer le port fin : 30
Port 22 est ouvert

Scan terminé.
```

## Limites

- **TCP uniquement** : les ports UDP ne sont pas testés.
- **Timeout d'une seconde** : un port qui ne répond pas est considéré comme fermé, mais il peut aussi être filtré par un pare-feu. Les deux cas ne sont pas distingués.
- **Scan séquentiel** : un port après l'autre (jusqu'à une seconde par port qui ne répond pas), donc lent sur de grandes plages.

## Avertissement

À utiliser uniquement sur **vos propres machines** ou avec l'autorisation de leur propriétaire.
Scanner un réseau sans autorisation est interdit et peut être puni par la loi.
Je décline toute responsabilité en cas d'utilisation abusive.

## Pistes d'amélioration

- Passer les paramètres en ligne de commande avec `argparse`
- Ajouter le nom du service à côté de chaque port ouvert