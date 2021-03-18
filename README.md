# Books to Scrape Analysis

## DESCRIPTION
"Books to Scrape Analysis" est un logiciel visant à extraire des informations d'intêret du site "http://books.toscrape.com/" de façon automatisée. 
Chaque page produit correpsond à un livre pour lequel, on cherche à récupérer les informations suivantes dans un fichier .csv :
* l'URL de la page (product_page_url)
* le code produit universel (upc)
* le titre du livre (title)
* le prix avec taxe (price_including_tax)
* le prix hors taxe (price_excluding_tax)
* le nombre d'articles disponibles (number available)
* la description du produit (product_description)
* la catégorie (category)
* la note des revues (review_rating)
* l'URL de l'image du livre (image_url)
"Books to Scrape Analysis" est capable de parcourir le site par catégorie de livres et à récupérer les informations désirées pour chaque livre du site en une seule éxecution.


## COMPOSITION DU DOSSIER
README.txt
requirements.txt
functions_scraping.py
product_page_scraping.py
category_page_screening.py
website_scraping.py

## INSTALLATION
Sous Python 3.9, installer les modules externes listés dans le fichier "requirements.txt" dans un environnement virtuel

Dans la ligne de commande, dans le dossier contenant les fichiers ci-dessus:

- création env virtuel:
  - $ python -m venv venvp2

- activation env virtuel
  - $ venvp2/Scripts/activate.ps1

- installation des modules externes
  - $ pip install -r requirements.txt


## EXECUTION DES PROGRAMMES
"Books to Scrape Analysis" regroupe 3 scripts pour 3 analyses:

1. **product_page_scraping.py** ==> analyse d'une page produit unique
2. **category_page_screening.py** ==> analyse des pages produit d'une catégorie déterminée
3. **website_scraping.py** ==> analyse de l'intégralité du site

* Chaque programme utilise des fonctions regroupés dans le fichier **functions_scraping.py**
* Le résultat d'une analyse est stockée dans un dossier (titre du livre/catégorie + date/heure). Ce dossier contient le/les fichier(s) ainsi qu'un sous-dossier pour la/les image(s)
* Le nom des images téléchargées correspond au code 'UPC' des livres associés
* Les programmes **product_page_scraping.py** et **category_page_screening.py** nécessitent deux saisies (lien HTML + titre du livre ou de la catégorie) de la part de l'utilisateur dans la console lors de l'éxécution du script.
* Lors de la lecture d'un fichier csv via un tableau, s'assurer que le tableur est configuré en **UTF-8** et la catégorie des cellules en **Nombre**, format **Standard**.


