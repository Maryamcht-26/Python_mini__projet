from bibliotheque import Livre, Membre, Bibliotheque
from gestion_donnees import (
    sauvegarder_livres, sauvegarder_membres,
    charger_livres, charger_membres,
    ajouter_historique
)
from visualisations import (
    diagramme_par_genre,
    histogramme_auteurs,
    courbe_emprunts
)
from datetime import datetime
import os

# Répertoire racine du projet (dossier contenant src, data, etc.)
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DATA_DIR = os.path.join(ROOT_DIR, "data")
FICHIER_LIVRES = os.path.join(DATA_DIR, "livres.txt")
FICHIER_MEMBRES = os.path.join(DATA_DIR, "membres.txt")
FICHIER_HISTO = os.path.join(DATA_DIR, "historique.csv")

# Initialiser la bibliothèque
biblio = Bibliotheque()
biblio.livres = charger_livres()
biblio.membres = charger_membres(biblio.livres)

def menu():
    while True:
        print("\n=== GESTION BIBLIOTHÈQUE ===")
        print("1. Ajouter un livre")
        print("2. Inscrire un membre")
        print("3. Emprunter un livre")
        print("4. Rendre un livre")
        print("5. Lister tous les livres")
        print("6. Afficher les statistiques")
        print("7. Sauvegarder et quitter")
        choix = input("Votre choix : ").strip()

        try:
            if choix == "1":
                isbn = input("ISBN : ").strip()
                titre = input("Titre : ").strip()
                auteur = input("Auteur : ").strip()
                annee = input("Année : ").strip()
                genre = input("Genre : ").strip()
                livre = Livre(isbn, titre, auteur, annee, genre)
                biblio.ajouter_livre(livre)
                print(" Livre ajouté.")

            elif choix == "2":
                id_membre = input("ID du membre : ").strip()
                nom = input("Nom du membre : ").strip()
                membre = Membre(id_membre, nom)
                biblio.enregistrer_membre(membre)
                print(" Membre inscrit.")

            elif choix == "3":
                id_membre = input("ID du membre : ").strip()
                titre = input("Titre du livre : ").strip()
                biblio.emprunter_livre(id_membre, titre)
                livre = next((l for l in biblio.livres if l.titre.lower() == titre.lower()), None)
                if livre:
                    ajouter_historique(datetime.today().date(), livre.ISBN, id_membre, "emprunt")
                print(" Livre emprunté.")

            elif choix == "4":
                id_membre = input("ID du membre : ").strip()
                titre = input("Titre du livre : ").strip()
                biblio.rendre_livre(id_membre, titre)
                livre = next((l for l in biblio.livres if l.titre.lower() == titre.lower()), None)
                if livre:
                    ajouter_historique(datetime.today().date(), livre.ISBN, id_membre, "retour")
                print(" Livre rendu.")

            elif choix == "5":
                print("\n LIVRES DISPONIBLES :")
                for livre in biblio.livres:
                    statut = "emprunté" if livre.est_emprunte else "disponible"
                    print(f"- {livre.titre} ({livre.auteur}, {livre.annee}) [{statut}]")

            elif choix == "6":
                sauvegarder_livres(biblio.livres)
                sauvegarder_membres(biblio.membres)
                diagramme_par_genre(FICHIER_LIVRES)
                histogramme_auteurs(FICHIER_LIVRES)
                courbe_emprunts(FICHIER_HISTO)

            elif choix == "7":
                sauvegarder_livres(biblio.livres)
                sauvegarder_membres(biblio.membres)
                print(" Données sauvegardées.")
                break

            else:
                print("Choix invalide. Veuillez choisir un nombre entre 1 et 7.")

        except Exception as e:
            print("Erreur :", e)

if __name__ == "__main__":
    menu()
