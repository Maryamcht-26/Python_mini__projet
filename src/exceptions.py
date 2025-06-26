class LivreIndisponibleError(Exception):
    def __init__(self):
        super().__init__("Le livre est déjà emprunté.")

class LivreInexistantError(Exception):
    def __init__(self):
        super().__init__("Le titre du livre est incorrect ou inexistant.")

class MembreInexistantError(Exception):
    def __init__(self):
        super().__init__("L'identifiant du membre est incorrect ou inexistant.")

class QuotaEmpruntDepasseError(Exception):
    def __init__(self):
        super().__init__("Le membre a atteint le nombre maximal d'emprunts.")
