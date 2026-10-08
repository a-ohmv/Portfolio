import socket

def demander_ip():
    """Fonction qui permet d'entrer une adresse IP quand elle est appelée.

    Affiche un message si rien n'est saisi.
    Renvoie l'IP saisie (str), ou une chaîne vide (si rien n'a été tapé) pour pouvoir l'utiliser en dehors de la fonction
    """
    ip = input("Entrer une IP : ")
    if ip == "":
        print("\nAucune IP saisie.\n")
    return ip

def tester_port(ip, port):
    """Fonction qui permet de tester un port TCP d'une adresse IP.

    Reçoit une IP (str) et un numéro de port (int).
    Renvoie True si le port est ouvert, False si le port est fermé, et None si l'IP entrée est invalide ("abc" par exemple).
    """
    s = socket.socket()
    # Si le port ne répond pas au bout d'une seconde, il est considéré comme fermé ou filtré (pare-feu).
    # Une valeur plus haute ralentirait considérablement le scan.
    s.settimeout(1)
    try:
        result = s.connect_ex((ip, port))
    except socket.gaierror:
        # Si IP invalide (exemple "abc"), on renvoie None.
        return None
    finally:
        s.close()
    # 0 quand le port est ouvert, si un autre nombre, le port est fermé.
    if result == 0:
        return True
    else:
        return False

def scan_plage():
    """Fonction qui permet de scanner une plage de ports TCP sur une adresse IP.

    Demande l'IP, le port de début et le port de fin (int), puis affiche les ports ouverts.
    Affiche un message et s'arrête si un port est hors de 0-65535, si le port de début dépasse celui de fin,
    ou si l'IP est invalide.
    """
    ip = demander_ip()
    if ip == "":
        return
    try:
        port1 = int(input("Entrer le port de début : "))
        port2 = int(input("Entrer le port fin : "))
        if port2 > 65535 or port1 < 0:
            print("\nLe port de fin doit être inférieur ou égal à 65535 et le port de début égal ou supérieur à 0.\n")
            return
        elif port1 > port2:
            print("\nLe port début ne doit pas être supérieur au port de fin.\n")
            return
    except ValueError:
        print("\nEntrer un numéro, pas une chaine de caractères.\n")
        return
    # Si le port de fin saisi est le port 22, range s'arrêtera à 21,
    # j'ai donc ajouté + 1 pour tester aussi le port de fin.
    for n in range(port1, port2 + 1):
        result = tester_port(ip, n)
        if result is None:
            print("\nEntrer une IP valide.\n")
            return
        elif result:
            print(f"Port {n} est ouvert")
    print("\nScan terminé.\n")

def scan_port():
    """Fonction qui permet de scanner un port TCP sur une adresse IP.

    Demande l'IP et le port qu'on veut scanner.
    Affiche un message si l'IP est invalide.
    Affiche un message et s'arrête si le port saisi n'est pas un nombre ("abc" par exemple).
    Affiche un message et s'arrête si un port est hors de 0-65535.
    Affiche si le port est ouvert ou s'il est fermé.
    """
    ip = demander_ip()
    if ip == "":
        return
    try:
        port = int(input("Entrer le port à tester: "))
        if port > 65535 or port < 0:
            print("\nLe port doit être compris entre 0 et 65535.\n")
            return
    except ValueError:
        print("\nEntrer un numéro, pas une chaine de caractères.\n")
        return
    result = tester_port(ip, port)
    if result is None:
        print("\nEntrer une IP valide.\n")
        return
    elif result:
        print(f"Port {port} est ouvert")
    else:
        print(f"Port {port} est fermé")
    print("\nScan terminé.\n")

def scan_courants():
    """Fonction qui permet de tester une liste fixe de ports courants sur une adresse IP.

    Demande l'IP.
    Affiche un message si l'IP est invalide.
    Les ports testés sont une liste fixe (21, 22, 23, 25, 53, 80, 443, 445, 3389).
    Affiche si le port est ouvert ou s'il est fermé.
    """
    port_liste = [21, 22, 23, 25, 53, 80, 443, 445, 3389]
    ip = demander_ip()
    if ip == "":
        return
    for port in port_liste:
        result = tester_port(ip, port)
        if result is None:
            print("\nEntrer une IP valide.\n")
            return
        elif result:
            print(f"Port {port} est ouvert")
        else:
            print(f"Port {port} est fermé")
    print("\nScan terminé.\n")

while True:
    print("1: Scan d'une plage de ports sur une IP")
    print("2: Scan d'un seul port sur une IP")
    print("3: Scan de ports courants sur une IP")
    print("\n10: Sortir\n")
    try:
        choix = int(input("Entrer un numéro pour valider votre choix: "))
        if choix == 1:
            scan_plage()
        elif choix == 2:
            scan_port()
        elif choix == 3:
            scan_courants()
        elif choix == 10:
            break
        else:
            print("\nEntrer un nombre valide.\n")
    except ValueError:
        print("\nEntrer un nombre valide\n")