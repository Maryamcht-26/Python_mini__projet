import matplotlib.pyplot as plt
import pandas as pd
from collections import Counter
from datetime import datetime, timedelta

def diagramme_par_genre(fichier_livres, return_fig=False):
    try:
        df = pd.read_csv(fichier_livres, sep=';')
        genres = df['genre'].dropna()
        compteur = Counter(genres)
        fig, ax = plt.subplots(figsize=(5, 5))
        ax.pie(compteur.values(), labels=compteur.keys(), autopct='%1.1f%%')
        ax.set_title("Répartition des livres par genre")
        if return_fig:
            return fig
        else:
            plt.show()
    except Exception as e:
        print("Erreur lors de la génération du diagramme par genre:", e)

def histogramme_auteurs(fichier_livres, return_fig=False):
    try:
        df = pd.read_csv(fichier_livres, sep=';')
        auteurs = df['auteur'].dropna()
        compteur = Counter(auteurs)
        top = compteur.most_common(10)
        if top:
            noms, nombres = zip(*top) # je dois comprendre ca
            fig, ax = plt.subplots(figsize=(8, 4))
            ax.bar(noms, nombres, color='purple')
            ax.set_xticklabels(noms, rotation=45) #aussi ca
            ax.set_title("Top 10 des auteurs les plus populaires")
            fig.tight_layout()
            if return_fig:
                return fig
            else:
                plt.show()
    except Exception as e:
        print("Erreur lors de la génération de l'histogramme des auteurs:", e)

def courbe_emprunts(fichier_historique, return_fig=False):
    try:
        df = pd.read_csv(fichier_historique)
        df['date'] = pd.to_datetime(df['date']) #aussi ca
        df = df[df['action'] == 'emprunt']
        aujourd_hui = datetime.today()
        il_y_a_30_jours = aujourd_hui - timedelta(days=30)#aussi ca
        df_30 = df[df['date'] >= il_y_a_30_jours]
        compte_par_jour = df_30['date'].dt.strftime('%d/%m').value_counts().sort_index() #aussi ca

        dates = pd.date_range(start=il_y_a_30_jours, end=aujourd_hui)
        labels = [d.strftime('%d/%m') for d in dates] #aussi ca
        valeurs = [compte_par_jour.get(label, 0) for label in labels]

        fig, ax = plt.subplots(figsize=(10, 4))
        ax.plot(labels, valeurs, marker='o')
        ax.set_xticklabels(labels, rotation=45)
        ax.set_title("Activité des emprunts (30 derniers jours)")
        fig.tight_layout()
        if return_fig:
            return fig
        else:
            plt.show()
    except Exception as e:
        print("Erreur lors de la génération de la courbe des emprunts:", e)
