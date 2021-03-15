# coding UTF-8
# Executer pour analyser l'intégralité d'une catégorie de livres
from functions_scraping import category_page_analysis

#intéraction du client avec la console (entrée du lien de la catégorie + son titre)
link = input('Entrez un lien de catégorie de livres à analyser (exemple : http://books.toscrape.com/catalogue/category/books/travel_2/index.html) : ')
category_title = input('Entrez le titre de la catégorie de livres : ')

# intégration du lien et titre du client dans la fonction d'analyse d'une catégorie
# Execution de la fonction
category_page_analysis(category_title, link)
