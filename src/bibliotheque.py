from exceptions import *
# Classes Métiers
class Livre:
    def __init__(self, ISBN, titre, auteur, annee, genre):
        self.ISBN = ISBN
        self.titre = titre
        self.auteur = auteur
        self.annee = annee
        self.genre = genre
        self.est_emprunte = False

    def emprunter(self):
        if not self.est_emprunte:
            self.est_emprunte = True
        else:
            raise LivreIndisponibleError()

    def rendre(self):
        if self.est_emprunte:
            self.est_emprunte = False
        else:
            raise Exception("Ce livre n’est pas actuellement emprunté.")

class Membre:
    Livre_Max = 7

    def __init__(self, ID, nom):
        self.ID = ID
        self.nom = nom
        self.livres_empruntes = []

    def emprunter_livre(self, livre):
        if livre.est_emprunte:
            raise LivreIndisponibleError()
        if len(self.livres_empruntes) >= Membre.Livre_Max:
            raise QuotaEmpruntDepasseError()
        livre.emprunter()
        self.livres_empruntes.append(livre)

    def rendre_livre(self, livre):
        if livre in self.livres_empruntes:
            livre.rendre()
            self.livres_empruntes.remove(livre)
        else:
            raise Exception("Ce livre n’est pas emprunté par ce membre.")
class Bibliotheque:
    def __init__(self):
        self.livres = []
        self.membres = []

    def ajouter_livre(self, livre):
        self.livres.append(livre)

    def supprimer_livre(self, livre):
        if livre in self.livres:
            self.livres.remove(livre)
        else:
            raise LivreInexistantError()

    def enregistrer_membre(self, membre):
        self.membres.append(membre)


    def emprunter_livre(self, ID_membre, titre_livre):
        membre = None
        livre = None
        for m in self.membres:
            if m.ID == ID_membre:
                membre = m
                break
        if not membre:
            raise MembreInexistantError()

        for l in self.livres:
            if l.titre == titre_livre:
                livre = l
                break
        if not livre:
            raise LivreInexistantError()

        membre.emprunter_livre(livre)

    def rendre_livre(self, ID_membre, titre_livre):
        membre = None
        livre = None
        for m in self.membres:
            if m.ID == ID_membre:
                membre = m
                break
        if not membre:
            raise MembreInexistantError()

        for l in self.livres:
            if l.titre == titre_livre:
                livre = l
                break
        if not livre:
            raise LivreInexistantError()

        membre.rendre_livre(livre)
