import socket

def demander_ip():
    ip = input("Entrer une IP : ")
    if ip == "":
        print("\nAucunes IP saisie.\n")
    return ip

def scan_plage():
    ip = demander_ip()
    if ip == "":
        return
    try:
        port1 = int(input("Entrer le port de début : "))
        port2 = int(input("Entrer le port fin : "))
        if port2 > 65535 or port1 < 0:
            print("\nLe port de fin doit être inférieur ou égal à 65535 et le port de début égal ou supérieur à 0.\n")
            return
    except ValueError:
        print("\nEntrer un numéro, pas une chaine de caractères.\n")
        return

    if port1 > port2:
        print("\nLe port de début doit être inférieur au port de fin.\n")
        return

    for n in range(port1, port2 + 1):
        s = socket.socket()
        s.settimeout(1)
        try:
            result = s.connect_ex((ip, n))
        except socket.gaierror:
            print("\nEntrer une IP valide.\n")
            return
        if result == 0:
            print(f"Port {n} is open")
        s.close()

    print("\nScan terminé.\n")

def scan_port():
    ip = demander_ip()
    if ip == "":
        return
    try:
        port = int(input("Entrer le port: "))
        if port > 65535 or port < 0:
            print("\nLe port doit être compris entre 0 et 65535.\n")
            return
    except ValueError:
        print("\nEntrer un numéro, pas une chaine de caractères.\n")
        return

    s = socket.socket()
    s.settimeout(1)
    try:
        result = s.connect_ex((ip, port))
    except socket.gaierror:
        print("\nEntrer une IP valide.\n")
        return
    if result == 0:
        print(f"Port {port} is open")
    else:
        print(f"Port {port} is closed")
    s.close()

    print("\nScan terminé.\n")

def scan_courants():
    port_liste = [21, 22, 23, 25, 53, 80, 443, 445, 3389]
    ip = demander_ip()
    if ip == "":
        return
    for port in port_liste:
        s = socket.socket()
        s.settimeout(1)
        try:
            result = s.connect_ex((ip, port))
        except socket.gaierror:
            print("\nEntrer une IP valide.\n")
            return
        if result == 0:
            print(f"Port {port} is open")
        s.close()
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