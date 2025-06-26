
# Gestion de Bibliothèque 

**Auteur** : Maryam Chtioui (etudiante ENSAO)

## Guide d'installation

1. **Cloner le dépôt** :
   ```bash
   git clone https://github.com/Maryamcht-26/Python_mini__projet.git
   cd Python_mini_projet
   ```

2. **Créer un environnement virtuel (optionnel mais recommandé)** :
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # sous Linux/macOS
   .venv\Scripts\activate   # sous Windows
   ```

3. **Installer les dépendances** :
   ```bash
   pip install -r requirements.txt
   ```

4. **Lancer l'application** :
   ```bash
   python src/interface_main.py
   python src/main.py   ```

## Exemples d'utilisation

### 1. Interface graphique

- Gérer les livres : ajouter, afficher, supprimer
- Gérer les membres : inscrire un nouvel adhérent
- Emprunter / rendre un livre
- Visualiser les statistiques : diagrammes, histogrammes et courbes

### 2. Interface console 
- Accessible via `src/main.py`
- Permet les mêmes opérations sans interface graphique

##  Structure du projet

- `src/` : Code source principal (interface, console, logique métier,exceptions)
- `data/` : Données enregistrées (livres.txt, membres.txt, historique.csv)
-`docs/`   : Rapport de projet
-`assets/`:Images statistiques, vidéo de démonstration, diagramme UML
- `README.md` : Guide d'installation et d'utilisation
- `requirements.txt` : Dépendances Python à installer

---
> Ce projet utilise `Tkinter` pour l'interface graphique et `matplotlib`/`pandas` pour les statistiques.
