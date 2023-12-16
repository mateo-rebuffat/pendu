import pygame
import random
import sys
import os

# Initialisation de Pygame
pygame.init()

# Configuration
largeur_fenetre = 800
hauteur_fenetre = 600
couleur_fond = (255, 255, 255)
couleur_texte = (0, 0, 0)
taille_police = 40
niveaux_difficulte = {"facile": 10, "moyen": 7, "difficile": 5}

# Ajoutez les images du pendu
images_pendu = [pygame.image.load(f"pendu{i}.png") for i in range(9)]

# Fonction pour choisir un mot aléatoire
def choisir_mot():
    with open("mots.txt", "r") as fichier_mots:
        mots = fichier_mots.read().splitlines()
    return random.choice(mots)

# Fonction pour afficher le mot caché
def afficher_mot_cache(mot, lettres_trouvees):
    mot_cache = ""
    for lettre in mot:
        if lettre in lettres_trouvees:
            mot_cache += lettre
        else:
            mot_cache += "_"
    return mot_cache

# Fonction principale du jeu
def jouer_pendu(difficulte):
    mot_a_deviner = choisir_mot()
    lettres_trouvees = set()
    tentatives_max = niveaux_difficulte[difficulte]
    tentatives = 0

    # Initialisation de Pygame
    fenetre = pygame.display.set_mode((largeur_fenetre, hauteur_fenetre))
    pygame.display.set_caption("Jeu du Pendu")

    police = pygame.font.Font(None, taille_police)

    while tentatives < tentatives_max:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.unicode.isalpha():
                    lettre = event.unicode.lower()
                    lettres_trouvees.add(lettre)
                    if lettre not in mot_a_deviner:
                        # Traitement si la lettre n'est pas dans le mot
                        tentatives += 1

        fenetre.fill(couleur_fond)

        # Affichage du pendu
        if tentatives < len(images_pendu):
            fenetre.blit(images_pendu[tentatives], (10, 10))
        else:
            # Affichez une image par défaut si le nombre d'erreurs dépasse le nombre d'images disponibles
            fenetre.blit(images_pendu[-1], (50, 50))

        # Affichage du mot caché
        texte_mot = police.render(afficher_mot_cache(mot_a_deviner, lettres_trouvees), True, couleur_texte)
        fenetre.blit(texte_mot, (largeur_fenetre // 2 - texte_mot.get_width() // 2, hauteur_fenetre // 2 - texte_mot.get_height() // 2))

        pygame.display.flip()

        if "_" not in afficher_mot_cache(mot_a_deviner, lettres_trouvees):
            print("Félicitations! Vous avez deviné le mot: ", mot_a_deviner)
            enregistrer_score(difficulte, tentatives_max - tentatives)
            break

    if "_" in afficher_mot_cache(mot_a_deviner, lettres_trouvees):
        print("Dommage! Le mot était: ", mot_a_deviner)

# Fonction pour ajouter un mot au fichier
def ajouter_mot():
    nouveau_mot = input("Entrez un nouveau mot : ")
    with open("mots.txt", "a") as fichier_mots:
        fichier_mots.write("\n" + nouveau_mot)

# Fonction pour enregistrer le score
def enregistrer_score(difficulte, score):
    nom_joueur = input("Entrez votre nom : ")
    with open("scores.txt", "a") as fichier_scores:
        fichier_scores.write(f"{nom_joueur} - {difficulte.capitalize()} - Score: {score}\n")

# Fonction pour afficher le tableau des scores
def afficher_scores():
    if not os.path.exists("scores.txt"):
        print("Aucun score disponible.")
    else:
        with open("scores.txt", "r") as fichier_scores:
            scores = fichier_scores.read()
            print("Tableau des scores :\n", scores)

# Menu principal
while True:
    choix = input("1. Jouer au pendu\n2. Ajouter un mot\n3. Afficher le tableau des scores\n4. Quitter\nChoisissez une option : ")

    if choix == "1":
        difficulte = input("Choisissez le niveau de difficulté (facile, moyen, difficile) : ").lower()
        if difficulte in niveaux_difficulte:
            jouer_pendu(difficulte)
        else:
            print("Niveau de difficulté non valide. Veuillez choisir à nouveau.")
    elif choix == "2":
        ajouter_mot()
    elif choix == "3":
        afficher_scores()
    elif choix == "4":
        break
    else:
        print("Option non valide. Veuillez choisir à nouveau.")
