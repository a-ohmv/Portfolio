# outils.sh : menu Bash d'outils réseau

Script Bash interactif pour tester des machines de mon homelab.
Écrit en octobre 2026, dans le cadre de mon autoformation réseau/Linux.

## Fonctionnalités
1. **Scan Nmap** : scan de plusieurs IP, avec test de présence avant le scan
2. **Scan IP** : test de présence par ping
3. **Scan disque** : espace disque et RAM
4. **Scan de ports** : ports 20 à 100 en TCP, sans nmap

## Utilisation

```bash
chmod +x outils.sh
./outils.sh
```

Exemple : il faut saisir plusieurs IP séparées par un espace (`192.0.2.10 192.0.2.11`).

## Ce que j'ai appris
- Fonctions Bash (`demander_ip`, `machine_en_ligne`) et codes de retour (`return 1`)
- Tableaux, boucles `for` et `case`
- Enchaînement avec `||`, `&&` et redirections (`> /dev/null 2>&1`)
- Mon premier test affichait "Scan réussi" sur une machine éteinte, parce que nmap retourne 0 dans tous les cas. J'ai corrigé avec un test ping avant le scan.

## Limites
- Les scans de ports sont limités à la plage 20-100 et au protocole TCP
- Le ping peut être bloqué par un pare-feu, la machine paraît alors hors ligne

## Usage responsable
J'utilise ce script uniquement sur mes propres machines ou sur un réseau où j'en ai l'autorisation.