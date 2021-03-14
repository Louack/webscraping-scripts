# coding UTF-8

from datetime import datetime
from functions_scraping import category_screening
import os
import csv

link = 'http://books.toscrape.com/catalogue/category/books/travel_2/index.html'
category_title = 'Fantasy'


###########################

# création d'un dossier et éxécution du code/génération des données dans ce dossier
now = datetime.now()
new_run_folder = category_title + now.strftime("_%d-%m-%Y at %Hh%Mm%Ss")
os.mkdir(new_run_folder)
os.chdir(new_run_folder)

#création d'un sous-dossier 'image'
image_folder = category_title + '_images'
os.mkdir(image_folder)


# création du dossier csv avec ses titres de colonnes
csv_headers_column = ['url', 'upc', 'title', 'price_incl_tax', 'price_excl_tax', 'number_available',
                      'product_description', 'category', 'review_rating', 'image_url']
with open(category_title+'.csv', 'w', newline='', encoding='UTF-8') as f:
    writer = csv.writer(f)
    writer.writerow(csv_headers_column)

page = ''

category_screening(link, category_title, page, image_folder)
