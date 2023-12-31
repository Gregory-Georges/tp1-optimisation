"""
Monsieur Tartempion - Édition horrifique
420-5GP-BB, automne 2023, Collège Bois-de-Boulogne
Travail pratique 1
A
Ressources sous licences:
  522243__dzedenz__result-10.wav
  par DZeDeNZ, 2020-07-15
  Licence: https://creativecommons.org/publicdomain/zero/1.0/

  409282__wertstahl__syserr1v1-in_thy_face_short.wav
  par wertstahl, 2017-11-06
  Licence: https://creativecommons.org/licenses/by-nc/4.0/

  173859__jivatma07__j1game_over_mono.wav
  par jivatma07, 2013-01-11
  Licence: https://creativecommons.org/publicdomain/zero/1.0/

  550764__erokia__msfxp9-187_5-synth-loop-bpm-100.wav
  par Erokia, 2020-12-26
  Licence: https://creativecommons.org/licenses/by-nc/4.0/
"""






import random
import simpleaudio as audio
import time
import sqlite3 as sql
import PySimpleGUI as SimpleGui

from images import *
from indicateurs import Indicateur


NB_QUESTIONS = 21

police_title = (SimpleGui.DEFAULT_FONT, 40, 'italic')
police_etiquettes = (SimpleGui.DEFAULT_FONT, 20, 'normal')
police_temps = (SimpleGui.DEFAULT_FONT, 50, 'normal')
police_question = (SimpleGui.DEFAULT_FONT, 30, 'normal')
police_reponses = (SimpleGui.DEFAULT_FONT, 20, 'normal')
police_ou = (SimpleGui.DEFAULT_FONT, 20, 'italic')





####################################################
# Splasher
####################################################

#Affiche l'image en parametre
def splasher(image_data, par_dessus : bool, delais_ms : int, couleur_transparente=None) -> None:
    SimpleGui.Window('Monsieur Tartempion', image_data, transparent_color=couleur_transparente, no_titlebar=True, keep_on_top=par_dessus).read(timeout=delais_ms, close=True)


def splacher_titre(delai: int, pardessus: bool) -> None:
    splasher([[SimpleGui.Image(data=titre_base64())]], pardessus, delai)

def splasher_echec(temps_ms: int) -> None:
    splasher([[SimpleGui.Image(data=echec_base64())]], True, temps_ms, SimpleGui.theme_background_color())

def splasher_succes() -> None:
    splasher([[SimpleGui.Image(data=succes_base64())]], True, 3000, "maroon2")

def splasher_equipe(temps_ms: int) -> None:
    splasher([[SimpleGui.Image(data=equipe_base64())]], True, temps_ms)		# transparent_color=SimpleGui.theme_background_color()
    
    
    
    
    

####################################################
# Modifier l'interface
####################################################
    
def effacer_question_affichee(fenetre: SimpleGui.Window) -> None:
    fenetre['BOUTON-GAUCHE'].update('', disabled=True, visible=True)
    fenetre['QUESTION'].update("")
    fenetre['OU'].update(text_color=SimpleGui.theme_background_color())
    fenetre['BOUTON-DROIT'].update('', disabled=True, visible=True)
    
    
    
    
    
    
####################################################
# Manipulation des questions
####################################################

def charger_questions(fichier_db: str) -> list:

    connexion = sql.connect(fichier_db)
    
    with connexion:
        resultat_requete = connexion.execute('SELECT question, reponse_exacte, reponse_erronee FROM QUESTIONS')
    return [(enregistrement[0], enregistrement[1], enregistrement[2]) for enregistrement in resultat_requete]


def choisir_questions(banque: list, nombre: int) -> list:
    return [[question, Indicateur.VIDE] for question in random.choices(banque, k=nombre)]


def melanger_reponses(reponses: tuple) -> tuple:
    return (reponses[0], reponses[1]) if bool(random.getrandbits(1)) else (reponses[1], reponses[0])






###################################################
# Modification et affichage de l'interface
###################################################

def afficher(fenetre: SimpleGui.Window, question: tuple) -> None:
    fenetre['QUESTION'].update(question[0])
    reponses = melanger_reponses((question[1], question[2]))
    fenetre['BOUTON-GAUCHE'].update(reponses[0], disabled=False, visible=True)
    fenetre['OU'].update(text_color='white')
    fenetre['BOUTON-DROIT'].update(reponses[1], disabled=False, visible=True)



def effacer_question(fenetre: SimpleGui.Window) -> None:
    fenetre['QUESTION'].update('')
    fenetre['BOUTON-GAUCHE'].update('', disabled=True, visible=True)
    fenetre['OU'].update(text_color=SimpleGui.theme_background_color())
    fenetre['BOUTON-DROIT'].update('', disabled=True, visible=True)
    
    
    
def afficher_jeu() -> SimpleGui.Window:

    title = [SimpleGui.Text('Monsieur Tartempion', key='TITLE', font=police_title)]

    temps = [[SimpleGui.Text('Temps restant', font=police_etiquettes, size=70, justification='center')], [SimpleGui.Text(str(60), key='TEMPS', font=police_temps)]]

    boutons_reponse = [SimpleGui.Column([[SimpleGui.Button(key='BOUTON-GAUCHE', font=police_reponses, button_color=('white', SimpleGui.theme_background_color()),
                   border_width=0, disabled=True, visible=True),
        SimpleGui.Text(' ou ', key='OU', font=police_ou, text_color=SimpleGui.theme_background_color()),
        SimpleGui.Button(key='BOUTON-DROIT', font=police_reponses, button_color=('white', SimpleGui.theme_background_color()),
                   border_width=0, disabled=True, visible=True)]], element_justification='center')]

    question = [SimpleGui.Text(' ', key='QUESTION', font=police_question)]

    action = [SimpleGui.Button(image_data=bouton_jouer_base64(), key='BOUTON-ACTION', border_width=0, button_color=(SimpleGui.theme_background_color(), SimpleGui.theme_background_color()), pad=(0, 10)),
              SimpleGui.Image(data=bouton_inactif_base64(), key='IMAGE-BOUTON-INACTIF', visible=False, pad=(0, 10))]

    indicateurs = [*[SimpleGui.Image(data=indicateur_vide_base64(), key=f'INDICATEUR-{i}', pad=(4, 10)) for i in range(NB_QUESTIONS)]]

    fenetre = SimpleGui.Window('Monsieur Tartempion', [temps, boutons_reponse, question, action, indicateurs], keep_on_top=True, element_padding=(0, 0),
                        element_justification='center', resizable=False, finalize=True)

    return fenetre






###################################################
# Programme primcipal
###################################################

def programme_principal() -> None:
    """Despote suprême de toutes les fonctions."""

    SimpleGui.theme('Black')

    son_victoire = audio.WaveObject.from_wave_file('522243__dzedenz__result-10.wav')
    son_erreur = audio.WaveObject.from_wave_file('409282__wertstahl__syserr1v1-in_thy_face_short.wav')
    son_fin_partie = audio.WaveObject.from_wave_file('173859__jivatma07__j1game_over_mono.wav')
    musique_questions = audio.WaveObject.from_wave_file('550764__erokia__msfxp9-187_5-synth-loop-bpm-100.wav')

    splasher_equipe(1500)
    splacher_titre(2000, True)

    toutes_les_questions = charger_questions("questions.bd")
    questions = choisir_questions(toutes_les_questions, 21)

    fenetre = afficher_jeu()
    temps_restant = 60
    prochaine_question = 0
    decompte_actif = False

    quitter = False
    while not quitter:
        event, valeurs = fenetre.read(timeout=10)
        if decompte_actif:
            dernier_temps = temps_actuel
            temps_actuel = round(time.time())
            if dernier_temps != temps_actuel:
                temps_restant -= 1
                fenetre['TEMPS'].update(str(temps_restant))
                if temps_restant == 0:
                    decompte_actif = False
                    fenetre.hide()
                    effacer_question(fenetre)
                    for i in range(NB_QUESTIONS):
                        fenetre[f'INDICATEUR-{i}'].update(data=indicateur_vide_base64())
                    son_fin_partie.play()
                    musique_questions_controles.stop()
                    splasher_echec(3000)

                    fenetre['BOUTON-ACTION'].update(disabled=False, visible=True)
                    fenetre['IMAGE-BOUTON-INACTIF'].update(visible=False)
                    temps_restant = 60
                    fenetre['TEMPS'].update(str(temps_restant))
                    fenetre.un_hide()
                    questions = choisir_questions(toutes_les_questions, NB_QUESTIONS)
                    prochaine_question = 0
                    continue

        if event == 'BOUTON-ACTION':
            fenetre['BOUTON-ACTION'].update(disabled=True, visible=False)
            fenetre['IMAGE-BOUTON-INACTIF'].update(visible=True)
            temps_actuel = round(time.time())
            decompte_actif = True
            afficher(fenetre, questions[prochaine_question][0])
            musique_questions_controles = musique_questions.play()
        elif event == 'BOUTON-GAUCHE' or event == 'BOUTON-DROIT':
            if (event == 'BOUTON-GAUCHE' and fenetre['BOUTON-GAUCHE'].get_text() != questions[prochaine_question][0][1]) or \
               (event == 'BOUTON-DROIT' and fenetre['BOUTON-DROIT'].get_text() != questions[prochaine_question][0][1]):
                # le joueur a choisi la mauvaise réponse
                fenetre[f'INDICATEUR-{prochaine_question}'].update(data=indicateur_vert_base64())
                questions[prochaine_question][1] = Indicateur.VERT
                prochaine_question += 1
                if prochaine_question < NB_QUESTIONS:
                    afficher(fenetre, questions[prochaine_question][0])
                elif 21 <= prochaine_question:
                    decompte_actif = False
                    fenetre.hide()
                    effacer_question_affichee(fenetre)
                    for i in range(NB_QUESTIONS):
                        fenetre[f'INDICATEUR-{i}'].update(data=indicateur_vide_base64())
                        questions[i][1] = Indicateur.VIDE
                    musique_questions_controles.stop()
                    son_victoire.play()
                    splasher_succes()
                    fenetre['BOUTON-ACTION'].update(disabled=False, visible=True)
                    fenetre['IMAGE-BOUTON-INACTIF'].update(visible=False)
                    temps_restant = TEMPS_EPREUVE
                    fenetre['TEMPS'].update(str(temps_restant))
                    fenetre.un_hide()
                    questions = choisir_questions(toutes_les_questions, NB_QUESTIONS)
                    prochaine_question = 0
                    continue
            else:
                # le joueur a choisi la bonne réponse
                decompte_actif = False
                effacer_question(fenetre)
                for i in range(prochaine_question):
                    fenetre[f'INDICATEUR-{i}'].update(data=indicateur_jaune_base64())
                    questions[i][1] = Indicateur.JAUNE
                fenetre[f'INDICATEUR-{prochaine_question}'].update(data=indicateur_rouge_base64())
                questions[prochaine_question][1] = Indicateur.ROUGE
                prochaine_question = 0
                fenetre['BOUTON-ACTION'].update(disabled=False, visible=True)
                fenetre['IMAGE-BOUTON-INACTIF'].update(visible=False)
                son_erreur.play()
                musique_questions_controles.stop()
        elif event == SimpleGui.WIN_CLOSED:
            decompte_actif = False
            quitter = True

    fenetre.close()
    del fenetre



if __name__ == "__main__":
	programme_principal()
