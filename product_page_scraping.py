# coding : UTF-8
import requests
from bs4 import BeautifulSoup
import csv
import re
from datetime import datetime
import os

link = 'http://books.toscrape.com/catalogue/robin-war_730/index.html'
csv_title = 'test'

#######################

# création d'un dossier et éxécution du code/génération des données dans ce dossier
now = datetime.now()
new_run_folder = csv_title + now.strftime(" %d-%m-%Y at %Hh%Mm%Ss")
os.mkdir(new_run_folder)
os.chdir(new_run_folder)

# création du dossier csv avec ses titres de colonnes
csv_headers_column = ['url', 'upc', 'title', 'price_incl_tax', 'price_excl_tax', 'number_available',
                      'product_description', 'category', 'review_rating', 'image_url']
with open(csv_title+'.csv', 'w', newline='', encoding='UTF-8') as f:
    writer = csv.writer(f)
    writer.writerow(csv_headers_column)


def product_page_scraping(url, category_title):
    # obtenir le code HTML de la page produit en UTF-8
    product_page = requests.get(url)
    product_page.encoding = 'UTF-8'
    product_page = product_page.text

    # Structuer la page HTML avec BeautifulSoup
    soup = BeautifulSoup(product_page, 'html.parser')

    # recherche et listing des différents éléments à isoler
    wanted_features = [url]

    # isolement des élements 'upc', 'price w/o tax' et 'availability'
    table = soup.find('table', class_='table table-striped')
    for row in table.findAll('tr'):
        left_cell = row.th.text
        right_cell = row.td.text
        if left_cell == 'UPC':
            upc = right_cell
        if left_cell == 'Price (excl. tax)':
            price_excl_tax = right_cell
        if left_cell == 'Price (incl. tax)':
            price_incl_tax = right_cell
        if left_cell == 'Availability':
            availability = right_cell
            number_available = re.findall('\d+', availability)[0]

    # isolement de l'élément 'titre'
    title = soup.find('div', class_='col-sm-6 product_main').h1.text

    # isolement de l'élement 'product_description'
    product_description_title = soup.find('div', id='product_description')
    try:
        product_description = product_description_title.find_next('p').text
    except AttributeError:
        product_description = 'No description available'

    # isolement de l'élément 'review_rating'
    review_rating = ((soup.find('div', class_='col-sm-6 product_main').findAll('p')[-1])['class'])[1]
    if review_rating == 'One':
        review_rating = '1/5'
    if review_rating == 'Two':
        review_rating = '2/5'
    if review_rating == 'Three':
        review_rating = '3/5'
    if review_rating == 'Four':
        review_rating = '4/5'
    if review_rating == 'Five':
        review_rating = '5/5'

    # isolement de l'élément 'category'
    category = ((soup.find('ul', class_='breadcrumb').findAll('li'))[-2]).text.strip()

    # isolement de l'élément 'image_url'
    image_url = (soup.find('div', id='product_gallery').find('img'))['src'].replace('../../',
                                                                                    'http://books.toscrape.com/')

    wanted_features.extend([upc, title, price_incl_tax, price_excl_tax, number_available, product_description,
                            review_rating, category, image_url])
    with open(category_title+'.csv', 'a', newline='', encoding='UTF-8') as f:
        writer = csv.writer(f)
        writer.writerow(wanted_features)


product_page_scraping(link, csv_title)
