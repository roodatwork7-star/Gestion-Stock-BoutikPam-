# BoutikPam — Gestion de stock

Application de bureau en **Python (Tkinter)** pour gérer le stock d'une petite boutique : ajouter, modifier et supprimer des produits, avec validation des saisies et statistiques en temps réel.

<!-- Ajoutez une capture d'écran : créez un dossier docs/ puis décommentez la ligne suivante -->
<!-- ![Aperçu de BoutikPam](docs/apercu.png) -->

## Fonctionnalités

- **Ajouter** un produit (nom, prix, quantité, catégorie)
- **Modifier** un produit : un clic sur une ligne du tableau remplit le formulaire
- **Supprimer** un produit, avec confirmation
- **Détection des doublons** : « Diri », « diri » et « DIRI » sont considérés comme le même produit
- **Validation des saisies** avec boîtes de dialogue claires (pas de plantage si on tape du texte à la place d'un nombre)
- **Statistiques mises à jour automatiquement** : nombre de produits, valeur totale du stock, produit le plus cher
- Interface qui s'adapte à la taille de la fenêtre

## Règles de validation

| Champ | Règle |
|---|---|
| Nom | au moins 2 caractères (espaces ignorés), unique sans tenir compte de la casse |
| Prix | nombre strictement supérieur à 0 (séparateur décimal : le point, ex. `5.5`) |
| Quantité | nombre entier supérieur ou égal à 0 |
| Catégorie | choisie dans une liste fixe |

## Prérequis et lancement

- Python 3.8 ou supérieur. Tkinter est inclus avec Python sous Windows et macOS. Sous Linux : `sudo apt install python3-tk`.
- Aucune bibliothèque externe à installer.

```bash
python gestion_stock.py
```

## Utilisation

1. Remplissez le formulaire puis cliquez sur **Ajouter**.
2. Cliquez sur une ligne du tableau pour charger le produit dans le formulaire.
3. Changez ce que vous voulez, puis cliquez sur **Modifier**.
4. Sélectionnez une ligne et cliquez sur **Supprimer** pour l'enlever (une confirmation est demandée).
5. **Annuler** vide simplement le formulaire, sans toucher au tableau.

## Structure du code

Le projet tient dans un seul fichier, organisé autour de la classe `GestionStock`.

| Méthode | Rôle |
|---|---|
| `lire_entree()` | Lit et valide le formulaire, retourne un dictionnaire ou `None` |
| `existe_deja(nom, ignorer)` | Détecte un doublon (en ignorant éventuellement le produit en cours de modification) |
| `rafraichir_tableau()` | Reconstruit le tableau depuis la liste de produits |
| `ajouter()`, `modifier()`, `supprimer()` | Actions des boutons |
| `calculer_stats()` | Calcule les statistiques (sans rien afficher) |
| `afficher_stats()` | Affiche les statistiques dans l'interface |

Choix de conception :

- **La liste `self.produits` est la source de vérité.** Le tableau n'est qu'un affichage, reconstruit après chaque changement. Cela évite que les deux se désynchronisent et facilitera l'ajout d'une sauvegarde ou d'une recherche.
- **Séparation calcul / affichage** : `calculer_stats()` retourne des valeurs, `afficher_stats()` les montre. Les calculs se testent sans interface.
- **Identifiant de ligne = position dans la liste** (`iid`), ce qui permet de retrouver le produit sélectionné sans ambiguïté.

## Compétences mises en pratique

Programmation orientée objet · Tkinter (`grid`, `Frame`, `Treeview`, `Combobox`, `messagebox`, événements avec `bind`) · gestion des erreurs avec `try/except` · validation des entrées · structures de données (liste de dictionnaires)

## Limites actuelles et pistes d'amélioration

- [ ] **Sauvegarde** : les données sont perdues à la fermeture (prévu : JSON, puis SQLite ou MySQL)
- [ ] Mise en évidence en rouge des produits dont la quantité est inférieure à `SEUIL_STOCK_BAS`
- [ ] Recherche et tri dans le tableau
- [ ] Export CSV
- [ ] Tests automatisés des fonctions de calcul

## Auteur

Gaspard Roody — projet réalisé pendant ma formation en informatique, dans le cadre de mon apprentissage de Python.
