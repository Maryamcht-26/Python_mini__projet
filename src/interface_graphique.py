import tkinter as tk
from tkinter import ttk, messagebox
from bibliotheque import Livre, Membre, Bibliotheque
from gestion_donnees import (
    charger_livres, charger_membres, sauvegarder_livres, sauvegarder_membres, ajouter_historique
)
from visualisations import diagramme_par_genre, histogramme_auteurs, courbe_emprunts
from datetime import datetime
import os
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DATA_DIR = os.path.join(ROOT_DIR, "data")

class InterfaceBibliotheque(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("📚 Bibliothèque")
        self.geometry("1250x720")
        self.configure(bg="#ffffff")
        self.resizable(False, False)

        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure("TFrame", background="#ffffff")
        style.configure("Header.TLabel", font=("Segoe UI", 24, "bold"), foreground="#2c3e50", background="#ffffff")
        style.configure("Sidebar.TFrame", background="#2980b9")
        style.configure("Sidebar.TLabel", font=("Segoe UI", 14, "bold"), foreground="#ecf0f1", background="#2980b9")
        style.map("Sidebar.TLabel",
                  background=[("active", "#3498db")],
                  foreground=[("active", "#ffffff")])
        style.configure("Primary.TButton",
                        font=("Segoe UI Semibold", 12),
                        padding=8,
                        background="#2980b9",
                        foreground="white",
                        borderwidth=0)
        style.map("Primary.TButton",
                  background=[("active", "#1c5980")],
                  foreground=[("active", "white")])
        style.configure("Treeview", font=("Segoe UI", 11))

        # Charger données
        self.biblio = Bibliotheque()
        self.biblio.livres = charger_livres()
        self.biblio.membres = charger_membres(self.biblio.livres)

        self.main_frame = ttk.Frame(self)
        self.main_frame.pack(fill='both', expand=True)

        self.sidebar = ttk.Frame(self.main_frame, style="Sidebar.TFrame", width=260)
        self.sidebar.pack(side="left", fill="y")

        self.content_frame = ttk.Frame(self.main_frame)
        self.content_frame.pack(side="right", fill="both", expand=True, padx=25, pady=25)

        self.label_titre = ttk.Label(self.content_frame, text="📚 Interface Bibliothèque", style="Header.TLabel")
        self.label_titre.pack(pady=(0, 25))

        boutons = [
            ("📖 Livres", self.creer_onglet_livres),
            ("👥 Membres", self.creer_onglet_membres),
            ("🔁 Emprunts", self.creer_onglet_emprunts),
            ("📈 Statistiques", self.creer_onglet_statistiques)
        ]

        for text, command in boutons:
            lbl = ttk.Label(self.sidebar, text=text, style="Sidebar.TLabel", anchor="w", cursor="hand2", padding=15)
            lbl.pack(fill="x", pady=5)
            lbl.bind("<Enter>", lambda e, l=lbl: l.configure(background="#3498db"))
            lbl.bind("<Leave>", lambda e, l=lbl: l.configure(background="#2980b9"))
            lbl.bind("<Button-1>", lambda e, c=command: self.afficher_page(c))

        self.afficher_page(self.creer_onglet_livres)

    def afficher_page(self, creator):
        for widget in self.content_frame.winfo_children():
            if widget != self.label_titre:
                widget.destroy()
        titre = creator.__name__.replace("creer_onglet_", "").capitalize()
        self.label_titre.config(text=f"{titre}")
        creator(self.content_frame)

    def creer_onglet_livres(self, parent):
        form = ttk.Frame(parent)
        form.pack(pady=10)
        self.entrees_livre = {}
        colonnes = ["ISBN", "Titre", "Auteur", "Année", "Genre"]
        for i, champ in enumerate(colonnes):
            ttk.Label(form, text=champ).grid(row=i, column=0, padx=10, pady=5, sticky='e')
            entry = ttk.Entry(form, width=40)
            entry.grid(row=i, column=1, pady=5)
            self.entrees_livre[champ] = entry

        ttk.Button(form, text="Ajouter", style="Primary.TButton", command=self.ajouter_livre).grid(row=0, column=2, rowspan=5, padx=20, pady=10)

        self.table_livres = ttk.Treeview(parent, columns=colonnes, show="headings", height=15)
        for c in colonnes:
            self.table_livres.heading(c, text=c)
            self.table_livres.column(c, width=160, anchor="center")
        self.table_livres.pack(fill="both", expand=True, pady=20)

        ttk.Button(parent, text="Supprimer le livre sélectionné", style="Primary.TButton", command=self.supprimer_livre_selectionne).pack(pady=5)

        self.remplir_table_livres()

    def supprimer_livre_selectionne(self):
        selection = self.table_livres.selection()
        if not selection:
            messagebox.showwarning("Aucune sélection", "Veuillez sélectionner un livre à supprimer.")
            return

        reponse = messagebox.askyesno("Confirmation", "Voulez-vous vraiment supprimer ce livre ?")
        if not reponse:
            return

        try:
            item = self.table_livres.item(selection[0])
            valeurs = item['values']
            isbn = valeurs[0]
            livre_a_supprimer = next(l for l in self.biblio.livres if l.ISBN == isbn)
            self.biblio.supprimer_livre(livre_a_supprimer)
            self.remplir_table_livres()
            sauvegarder_livres(self.biblio.livres)
            messagebox.showinfo("Succès", "Le livre a été supprimé avec succès.")
        except Exception as e:
            messagebox.showerror("Erreur", str(e))

    def creer_onglet_membres(self, parent):
        form = ttk.Frame(parent)
        form.pack(pady=10)

        ttk.Label(form, text="ID").grid(row=0, column=0, padx=10, pady=5, sticky='e')
        self.entree_id_membre = ttk.Entry(form, width=40)
        self.entree_id_membre.grid(row=0, column=1, pady=5)

        ttk.Label(form, text="Nom").grid(row=1, column=0, padx=10, pady=5, sticky='e')
        self.entree_nom_membre = ttk.Entry(form, width=40)
        self.entree_nom_membre.grid(row=1, column=1, pady=5)

        ttk.Button(form, text="Inscrire", style="Primary.TButton", command=self.inscrire_membre).grid(row=0, column=2, rowspan=2, padx=20, pady=10)

        self.table_membres = ttk.Treeview(parent, columns=["ID", "Nom"], show="headings", height=15)
        self.table_membres.heading("ID", text="ID")
        self.table_membres.heading("Nom", text="Nom")
        self.table_membres.column("ID", width=200, anchor="center")
        self.table_membres.column("Nom", width=400, anchor="center")
        self.table_membres.pack(fill="both", expand=True, pady=20)
        self.remplir_table_membres()

    def creer_onglet_emprunts(self, parent):
        form = ttk.Frame(parent)
        form.pack(pady=10)

        ttk.Label(form, text="ID Membre").grid(row=0, column=0, padx=10, pady=5, sticky='e')
        self.entree_id_emprunt = ttk.Entry(form, width=40)
        self.entree_id_emprunt.grid(row=0, column=1, pady=5)

        ttk.Label(form, text="Titre Livre").grid(row=1, column=0, padx=10, pady=5, sticky='e')
        self.entree_titre_emprunt = ttk.Entry(form, width=40)
        self.entree_titre_emprunt.grid(row=1, column=1, pady=5)

        btn_frame = ttk.Frame(form)
        btn_frame.grid(row=0, column=2, rowspan=2, padx=20, pady=5)
        ttk.Button(btn_frame, text="Emprunter", style="Primary.TButton", command=self.emprunter_livre).pack(fill="x", pady=(0, 5))
        ttk.Button(btn_frame, text="Rendre", style="Primary.TButton", command=self.rendre_livre).pack(fill="x")

        colonnes = ["ISBN", "Titre", "Statut"]
        self.table_livres_emprunts = ttk.Treeview(parent, columns=colonnes, show="headings", height=15)
        for c in colonnes:
            self.table_livres_emprunts.heading(c, text=c)
            self.table_livres_emprunts.column(c, width=300 if c != "Statut" else 150, anchor="center")
        self.table_livres_emprunts.pack(fill="both", expand=True, pady=20)

        self.remplir_table_disponibilite_livres()

    def creer_onglet_statistiques(self, parent):
        btn_frame = ttk.Frame(parent)
        btn_frame.pack(pady=10)
        largeur_btn = 20
        ttk.Button(btn_frame, text="Diagramme par genre", width=largeur_btn, style="Primary.TButton", command=self.afficher_diagramme_par_genre).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Top auteurs", width=largeur_btn, style="Primary.TButton", command=self.afficher_histogramme_auteurs).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Courbe des emprunts", width=largeur_btn, style="Primary.TButton", command=self.afficher_courbe_emprunts).pack(side="left", padx=5)

        self.frame_graph = ttk.Frame(parent)
        self.frame_graph.pack(fill='both', expand=True, pady=20)

    def _clear_frame_graph(self):
        for widget in self.frame_graph.winfo_children():
            widget.destroy()

    def _afficher_figure(self, figure):
        canvas = FigureCanvasTkAgg(figure, master=self.frame_graph)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True)

    def afficher_diagramme_par_genre(self):
        self._clear_frame_graph()
        fig = diagramme_par_genre(os.path.join(DATA_DIR, "livres.txt"), return_fig=True)
        self._afficher_figure(fig)

    def afficher_histogramme_auteurs(self):
        self._clear_frame_graph()
        fig = histogramme_auteurs(os.path.join(DATA_DIR, "livres.txt"), return_fig=True)
        self._afficher_figure(fig)

    def afficher_courbe_emprunts(self):
        self._clear_frame_graph()
        fig = courbe_emprunts(os.path.join(DATA_DIR, "historique.csv"), return_fig=True)
        self._afficher_figure(fig)

    def ajouter_livre(self):
        try:
            infos = [entry.get().strip() for entry in self.entrees_livre.values()]
            if any(not i for i in infos):
                raise ValueError("Tous les champs doivent être remplis.")
            livre = Livre(*infos)
            self.biblio.ajouter_livre(livre)
            self.remplir_table_livres()
            for entry in self.entrees_livre.values():
                entry.delete(0, 'end')
            sauvegarder_livres(self.biblio.livres)
        except Exception as e:
            messagebox.showerror("Erreur", str(e))

    def inscrire_membre(self):
        try:
            ID = self.entree_id_membre.get().strip()
            nom = self.entree_nom_membre.get().strip()
            if not ID or not nom:
                raise ValueError("Tous les champs doivent être remplis.")
            membre = Membre(ID, nom)
            self.biblio.enregistrer_membre(membre)
            self.remplir_table_membres()
            self.entree_id_membre.delete(0, 'end')
            self.entree_nom_membre.delete(0, 'end')
            sauvegarder_membres(self.biblio.membres)
        except Exception as e:
            messagebox.showerror("Erreur", str(e))

    def emprunter_livre(self):
        ID = self.entree_id_emprunt.get().strip()
        titre = self.entree_titre_emprunt.get().strip()
        try:
            self.biblio.emprunter_livre(ID, titre)
            livre = next(l for l in self.biblio.livres if l.titre == titre)
            ajouter_historique(datetime.today().date(), livre.ISBN, ID, "emprunt")
            sauvegarder_livres(self.biblio.livres)
            sauvegarder_membres(self.biblio.membres)
            messagebox.showinfo("Succès", f"Le livre '{titre}' a été emprunté par {ID}.")
            self.remplir_table_disponibilite_livres()
        except Exception as e:
            messagebox.showerror("Erreur", str(e))

    def rendre_livre(self):
        ID = self.entree_id_emprunt.get().strip()
        titre = self.entree_titre_emprunt.get().strip()
        try:
            self.biblio.rendre_livre(ID, titre)
            livre = next(l for l in self.biblio.livres if l.titre == titre)
            ajouter_historique(datetime.today().date(), livre.ISBN, ID, "retour")
            sauvegarder_livres(self.biblio.livres)
            sauvegarder_membres(self.biblio.membres)
            messagebox.showinfo("Succès", f"Le livre '{titre}' a été rendu par {ID}.")
            self.remplir_table_disponibilite_livres()
        except Exception as e:
            messagebox.showerror("Erreur", str(e))

    def remplir_table_livres(self):
        for row in self.table_livres.get_children():
            self.table_livres.delete(row)
        for livre in self.biblio.livres:
            self.table_livres.insert('', 'end', values=(livre.ISBN, livre.titre, livre.auteur, livre.annee, livre.genre))

    def remplir_table_membres(self):
        for row in self.table_membres.get_children():
            self.table_membres.delete(row)
        for membre in self.biblio.membres:
            self.table_membres.insert('', 'end', values=(membre.ID, membre.nom))

    def remplir_table_disponibilite_livres(self):
        for row in self.table_livres_emprunts.get_children():
            self.table_livres_emprunts.delete(row)
        for livre in self.biblio.livres:
            statut = "Emprunté" if livre.est_emprunte else "Disponible"
            self.table_livres_emprunts.insert('', 'end', values=(livre.ISBN, livre.titre, statut))

if __name__ == "__main__":
    app = InterfaceBibliotheque()
    app.mainloop()
