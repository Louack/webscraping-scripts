# coding UTF-8
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from functions_scraping import category_screening
import os
import csv

link = 'http://books.toscrape.com/catalogue/category/books/fantasy_19/page-1.html'
category_title = 'Fantasy'


###########################

# création d'un dossier et éxécution du code/génération des données dans ce dossier
now = datetime.now()
new_run_folder = category_title + now.strftime("_%d-%m-%Y at %Hh%Mm%Ss")
os.mkdir(new_run_folder)
os.chdir(new_run_folder)
image_folder = category_title + ' images'
os.mkdir(image_folder)


# création du dossier csv avec ses titres de colonnes
csv_headers_column = ['url', 'upc', 'title', 'price_incl_tax', 'price_excl_tax', 'number_available',
                      'product_description', 'category', 'review_rating', 'image_url']
with open(category_title+'.csv', 'w', newline='', encoding='UTF-8') as f:
    writer = csv.writer(f)
    writer.writerow(csv_headers_column)

page = ''

category_screening(link, category_title, page, image_folder)
