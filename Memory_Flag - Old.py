#!/usr/bin/env python3
#title           : Memory_Flag.py
#description     : Petit jeu de mémoire en ligne
#author          : Inès & Amélie 
#date            : année scolaire 2015-2016 (Mars Avril 2016)
#version         : 5.1
#usage           : python Memory_Flag.py
#notes           : projet INS BAC 2016
#python_version  : 3.5.1
#=======================================================================

# Import des modules nécessaire à l'execution du script.
import random
from tkinter import *  # le programme va aller chercher toutes les fonctions de la bibliothèque Tkinter
import sys

 
#  Définition des principales fonction du jeu				   
# =================================================

#   Affichage du menu
  
def menu_choix_niveau():
    global niveau, nb_lignes, nb_colonnes,lib_niveau
    nb_lignes = 0
    nb_colonnes = 0
	
    print ("Bonjour,\nVous allez jouer au MEMORY FLAG\n")
    print ("Merci de choisir le niveau souhaité:\n")
    print ("1. Niveau Facile (12 cartes)")
    print ("2. Niveau Intermédiaire (20 cartes)")
    print ("3. Niveau Expert (30 cartes)")

    niveau = input(" >>  ")
    choix_niveau(niveau)
    return

def choix_niveau(niveau):
     global ch
     ch = niveau

# Initialisation de l'affichage du plateau ==> tout est "mis à zéro"_

def initialisation_du_jeu ():
    global duree, nb_de_cartes_retournees, liste_des_cartes, cartes_melangees
    duree = (1200) 
    nb_de_cartes_retournees = 0
    liste_des_cartes = initialisation_affichage()
    cartes_melangees = melange_des_cartes()
    mise_a_zero_clics_souris()

def initialisation_affichage ():
    affichage_des_cartes.delete(ALL)
    liste_tags = []
    for ligne in range(nb_lignes):
        for colonne in range(nb_colonnes):
            liste_tags.append(affichage_des_cartes.create_image( 110*colonne+10, 110*ligne+10, anchor=NW, image=carte_retournee, tags="memory",))
    return liste_tags

# Chargement des images sur le plateau 
def chargement_des_images ():
    nb_images = 1 + nb_total_cartes // 2
    images = []
    for i in range(nb_images):
        images.append(PhotoImage(file="Images\img{}.gif".format(i)))
    return images

#  Mélange de la position des images sur le plateau 
def melange_des_cartes ():
    liste = list(range(1, nb_total_cartes//2 + 1)) * 2
    random.shuffle(liste)
    return liste
    
#  Les images sont retournées sur le plateau 
def masquer_cartes ():
    affichage_des_cartes.itemconfigure("memory", image=carte_retournee)
    mise_a_zero_clics_souris()
    
#  Si deux images identiques sont retournées elles sont effacée du plateau 
def suppression_cartes ():
    global nb_de_cartes_retournees
    affichage_des_cartes.delete(carte_une)
    affichage_des_cartes.delete(carte_deux)
    nb_de_cartes_retournees += 2
    if nb_de_cartes_retournees >= nb_total_cartes:
        bravo()
    else:
        mise_a_zero_clics_souris()
        
#  Fin de la partie, affichage des messages 
def bravo ():
# on commence par tout effacer
    affichage_des_cartes.delete(ALL)

# determination du point central de la fenêtre du jeux
    x, y = affichage_des_cartes.winfo_reqwidth()//2, affichage_des_cartes.winfo_reqheight()//2

# affichage des messages de fin de jeu
    affichage_des_cartes.create_text(x,      y+70,  text= "Jeu créé par Inès & Amélie",               font="sans 10",             fill="Black")
    affichage_des_cartes.create_text(x,      y+90,  text= "Projet ISN (Année scolaire 2015-2016)",    font="sans 10",             fill="Black")
    affichage_des_cartes.create_text(x+220,  y+315, text= "© Inès & Amélie",                          font="sans 10 italic",      fill="Black")
    affichage_des_cartes.create_text(x,      y-250, text="Partie terminée",                           font="sans 20 bold",        fill="hotpink")
    affichage_des_cartes.create_text(x,      y-200, text="Félicitations",                             font="sans 20 bold",        fill="hotpink")
    affichage_des_cartes.create_text(x,      y,     text=" Une autre partie de " +(lib_niveau)+ " ?", font="sans 15 bold italic", fill="hotpink")
    
# Création du bouton rejouer
    affichage_des_cartes.create_window(x, y+40, window = Button(affichage_des_cartes, text="  ~> Ici <~ ", font="sans 10 bold", command = initialisation_du_jeu),)


	
#  Remise à zéro des clics souris

def mise_a_zero_clics_souris ():
    global carte_une, carte_deux
    carte_une = carte_deux = 0

#gestionnaire événements clics souris

def sur_clic_souris (clic):
    global carte_une, carte_deux

# init coordonnées clic X & Y de la souris
    x, y = clic.x, clic.y
    
# recherche de carte
    collisions = affichage_des_cartes.find_overlapping(x, y, x, y)
    
# le joueur a cliqué sur une carte ?
    if collisions and collisions[0] in liste_des_cartes:
		
# init ID carte
        id_carte = collisions[0]
        
# première carte à retourner ?
        if carte_une == 0:
			
# init IDs cartes
            carte_une = id_carte
            carte_deux = 0
            afficher_carte(carte_une)
            
# deuxième carte à retourner ?
        elif carte_deux == 0 and id_carte != carte_une:
			
# init ID carte
            carte_deux = id_carte
            afficher_carte(carte_deux)

# Si correspondance trouvée ?

            if correspondance(carte_une, carte_deux):

# Alors supprimer les cartes au bout d'un délai
                Plateau.after(duree, suppression_cartes)           
            else:
# Si non si pas de correspondance trouvée
# retourner les cartes au bout d'une certaine durée
                Plateau.after(duree, masquer_cartes)

#affiche la carte correspondant à l'ID de canvasItem"
def afficher_carte (id_carte):
 # affichage carte
    affichage_des_cartes.itemconfigure(id_carte, image=images[valeur_carte(id_carte)])
    
#retourne la valeur de la carte correspondant à l'ID de canvasItem

def valeur_carte (id_carte):
# init index carte
    index = liste_des_cartes.index(id_carte)
# valeur carte à cet emplacement
    return cartes_melangees[index]

# vérifie la correspondance entre les deux cartes"
def correspondance (clic_carte_1, clic_carte_2):
    return bool(valeur_carte(clic_carte_1) == valeur_carte(clic_carte_2))
	
# =======================
#      Programme principal
# =======================
if __name__ == "__main__":

# Launch main menu
    menu_choix_niveau()

# ----- variables globales
# Nombre de cartes du jeu [lignes x colonnes]
    
    if ch == '1':
         nb_lignes = 4
         nb_colonnes = 3
         lib_niveau = 'Niveau Facile'
    elif ch == '2':
        nb_lignes = 5
        nb_colonnes = 4
        lib_niveau = 'Niveau Intermédiaire'
    elif ch == '3':
        nb_lignes = 6
        nb_colonnes = 5
        lib_niveau = 'Niveau Expert'
    if ch not in ['1','2','3','0','9']:
        lib_niveau = 'mauvais niveau!'
        print("\n Merci de choisir le bon niveau")
    print("\n Vous avez choisi le "+str(lib_niveau))
    print(	" Avec "+str(nb_lignes)+ " lignes & "+str(nb_colonnes)+" colonnes")
    nb_total_cartes = nb_lignes * nb_colonnes
    
    # fenêtre principale
    Plateau = Tk() # vous pouvez choisir le nom que vous voulez pour votre fenêtre
    
    Plateau.title( "Jeu 'MEMORY FLAG' ~ ISN 2015-2016 ~ Inès & Amélie ~ " + (lib_niveau) ) 
    
    Plateau.resizable(width=True, height=True)
    
    # la liste images contient les x images gif (Le dos + x autres images)
    images = chargement_des_images()
    
    # init dos carte
    carte_retournee = images[0]
    
    # init plateau graphique
    affichage_des_cartes = Canvas(Plateau, width=550, height=650, bg='white',bd=5, relief="ridge")
	
	# Le widget Canvas (canevas, en français) est une zone de dessin rectangulaire.
    # Notons que l'angle haut gauche du canevas est l'origine des coordonnées (x,y)=(0,0).
	# Quelques propriétés de l'objet Canvas[modifier | modifier le wikicode]
    # Les propriétés sont définies en paramètre lors de la construction de l'objet
    # height : Hauteur Y du canvas
    # width  : Largeur X du canvas
    # bg  : Couleur de fond du canvas
    # bd  : Taille en pixels du bord du canvas (2 par défaut)
    # relief : Style de la bordure (flat (par défaut),raised,sunken,groove,ridge)

    affichage_des_cartes.pack()
    
    # init données jeu
    initialisation_du_jeu()
    
    # gestionnaire clics souris
    affichage_des_cartes.bind('<Button-1>', sur_clic_souris)
    
    # Création du bouton quitter
    Button  ( Plateau, text=">> Quitter le jeu <<", font="sans 12 bold ", command=Plateau.destroy).pack(padx=5, pady=5)
    
    # boucle principale
    Plateau.mainloop()
