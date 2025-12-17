import json
import random
import time

# -----------------------------------------------------
# Lecture des cartes depuis cards.json
# -----------------------------------------------------
def lire_cartes(niveau):
    try:
        with open("cards.json", "r", encoding="utf-8") as file:
            data = json.load(file)
        return data[niveau]
    except FileNotFoundError:
        print("Le fichier cards.json n'existe pas.")
        return[]

# -----------------------------------------------------
# Mélanger les cartes
# -----------------------------------------------------
def melanger_cartes(cartes):
    melange = list(cartes)
    random.shuffle(melange)
    return melange

# -----------------------------------------------------
# Afficher les cartes
# -----------------------------------------------------
def afficher_cartes(cartes, etat):
    print("********** CARTES **********")

    for i in range(len(cartes)):

        if etat[i] == "cache":           #Si la carte est cachee, cest sa position qui apparaitra ex: [1].
            print(f"[{i+1}]", end=" ")

        elif etat[i] == "visible":       #Si la carte est visible, cest son emoji qui apparaitra.
           print(f"{cartes[i]}", end=" ")

        elif etat[i] == "trouve":        #Si la carte est trouvee, il y aura un [X] a sa position.
            print("X", end=" ")
    
    print("\n")


# -----------------------------------------------------
# Demander une position valide
# -----------------------------------------------------
def demander_position(nb_cartes, etat):
    while True:
        try:
            position = int(input(f"Choisissez une position (1 à {nb_cartes}) : "))-1
            if  0 <= position < nb_cartes and etat[position] == "cache":  #La carte chosie doit etre cachee.
                return position  
            else:
                print("Position invalide ou carte déjà révélée.")
        
        except ValueError:
            print("Vous devez entrer un nombre.")


# -----------------------------------------------------
# Gérer les choix
# -----------------------------------------------------
def gerer_choix(cartes, etat):
    choix1 = demander_position(len(cartes), etat)
    etat[choix1] = "visible"
    afficher_cartes(cartes, etat)


    choix2 = demander_position(len(cartes), etat)
    etat[choix2] = "visible"
    afficher_cartes(cartes, etat)

    #Fait une pause de 1 seconde entre le choix des cartes et le resultat.
    time.sleep(1) 

    if cartes[choix1] == cartes[choix2]:
        print("Paire trouvée! \n----------------------------------------\n")
        etat[choix1] = "trouve"
        etat[choix2] = "trouve"
        
       
    else:
        print("Pas une paire. \n----------------------------------------\n")
        etat[choix1] = "cache"
        etat[choix2] = "cache"
    
    time.sleep(1)

# -----------------------------------------------------
# Ajouter un score au fichier scores.json
# -----------------------------------------------------
def ajouter_score(nom, coups):
    try:
        with open("scores.json", "r", encoding="utf-8") as file:
            scores= json.load(file)
    except FileNotFoundError:
        print("Le fichier scores.json n'existe pas.")

    scores.append({"nom": nom,"coups": coups})

    with open("scores.json","w", encoding="utf-8") as file:
        json.dump(scores, file, indent=4)

# -----------------------------------------------------
# Afficher tous les scores
# -----------------------------------------------------
def afficher_scores():
    try:
        with open("scores.json", "r", encoding="utf-8") as file:
            scores= json.load(file)
            print(scores)  
    except FileNotFoundError:
        print("Le fichier scores.json n'existe pas.")  

# -----------------------------------------------------
# Mode 1 joueur
# -----------------------------------------------------
def jouer_1joueur(cartes):
    print("\n")
    #Melanger les cartes et les cacher
    cartes = melanger_cartes(cartes)
    etat = ["cache"] * len(cartes)   
    coups = 0

    joueur=(input("Nom du joueur: "))
    #Validation du nom.
    while joueur =="":
        joueur = (input("Nom du joueur: "))

    print("\n")
    #La boucle continue jusqua ce que toutes les cartes soient trouvees.
    while "cache" in etat:
        afficher_cartes(cartes, etat)
        gerer_choix(cartes, etat)
        coups += 1

    print(f"Bravo {joueur}, vous avez trouvé toutes les paires en {coups} coups!")
    ajouter_score(joueur, coups)

    while True:
        suite=input("\n1- Rejouer.\n2- Revenir au menu.\n->")
        if suite == "1":
            jouer_1joueur(cartes)
            break
        elif suite == "2":
            menu_principal()
            break
        else:
            print("Entrez un choix valide.")
    
# -----------------------------------------------------
# Mode 2 joueurs
# -----------------------------------------------------
def jouer_2joueurs(cartes):
    #Melanger les cartes et les cacher.
    cartes = melanger_cartes(cartes)
    etat = ["cache"] * len(cartes)   

    joueurs=["",""]
    for i in range(2):
        joueurs[i]= input(f"Nom du joueur {i+1} : ")
        #Validation des noms.
        while joueurs[i] =="":
            joueurs[i]=input(f"Nom du joueur {i+1} : ")

    
    #Initialisation du nb de coups et de paires.
    coups = [0,0]
    paires = [0,0]
    index = 0

    print("\n")
    #La boucle continue jusqua ce que toutes les cartes soient trouvees.
    while "cache" in etat:
        print(f"C'est le tour de {joueurs[index]}.")

        afficher_cartes(cartes, etat)

        #Comparer le nb de paires trouvees avant et apres pour voir si une nouvelle paire a ete trouvee.
        avant = etat.count("trouve")
        gerer_choix(cartes, etat)
        apres = etat.count("trouve")
        
        if avant < apres :
            paires[index] += 1
        
        coups[index] += 1
        
        #Change le tour (le prochain joueur a le tour)
        index = 1 - index
        
        
    print(f"{joueurs[0]} : {paires[0]} paires.")
    print(f"{joueurs[1]} : {paires[1]} paires.")

    if paires[0] > paires[1]:
        print(f"{joueurs[0]} vous avez gagné!")

    elif paires[0] < paires[1]:
        print(f"{joueurs[1]} vous avez gagné!")
    
    else:
        print("Match nul.")
    
    ajouter_score(joueurs[0], coups[0])
    ajouter_score(joueurs[1], coups[1])

    while True:
        suite=input("1- Rejouer\n2- Revenir au menu.\n ->")
        if suite == "1":
            jouer_2joueurs(cartes)
            break
        elif suite == "2":
            menu_principal()
            break
        else:
            print("Entrez un choix valide.")


    
# -----------------------------------------------------
# Menu principal 
# -----------------------------------------------------5

def menu_principal():
    while True:
        
        print("\n=== MENU PRINCIPAL ===")
        print("1 - Jouer une partie")
        print("2 - Afficher les scores")
        print("3 - Quitter")

        choix = input("-> ")
 
        if choix == "1":
            while True:
                niveau = input("\nChoisissez un niveau :\n 1 - Facile \n 2 - Moyen \n 3 - Difficile \n-> ")
                if niveau == "1":
                    cartes = lire_cartes("facile")
                    break
                elif niveau == "2":
                    cartes = lire_cartes("moyen")
                    break
                elif niveau =="3":
                    cartes = lire_cartes("difficile")
                    break
                else:
                    print("\nEntrez un choix valide (1,2 ou 3).")
            
                    
                
            while True:
                mode = input("\nNombre de joueurs:\n-> ")
                if mode == "1":
                    jouer_1joueur(cartes)
                    break

                elif mode == "2":
                    jouer_2joueurs(cartes)
                    break

                else:
                    print("Entrez un choix valide ( 1 ou 2 ).")
            



        elif choix == "2":
            afficher_scores()

        elif choix == "3":
            print("Merci d'avoir joue ! À bientôt.")
            break

        else:
            print("Entrez un choix valide.")
 
menu_principal()
