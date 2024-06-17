from curses import KEY_SCOMMAND
import datetime
import sys
from typing import Any
from tgtg import *
import configparser
import json
import datetime
import signal

config = configparser.ConfigParser()

# --------- LECTURE (ou non) DU FICHIER DE CONFIG ---------

try: 
	config.read("config.ini")
	connected = config.getboolean("connexion", "connected")
except:
	connected = False 
	config.add_section("connexion")
	config.add_section("credentials")
	config.set("connexion", "connected", "False")


# --------- CONNEXION ---------

try:
	if not connected: # Si compte non connecté
		inptemail = input("Email tgtg : ")
		client = TgtgClient(email=inptemail)
		credentials = client.get_credentials()

	else : # déjà connecté > récup des données
		try:
			credentials = {
				"access_token": config.get("credentials", "access_token"),
				"refresh_token": config.get("credentials", "refresh_token"),
				"user_id": config.get("credentials", "user_id"),
				"cookie": config.get("credentials", "cookie"),
			}
			client = TgtgClient(**credentials)

		except configparser.NoOptionError as cf:
			print(f"Problème dans le fichier de configuration. \n > Détail: {cf}")
			sys.exit(1)   
		
		except Exception as e:
			print(f"Erreur : {e}")
			sys.exit(1)

	config.set("credentials", "access_token", credentials["access_token"])
	config.set("credentials", "refresh_token", credentials["refresh_token"])
	config.set("credentials", "user_id", credentials["user_id"])
	config.set("credentials", "cookie", credentials["cookie"])
	config.set("connexion", "connected", "True")

	with open("config.ini", "w") as configfile:
		config.write(configfile) #sauvegarde de la configuration

	client.get_items() # pour s'assurer de la bonne connexion

except TgtgAPIError as api:
	print(f"Problème de connexion. Attention à la config fournie! \n> Détail : {api}")
	sys.exit(1)

except Exception as e: 
	print(e.__class__)
	print(f"Erreur : non connecté, {e}")
	sys.exit(1)

print("Connecté en tant que ", client.email)


# --------- RECUP DES FAVORIS ---------

try: # session existante
	with open('favoris.json', 'r') as f:
		data = json.load(f)

except: # impossible d'ouvrir les favs - création de la session
	try:
		# charger manuellement / premier chargement
		favs: list[set] = client.get_items() # recup favoris (set de données)
		data: dict[int, set[chr, Any]] = {}

		for it in favs: #ajout des favoris dans le dico (première fois)
			it_id: int = it["item"]["item_id"]
			data[it_id] = {
				"display_name": it["display_name"],
				"items_available": it["items_available"],
				"majPanier": None,
				"lastUpdate": datetime.datetime.now().isoformat(),
				"old_available" : 0 # mémoire du nb d'items available à la dernière itération (pour le check des paniers)
			}

	except Exception as e: # pb lors du chargement des items?
		print(f"Erreur : {e}")



def send_notification(msg: str):
	"""
	PARAM futur : message à inclure dans la notif + destinataire ?
	"""
	print(str+" - Notification envoyée!")
	pass


# --------- SORTIE PROGRAMME (save) ---------

def sortie(sig, frame):
	"""
	Fonction de sortie du programme lors de la réception d'un signal. \n
	Params :
	* sig : signal reçu
	* frame : frame d'execution en cours (nécessaire lors de l'appel avec signal)
	- returns : rien, sort du programme (sysexit)
	"""
	# Save des favoris dans un fichier
	with open('favoris.json', 'w') as f:
		json.dump(data, f, indent=4)
	print("\nDonnées sauvegardés")
	sys.exit(0)

signal.signal(signal.SIGINT, sortie) # déclaration de la redirection du signal


# --------- COMPARAISON DES ITEMS DISPOS (nouveaux paniers) ---------

while True:
	for keyData, itemData in data.items():
		# condition : paniers dispo + les paniers n'étaient pas déjà dispo
		if (itemData["items_available"]>0) and (itemData["old_available"]==0) and (itemData["items_available"] > itemData["old_available"]): 
			print("Nouveau panier : ", itemData["display_name"])
			itemData["majPanier"] = datetime.datetime.now().isoformat() # mémoire de l'heure d'ajout du dernier panier
			# envoi notification --
			send_notification(str(itemData["display_name"]+"("+itemData["items_available"]+")"))

		# changement du dernier disponible + date du dernier chargement
		itemData["old_available"] = itemData["items_available"] 
		itemData["lastUpdate"] = datetime.datetime.now().isoformat()
		