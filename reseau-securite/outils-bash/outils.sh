#!/usr/bin/bash
demander_ip() {
	read -p "Entrez les IP à scanner (séparées par un espace) : " -a ips
	if [ "${#ips[@]}" -eq 0 ]
	then
		echo "Aucune IP saisie"
		return 1
	fi
}

machine_en_ligne() {
	ping -c 1 "$1" > /dev/null 2>&1
}

while true
do
	printf "1: Scan Nmap\n"
	printf "2: Scan IP\n"
	printf "3: Scan disque\n"
	printf "4: Scan ports des IP\n"
	printf "9: Sortir\n\n"
	read -p "Insérez un chiffre : " menu

	case "$menu" in
		1)
			demander_ip || continue
			for ip in "${ips[@]}"
			do
				machine_en_ligne "$ip" || { echo "$ip : hors ligne"; continue; }
				printf "\n- Scan de $ip: \n\n"
				if nmap "$ip"
				then
					printf "\n=== $ip: Scan NMAP réussi ===\n\n"
				fi
			done
			printf "\n=======Fin du scan=======\n\n"
			;;
		2)
			demander_ip || continue
			for ip in "${ips[@]}"
			do
				if machine_en_ligne "$ip"
				then
					printf "\n$ip: Ok\n\n"
				else
					printf "\n$ip: Pas Ok\n\n"
				fi
			done
			;;
		3)
			printf "\n===DISK===\n\n"
			df -h
			printf "\n===RAM===\n\n"
			free -h
			;;
		4)
			demander_ip || continue
			for ip in "${ips[@]}"
			do
				machine_en_ligne "$ip" || { echo "$ip : hors ligne"; continue; }
				printf "\nScan de $ip: \n\n"
				for port in {20..100}
				do
					if timeout 1 bash -c "echo > /dev/tcp/$ip/$port" 2>/dev/null
					then
						printf "Port $port ouvert\n\n"
					fi
				done
			done
			;;
		9)
			exit
			;;
	esac
done
