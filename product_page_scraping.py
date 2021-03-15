# coding : UTF-8
# Executer pour analyser une unique page produit
from functions_scraping import page_product_analysis

#intéraction du client avec la console (entrée du lien de la page produit + titre du livre)
link = input('Entrez le lien de la page produit à analyser (exemple : http://books.toscrape.com/catalogue/tsubasa-world-chronicle-2-tsubasa-world-chronicle-2_949/index.html) : ')
book_title = input('Entrez le titre du livre : ')

# Intégration du lien et titre du client dans la fonction d'analyse d'une page produit
# Execution de la fonction
page_product_analysis(book_title, link)
