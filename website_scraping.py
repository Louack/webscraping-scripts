# coding UTF-8

from bs4 import BeautifulSoup
from datetime import datetime
from functions_scraping import category_screening
import requests
import csv
import os


# création d'un dossier et éxécution du code/génération des données dans ce dossier
now = datetime.now()
new_run_folder = 'bookstoscrape analysis' + now.strftime("_%d-%m-%Y at %Hh%Mm%Ss")
os.mkdir(new_run_folder)
os.chdir(new_run_folder)

# aller chercher le code source de la page:
url_mainpage = 'http://books.toscrape.com/'
html_mainpage = requests.get(url_mainpage)
html_mainpage.encoding = 'UTF-8'
html_mainpage = html_mainpage.text

# parsing mainpage:
soup = BeautifulSoup(html_mainpage, 'html.parser')

# isolement de la liste des catégories de livres
category_list = soup.find('ul', class_='nav nav-list')
category_list = category_list.find_next('ul')
category_list = category_list.findAll('a', href=True)

for category_link in category_list:
    category_title = (category_link.text.strip())
    category_link = (url_mainpage+category_link['href'])
    print(category_link)

    # création d'un sous-dossier 'image'
    image_folder = category_title + '_images'
    os.mkdir(image_folder)

    # création du dossier csv avec ses titres de colonnes
    csv_headers_column = ['url', 'upc', 'title', 'price_incl_tax', 'price_excl_tax', 'number_available',
                          'product_description', 'category', 'review_rating', 'image_url']
    with open(category_title + '.csv', 'w', newline='', encoding='UTF-8') as f:
        writer = csv.writer(f)
        writer.writerow(csv_headers_column)

    page = ''
    category_screening(category_link, category_title, page, image_folder)
