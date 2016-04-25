#!/usr/bin/env python3
#title           : MemoryFlag.py
#description     : Petit jeu de memoire en ligne
#author          : Inès & Amélie 
#date            : Annee Scolaire 2015-2016 (Mars Avril 2016)
#version         : 5.5
#usage           : python MemoryFlag.py
#notes           : projet INS BAC 2016
#python_version  : 3.5.1  
#==============================================================================

# Import des modules necessaire a l'execution du script.
import random, sys    # On importe le module 'random' pour le placement des cartes soit aleatoire et le module 'sys' pour l'execution du script
from tkinter import * # On importe le module tkinter pour afficher une fenetre graphique


#_____________________________________________________#
#                                                     #
#    Definitions des toutes les fonctions du jeu      #  
#_____________________________________________________#


def MenuLevel():          # définition du menu de niveau 
    WindowDefLevel = Tk() # fenêtre du niveau
    label          = Label ( WindowDefLevel, 
                             text = "\nMEMORY FLAG \n \n Veuillez choisir votre niveau\n",
                             font = "President 20 bold italic",
                             fg = "purple")
    label.pack()
    liste          = Listbox ( WindowDefLevel, width=30, height=5 ) # creation d'une liste avec les différents niveaux

    liste.insert   ( 1, " Niveau Débutant (18 cartes)")
    liste.insert   ( 2, " Niveau Intermédiaire (30 cartes)")
    liste.insert   ( 3, " Niveau Expert (42 cartes)")
    liste.pack()          # permet d'afficher dans la fenetre le packaging 

    WindowDefLevel.title("Jeu 'MEMORY FLAG' ~ ISN 2015-2016 ~ Inès & Amélie ~ Séléction du niveau de difficulté") # titre de la première fenetre
	
    Button( WindowDefLevel,
            text    = ">> Valider le Choix du Niveau <<",
            cursor  = "heart",
            font    = "sans 12 bold",
            fg      = "green",
            command = lambda: CombineFuncs ( DefLevel 
                                         ( liste.curselection()),
                                           WindowDefLevel.destroy(), 
                                           ExecGame())).pack()
# Creation du bouton valider le choix du niveau sur la fenetre de definition du niveau, font = police de caractère, fg = couleur de la police, command= execution lors du clic; passage sur le plateau de carte (execgame) et destruction(destroy) de la fenetre de definitiondu niveau   
# La commande Lambda est très pratiques pour créer des fonctions, quand on a besoin d’une fonction, mais que l’on ne va l’utiliser qu’une seule fois.
# Car on peut définir et utiliser cette fonction "anonyme" d’une traite, ce qui évite l’écriture en deux temps.

    Button ( WindowDefLevel,
             text         = ">> Quitter le jeu <<",
             cursor       = "pirate",
             font         = "sans 12 bold italic",
             fg           = "red",
             command      = WindowDefLevel.destroy).pack()
#Creation du bouton quitter dans la fenetre de definition du niveau, font= police de caractère, fg=couleur de la police, command= execution lors du clic; passage sur le plateau de carte et destruction(destroy) de la fenetre de definitiondu niveau
    
    PicHome               = PhotoImage ( file = "Images\PicHome1.png")
    PageHome              = Canvas ( WindowDefLevel)
    PageHome.create_image ( 200 , 100, anchor=CENTER, image=PicHome) # Placement et positionement de l'image d'accueil par rapport au centre
    PageHome.pack()
#Insertion d'une image sur la première fenêtre

    WindowDefLevel.mainloop()

	
def DefLevel ( Choice ): # Definitions de la fonction du choix du niveau du jeu 	
    global NbLine, NbRow, LibLevel  #initialisation des varibles selon le niveau 
    
    if str(Choice)   == '(1,)': #str = string: caractères 
        NbLine       = 6
        NbRow        = 5
        LibLevel     = ' Niveau Intermédiaire '

    elif str(Choice) == '(2,)':
        NbLine       = 6
        NbRow        = 7
        LibLevel     = ' Niveau Expert '

    else:
        NbLine       = 2#6
        NbRow        = 2#3
        LibLevel     = ' Niveau Débutant' #Par défaut niveau débutant 
        return NbLine, NbRow

	
def ExecGame(): # Definitions de la fonction d'execution du jeu
    global NbTotalFlags, ViewFlag, RetunedFlags, Flag, WindowGame # Déclaration des variables global qui seront utilisées dans cette fonction 
	
    NbTotalFlags     = NbLine * NbRow   # calcule du nb de cartes selon le niveau choisi par l'utilisateur
    WindowGame       = Tk()   #fenetre de Definition du jeu
    WindowGame.title( " Jeu 'MEMORY FLAG' ~ ISN 2015-2016 ~ Inès & Amélie ~ "
                      + ( LibLevel ) ) # titre de la deuxième fenetre + libellé du niveau varible selon choix de l'utilisateur    
    Flag             = LoadFlag() # la liste Flag contient les images gif chargées (Le dos + le nombre total de cartes)
    RetunedFlags     = Flag[0]    # Le dos des cartes est l'image [0]    
    ViewFlag         = Canvas(WindowGame, width=770, height=650, bg='white smoke', bd=10, relief="ridge") #height= taille ; bg=background; relief=cadre initialisation de la fenetre graphique (WindowGame)	
    ViewFlag.pack()
    InitPlayGame() 	# Initialisation des données du jeu pour commencer jeux
    ViewFlag.bind( '<Button-1>', OnMouseClick ) # gestionnaire du clic de la souris

    Button ( WindowGame,
             text    = ">> Quitter le jeu <<",
             cursor  = "pirate",
             font    = "sans 12 bold ",
             fg      = "red",
             command = WindowGame.destroy).pack(side=TOP, padx=5, pady=5) 
#Creation du bouton quitter sur la fenetre du jeu, font= police de caractère, fg=couleur de la police, command= execution lors du clic => fermeture (destroy) de la fenetre principale du jeu    

    WindowGame.mainloop()     # boucle principale

	
def InitPlayGame():             # Définition de la fontion d'initialisation du jeu 
    global duree, NbFindFlags, FlagList, FlagsMixed  # Déclaration des variables global qui seront utilisées dans la fontion d'initialisation 
	
    duree                 = (1200)        # Parametrage de la durée à 1200 millisecondes
    NbFindFlags           = 0             # Initialisation du nombre de carte trouvée à zéro    
    FlagList              = InitDisplay() # la variable liste des cartes appel la fonction d'affichage des cartes
    FlagsMixed            = MixFlag()     # la variable cartes mélangées appel la fonction de mélange des cartes
    
    RAZMouseClick()


def InitDisplay ():      # Définition de la fontion d'initialisation de l'affichage du jeu
    global RetunedFlags  # Déclaration de la variable global carte à retourner utilisée dans la fontion d'initialisation

    ViewFlag.delete( ALL ) # la fenêtre de visualisation des drapeaux est effacée pour commencer à jouer
    liste_ids        = []       # boucle pour alimenter la liste des identifiants des cartes  
    for Row in range(NbLine):
        for Column in range( NbRow ):
            liste_ids.append ( ViewFlag.create_image ( 110*Column+10, 
                                                       110*Row+10,
                                                       anchor = NW,
                                                       image  = RetunedFlags,
                                                       tags   ="memory" ) )
 # Placement et positionement des cartes par rapport au coin haut et gauche

    return liste_ids


def LoadFlag ():     # Definition de la fontion du chargement des cartes sur le plateau
    NbFlag           = 1 + NbTotalFlags // 2
# Nombre de drapeaux correspond ou nombre de couple de carte / par 2 + 1 qui correspond au dos des cartes 
    Flag             = []
# Boucle pour allimanter la liste des images en GIF des drapeaux contenu dans le dossier Images\.... prefixé par img  
    for i in range(NbFlag): 
        Flag.append(PhotoImage(file="Images\img{}.gif".format(i)))
        
    return Flag


def MixFlag ():            # Définition de la fonction de mélange des cartes sur la fenetre du jeu

    liste            = list ( range ( 1, NbTotalFlags//2 + 1)) * 2
# Constitution de la liste contenant le couple des imgages plus le dos
    random.shuffle(liste)  # Utilisation du module aléatoire pour le mélange des cartes selectionnées
    return liste
 

def HideFlag ():  # Definition de la fontion des cartes masquées (donc retournées)
    ViewFlag.itemconfigure("memory", image=RetunedFlags)   
    RAZMouseClick()
    

def DeleteFlag ():  # Definition de la fonction de suppression du couple de cartes trouvées
    global NbFindFlags
    
    ViewFlag.delete ( FirstFlag )      # Suppression de la carte 1 trouvée
    ViewFlag.delete ( SecondFlag )     # Suppression de la carte 2 trouvée
    NbFindFlags       += 2             # Incrémentation de la variable de 2, car un couple à été trouvé
    
    if   NbFindFlags  >=  NbTotalFlags: #Condition si le nombre de couple trouvé est supérieur ou égale au nombre total de carte => message BRAVO si non mise à zéro du click souris pour continuer de jouer
        WellDone()                  # Appel de la fonction BRAVO
    else:
        RAZMouseClick()             # Appel de la fonction mise à zéro du clic souris


def RAZMouseClick (): # Definition de la fonction de mise à zéro du clic souris	
    global FirstFlag, SecondFlag
    
    FirstFlag = SecondFlag = 0


def OnMouseClick (clic): # Definition de la fonction du Gestionnaire des événements des clics de la souris
    global WindowGame, FirstFlag, SecondFlag
	
# Initialisation des coordonnées du clic X & Y de la souris
    x, y                 = clic.x, clic.y
# recherche des cartes 
    collisions = ViewFlag.find_overlapping(x, y, x, y)

# le joueur a-il cliqué sur une carte ?
    if collisions and collisions[0] in FlagList:
# Initialisation ID carte
        IdFlag           = collisions[0]
# première carte à retourner ?
        if FirstFlag     == 0:
# Initialisation des identifiants des cartes
            FirstFlag    = IdFlag
            SecondFlag   = 0
            ShowFlag    ( FirstFlag )
# deuxième carte à retourner ?
        elif SecondFlag  == 0 and IdFlag != FirstFlag:
# init ID carte
            SecondFlag   = IdFlag
            ShowFlag     ( SecondFlag )
# Si correspondance trouvée ?
            if MatchFlag ( FirstFlag, SecondFlag ):
# Alors supprimer le couple de cartes au bout de 1200 millisecondes
                WindowGame.after ( duree, DeleteFlag )           
            else:
# Si pas de correspondance trouvée
# retourner les cartes au bout de 1200 millisecondes
                WindowGame.after ( duree, HideFlag )


def ShowFlag ( IdFlag ):  # Definition de la fonction d'affichage de la carte correspondant à l'identifiant
    ViewFlag.itemconfigure ( IdFlag, 
                             image = Flag[ValueFlag(IdFlag)]) # Retourne la valeur de la carte correspondant à l'ID de canvasItem"


def ValueFlag (IdFlag): # Definition de la fonction d'affectation d'une valeur à la carte 
    index  = FlagList.index(IdFlag)     # initialisation de l'index des cartes  
    return   FlagsMixed[index]     # valeur carte à cet emplacement lors du mélange


def MatchFlag   ( ClickFirstFlag, ClickSecondFlag):     # Definition de la fonction de vérification de la correspondance entre les deux cartes
    return bool ( ValueFlag ( ClickFirstFlag ) == ValueFlag ( ClickSecondFlag ))

	
def WellDone ():         # Definition de la fonction de fin de la partie pour l'affichage des messages de félicitation
    ViewFlag.delete(ALL) # On efface d'abord la fenetre du jeu
    x, y = ViewFlag.winfo_reqwidth()//2, ViewFlag.winfo_reqheight()//2 # determination du point central de la fenetre du jeux

# affichage des messages de fin de jeu. Les messages sont placés selon les coordonnées de X et Y

    ViewFlag.create_text(x,     y-250, text= " Partie terminée ",                         font="sans 20 bold",        fill="hotpink") 
    ViewFlag.create_text(x,     y-200, text= " Félicitations ! ",                         font="sans 20 bold",        fill="hotpink")
    ViewFlag.create_text(x,     y+70,  text= " Jeu créé par Inès & Amélie ",              font="sans 10",             fill="Black")
    ViewFlag.create_text(x,     y+90,  text= " Projet ISN (Année scolaire 2015-2016) ",   font="sans 10",             fill="Black")
    ViewFlag.create_text(x,     y,     text= " Une autre partie ? ", 		              font="sans 15 bold italic", fill="hotpink")
    ViewFlag.create_text(x+310, y+305, text= "© Inès & Amélie ",                          font="sans 10 italic",      fill="Black")
    
    ViewFlag.create_window ( x, y+40,
                             window = Button ( ViewFlag,
                    						    text = "  ~> Ici <~ ",
												cursor = "heart",
                    							font = "sans 10 bold",
												fg = "deep pink",
												command=lambda: CombineFuncs ( WindowGame.destroy(),
                                 											   MenuLevel( )
																			  )
											 )
							)
# Creation du bouton rejouer sur la fenetre du jeu, font= police de caractère, fg=couleur de la police, command= execution lors du clic; fermeture (destroy) de la fenetre principale du jeu et retour au menu du niveau 
# La commande Lambda est très pratiques pour créer des fonctions, quand on a besoin d’une fonction, mais que l’on ne va l’utiliser qu’une seule fois.
# Car on peut définir et utiliser cette fonction "anonyme" d’une traite, ce qui évite l’écriture en deux temps.

def CombineFuncs(self, *funcs):  # Definitionde la fonction avec une combinaison de fonctions afin d'executer similtanément deux actions 

    def CombinedFunc ( *args, **kwargs):
        for f in funcs: # Boucle de la conbinaison des fonctions
            f( *args, **kwargs)

    return CombinedFunc
#CombineFuncs est configuré dans le script, pour être plus propre nous aurions du le configurer dans les scripts de config de python.

if __name__ == "__main__": # Nécessaire au fonctionnement du jeu dans sa globalité, sans ses deux lignes le jeu ne tournerait pas
    MenuLevel()     # Cela va permettre de se servir d'un module en tant que script, sans avoir à l'importer dans la console.
#Et être intégré à un programme.
