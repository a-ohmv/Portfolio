# Récupération matérielle — OnePlus 6T bloqué en mode EDL

## Contexte

Mon téléphone personnel (OnePlus 6T) fonctionnait parfaitement jusqu'à ce que je tente de le faire booter sur un autre OS que l'Android d'origine, dans l'idée de remplacer Android par **Ubuntu Touch**. Cette tentative a provoqué un bootloop logiciel (le téléphone ne démarre plus normalement). La première étape pour revenir en arrière était de restaurer le téléphone via le mode **EDL (Emergency Download)**, un mode de récupération bas niveau intégré aux puces Qualcomm. J'ai passé environ 3 jours à essayer de diagnostiquer pourquoi la communication avec le téléphone en mode EDL échouait systématiquement, sans jamais réussir à passer cette étape.

*Note : j'ai utilisé Claude (Anthropic) comme assistant tout au long de ce diagnostic, notamment pour comprendre la chaîne de démarrage Qualcomm et structurer la méthode d'élimination des causes.*

**À noter honnêtement : ce sujet dépasse largement mon niveau actuel.** Je ne maîtrise pas les détails du protocole Qualcomm (Sahara/Firehose) ni le reverse engineering de formats propriétaires impliqués dans ce diagnostic. Je documente ce cas pour une autre raison : la méthode de diagnostic suivie, et la persévérance que ça a demandé.

## Ce qui a été tenté

Le téléphone était bien détecté par l'ordinateur en mode EDL (reconnu comme périphérique Qualcomm), mais impossible d'en faire quoi que ce soit : la communication avec le protocole **Sahara** (l'étape qui doit suivre la détection pour pouvoir dialoguer avec le téléphone) ne répondait jamais, malgré de nombreuses tentatives différentes :

- Plusieurs outils et pilotes USB testés
- Deux systèmes d'exploitation différents (Windows et Linux)
- Changement de câbles et de ports USB physiques, au cas où le souci vienne de là

Rien n'a débloqué la situation : le téléphone restait détecté, mais injoignable au niveau du protocole.

## Résultat

Le diagnostic n'a pas abouti à une réparation : la cause exacte du blocage reste non confirmée (hypothèse d'un étage de démarrage corrompu, qui demanderait une intervention matérielle pour être tranchée). Le téléphone reste à ce jour non récupéré par voie logicielle, et le projet Ubuntu Touch en suspens tant que cette étape n'est pas franchie.

## Ce que je retiens

- Un diagnostic qui n'aboutit pas n'est pas un diagnostic raté : avoir testé et éliminé plusieurs pistes (outils, pilotes, OS, câbles, ports) permet de savoir où s'arrête ce qu'on peut tester soi-même, même sans comprendre la cause exacte
- Savoir reconnaître la limite de ce qu'on peut résoudre à son niveau (ici, un possible problème matériel nécessitant une intervention physique) fait aussi partie de la démarche
- Ce cas touche à des notions utilisées en forensique mobile professionnelle (chaîne de confiance/secure boot) que je ne maîtrise pas aujourd'hui, mais que j'espère creuser plus tard
