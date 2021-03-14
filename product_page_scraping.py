# coding : UTF-8

import csv
from datetime import datetime
from functions_scraping import product_page_scraping
import os


link = 'http://books.toscrape.com/catalogue/tsubasa-world-chronicle-2-tsubasa-world-chronicle-2_949/index.html'
book_title = 'Tsubasa'

#######################

# création d'un dossier et éxécution du code/génération des données dans ce dossier
now = datetime.now()
new_run_folder = book_title + " book features" + now.strftime("_%d-%m-%Y at %Hh%Mm%Ss")
os.mkdir(new_run_folder)
os.chdir(new_run_folder)

#création d'un sous-dossier 'image'
image_folder = 'image'
os.mkdir(image_folder)

# création du dossier csv avec ses titres de colonnes
csv_headers_column = ['url', 'upc', 'title', 'price_incl_tax', 'price_excl_tax', 'number_available',
                      'product_description', 'category', 'review_rating', 'image_url']
with open(book_title+'.csv', 'w', newline='', encoding='UTF-8') as f:
    writer = csv.writer(f)
    writer.writerow(csv_headers_column)

product_page_scraping(link, book_title, image_folder)
