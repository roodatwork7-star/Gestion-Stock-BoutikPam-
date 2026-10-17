"""
BoutikPam - Gestion de stock

Application de bureau (Tkinter) pour gérer les produits d'une petite boutique :
ajouter, modifier, supprimer, et suivre quelques statistiques du stock.
"""
import tkinter as tk
from tkinter import messagebox, ttk

CATEGORIES = ["Cosmétique", "Alimentaire", "Boisson gazeuse", "Boisson alcoolisée", "Accessoires"]
SEUIL_STOCK_BAS = 5  # réservé : mise en évidence des produits presque épuisés (à venir)
DEVISE = "HTG"


class GestionStock:
    def __init__(self):
        self.app = tk.Tk()
        # La liste est la source de vérité : le tableau n'est qu'un affichage de cette liste.
        self.produits = []
        self.var_nom = tk.StringVar()
        self.var_prix = tk.DoubleVar()
        self.var_qte = tk.IntVar()

        self.init_components()

    # Lecture et validation du formulaire
    def lire_entree(self):
        """Lit et valide le formulaire.

        Retourne un dictionnaire produit si tout est valide, sinon None
        (le message d'erreur a déjà été affiché).
        """
        nom = self.var_nom.get().strip()
        if len(nom) < 2:
            messagebox.showerror("Entrée invalide",
                                 "Le nom du produit doit avoir au moins 2 caractères.\nExemple : 7Up")
            return None

        try:
            prix = self.var_prix.get()
            qte = self.var_qte.get()
        except tk.TclError:
            messagebox.showerror("Entrée invalide",
                                 "Le prix doit être un nombre et la quantité un entier.\nExemple : 450 et 89")
            return None

        if prix <= 0:
            messagebox.showwarning("Prix incorrect", "Le prix doit être supérieur à 0.")
            return None
        if qte < 0:
            messagebox.showwarning("Quantité incorrecte", "La quantité ne peut pas être négative.")
            return None

        return {"nom": nom, "prix": prix, "qte": qte, "categorie": self.cb_categorie.get()}

    def existe_deja(self, nom, ignorer=None):
        """Vrai si un produit porte déjà ce nom (sans tenir compte des majuscules).

        `ignorer` est la position d'un produit à sauter : utile quand on modifie
        un produit, pour qu'il ne se compare pas à lui-même.
        """
        for i, p in enumerate(self.produits):
            if ignorer is not None and i == ignorer:
                continue
            if p["nom"].lower() == nom.lower():
                return True
        return False

    # Tableau et sélection
    def rafraichir_tableau(self):
        """Reconstruit le tableau depuis self.produits, puis met les statistiques à jour.

        À appeler après chaque changement de la liste. L'identifiant de chaque ligne
        (iid) est la position du produit dans la liste.
        """
        self.tableau.delete(*self.tableau.get_children())
        for i, p in enumerate(self.produits):
            self.tableau.insert("", "end", iid=str(i),
                                values=(p["nom"], f"{p['prix']:.2f}", p["qte"], p["categorie"]))
        self.afficher_stats()  # hors de la boucle : doit aussi s'exécuter quand la liste est vide

    def index_selectionne(self):
        """Position du produit sélectionné, ou None (avec un avertissement) s'il n'y en a pas."""
        selection = self.tableau.selection()
        if not selection:
            messagebox.showwarning("Sélection", "Veuillez choisir un produit dans le tableau.")
            return None
        return int(selection[0])

    def remplir_formulaire(self, event=None):
        """Copie le produit sélectionné dans le formulaire (silencieux si rien n'est sélectionné)."""
        selection = self.tableau.selection()
        if not selection:
            return
        p = self.produits[int(selection[0])]

        self.var_nom.set(p["nom"])
        self.var_prix.set(p["prix"])
        self.var_qte.set(p["qte"])
        self.cb_categorie.set(p["categorie"])

    # Actions des boutons
    def ajouter(self):
        produit = self.lire_entree()
        if produit is None:
            return
        if self.existe_deja(produit["nom"]):
            messagebox.showwarning("Doublon", f"Le produit « {produit['nom']} » existe déjà.")
            return

        self.produits.append(produit)
        self.rafraichir_tableau()
        self.vider_formulaire()

    def modifier(self):
        index = self.index_selectionne()
        if index is None:
            return
        produit = self.lire_entree()
        if produit is None:
            return
        if self.existe_deja(produit["nom"], ignorer=index):
            messagebox.showwarning("Doublon", f"Le produit « {produit['nom']} » existe déjà.")
            return

        self.produits[index] = produit
        self.rafraichir_tableau()
        self.vider_formulaire()

    def supprimer(self):
        index = self.index_selectionne()
        if index is None:
            return
        nom_produit = self.produits[index]["nom"]
        reponse = messagebox.askyesno("Confirmation",
                                      f"Voulez-vous vraiment supprimer le produit : {nom_produit} ?")
        if reponse:
            self.produits.pop(index)
            self.rafraichir_tableau()
            self.vider_formulaire()

    def vider_formulaire(self):
        self.var_nom.set("")
        self.var_prix.set(0)
        self.var_qte.set(0)
        self.cb_categorie.current(0)

    # Statistiques
    def calculer_stats(self):
        """Retourne (nombre de produits, valeur du stock, produit le plus cher).

        Ne fait aucun affichage. La liste ne doit pas être vide.
        """
        nb = len(self.produits)

        valeur = 0
        for p in self.produits:
            valeur += p["prix"] * p["qte"]

        plus_cher = self.produits[0]
        for p in self.produits:
            if p["prix"] > plus_cher["prix"]:
                plus_cher = p

        return nb, valeur, plus_cher

    def afficher_stats(self):
        if not self.produits:
            self.lbl_stats.config(text="Aucun produit")
            return
        nb, valeur, plus_cher = self.calculer_stats()
        texte = (
            f"Produits : {nb} | "
            f"Valeur du stock : {valeur:,.2f} {DEVISE} | "
            f"Plus cher : {plus_cher['nom']} ({plus_cher['prix']:,.2f} {DEVISE})"
        )
        self.lbl_stats.config(text=texte)

    # Interface
    def init_components(self):
        self.app.title("BoutikPam")
        self.app.geometry("650x500")
        self.app.columnconfigure(0, weight=1)
        self.app.rowconfigure(3, weight=1)

        tk.Label(self.app, text="Gestion de stock", font=("Arial", 18, "bold"),
                 fg="blue").grid(row=0, column=0, pady=10)

        # Formulaire
        cadre_form = tk.Frame(self.app)
        cadre_form.grid(row=1, column=0)

        champs = [("Nom", self.var_nom), ("Prix", self.var_prix), ("Quantité", self.var_qte)]
        for i, (texte, variable) in enumerate(champs):
            tk.Label(cadre_form, text=texte, font=("Arial", 12, "bold")).grid(
                row=i, column=0, sticky="w", padx=5, pady=3)
            tk.Entry(cadre_form, textvariable=variable).grid(row=i, column=1, padx=5, pady=3)

        tk.Label(cadre_form, text="Catégorie", font=("Arial", 12, "bold")).grid(
            row=3, column=0, sticky="w", padx=5, pady=3)
        self.cb_categorie = ttk.Combobox(cadre_form, values=CATEGORIES, state="readonly", width=22)
        self.cb_categorie.grid(row=3, column=1, padx=5, pady=3)
        self.cb_categorie.current(0)

        # Boutons
        cadre_boutons = tk.Frame(self.app)
        cadre_boutons.grid(row=2, column=0, pady=10)

        boutons = [("Ajouter", "green", self.ajouter),
                   ("Modifier", "navy", self.modifier),
                   ("Supprimer", "red", self.supprimer),
                   ("Annuler", "gray40", self.vider_formulaire)]
        for i, (texte, couleur, action) in enumerate(boutons):
            tk.Button(cadre_boutons, text=texte, bg=couleur, fg="white", width=10,
                      font=("Arial", 11, "bold"), command=action).grid(row=0, column=i, padx=5)

        # Tableau
        cadre_tableau = tk.Frame(self.app)
        cadre_tableau.grid(row=3, column=0, padx=10, pady=5, sticky="nsew")
        cadre_tableau.grid_columnconfigure(0, weight=1)
        cadre_tableau.grid_rowconfigure(0, weight=1)

        colonnes = (("nom", "Nom", 250), ("prix", "Prix", 100), ("qte", "Qté", 80), ("categorie", "Catégorie", 150))
        self.tableau = ttk.Treeview(cadre_tableau, columns=[c[0] for c in colonnes],
                                    show="headings", height=8)
        for cle, titre, largeur in colonnes:
            self.tableau.heading(cle, text=titre)
            self.tableau.column(cle, width=largeur)
        self.tableau.grid(row=0, column=0, sticky="nsew")
        self.tableau.bind("<<TreeviewSelect>>", self.remplir_formulaire)

        # Statistiques
        self.lbl_stats = tk.Label(self.app, text="Aucun produit", font=("Arial", 11))
        self.lbl_stats.grid(row=4, column=0, pady=8)

    def run(self):
        self.app.mainloop()

if __name__ == "__main__":
    GestionStock().run()