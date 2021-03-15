Books to Scrape analysis

DESCRIPTION
Logiciel visant à extraire des informations d'intêret du site "http://books.toscrape.com/" de façon automatisée


COMPOSITION DU DOSSIER
README.txt
requirements.txt
functions_scraping.py
product_page_scraping.py
category_page_screening.py
website_scraping.py

INSTALLATION
Sous Python 3.9, installer les modules externes présents dans le fichier "requirements.txt" dans un environnement virtuel

Dans la ligne de commande, dans le dossier contenant les fichiers ci-dessus:

- création env virtuel:
$ python -m venv venvp2

- activation env virtuel
$ venvp2/Scripts/activate.ps1

- installation des modules externes
$ pip install -r requirements.txt


EXECUTION DES PROGRAMMES
3 programmes pour 3 analyses:

1) product_page_scraping.py ==> analyse d'une page produit unique
2) category_page_screening.py ==> analyse des pages produit d'une catégorie déterminée
3) website_scraping.py ==> analyse de l'intégralité du site

Chaque programme utilise des fonctions regroupés dans le fichier functions_scraping.py
Le résultat d'une analyse est stockée dans un dossier (titre du livre/catégorie + date/heure). Ce dossier contient le/les fichier(s) ainsi qu'un sous-dossier pour la/les image(s)
Le nom des images téléchargées correspond au code 'UPC' des livres associés
Les programmes 1) et 2) nécessitent deux saisies (lien HTML + titre du livre ou de la catégorie) de la part de l'utilisateur dans la console au début de l'éxécution du code.
Pour la saisie 'titre' éviter d'utiliser un caractère inaproprié pour la création d'un dossier/fichier sous peine d'échec au lancement du code


