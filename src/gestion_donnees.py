import pandas as pd
import os

# Répertoire racine du projet (dossier contenant src, data, etc.)
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DATA_DIR = os.path.join(ROOT_DIR, "data")

def sauvegarder_livres(livres):
    tableau = []
    for livre in livres:
        statut = "emprunté" if livre.est_emprunte else "disponible"
        ligne = [livre.ISBN, livre.titre, livre.auteur, livre.annee, livre.genre, statut]
        tableau.append(ligne)

    df = pd.DataFrame(tableau, columns=["ISBN", "titre", "auteur", "annee", "genre", "statut"])
    chemin = os.path.join(DATA_DIR, "livres.txt")
    try:
        df.to_csv(chemin, sep=';', index=False, encoding='utf-8')
        print(f" Livres sauvegardés dans {chemin}")
    except Exception as e:
        print(f"Impossible de sauvegarder livres : {e}")

def charger_livres():
    from bibliotheque import Livre
    livres = []
    chemin = os.path.join(DATA_DIR, "livres.txt")
    try:
        df = pd.read_csv(chemin, sep=';', encoding='utf-8')
        for _, ligne in df.iterrows():
            livre = Livre(
                ligne["ISBN"],
                ligne["titre"],
                ligne["auteur"],
                ligne["annee"],
                ligne["genre"]
            )
            livre.est_emprunte = (str(ligne["statut"]).strip().lower() == "emprunté")
            livres.append(livre)
        print(f"Livres chargés depuis {chemin}")
    except FileNotFoundError:
        print(f" Fichier {chemin} non trouvé, liste livres vide")
    except Exception as e:
        print(f" Impossible de charger livres : {e}")
    return livres

def sauvegarder_membres(membres):
    tableau = []
    for m in membres:
        titres = ",".join([l.titre for l in m.livres_empruntes])
        ligne = [m.ID, m.nom, titres]
        tableau.append(ligne)

    df = pd.DataFrame(tableau, columns=["ID", "nom", "livres_empruntes"])
    chemin = os.path.join(DATA_DIR, "membres.txt")
    try:
        df.to_csv(chemin, sep=';', index=False, encoding='utf-8')
        print(f" Membres sauvegardés dans {chemin}")
    except Exception as e:
        print(f" Impossible de sauvegarder membres : {e}")

def charger_membres(livres):
    from bibliotheque import Membre
    membres = []
    chemin = os.path.join(DATA_DIR, "membres.txt")
    try:
        df = pd.read_csv(chemin, sep=';', encoding='utf-8')
        for _, ligne in df.iterrows():
            m = Membre(ligne["ID"], ligne["nom"])
            titres = ligne["livres_empruntes"].split(",") if pd.notna(ligne["livres_empruntes"]) else []
            for titre in titres:
                for l in livres:
                    if l.titre == titre:
                        m.livres_empruntes.append(l)
                        l.est_emprunte = True
            membres.append(m)
        print(f" Membres chargés depuis {chemin}")
    except FileNotFoundError:
        print(f" Fichier {chemin} non trouvé, liste membres vide")
    except Exception as e:
        print(f" Impossible de charger membres : {e}")
    return membres

def ajouter_historique(date, isbn, id_membre, action):
    historique_path = os.path.join(DATA_DIR, "historique.csv")
    ligne = pd.DataFrame([[date, isbn, id_membre, action]], columns=["date", "ISBN", "ID_membre", "action"])
    try:
        if os.path.exists(historique_path):
            ligne.to_csv(historique_path, mode='a', index=False, header=False, encoding='utf-8')
        else:
            ligne.to_csv(historique_path, mode='w', index=False, encoding='utf-8')
        print(f" Historique mis à jour : {action} {isbn} par {id_membre} le {date}")
    except Exception as e:
        print(f" Impossible de mettre à jour historique : {e}")
