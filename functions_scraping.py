# coding UTF-8
import requests
from bs4 import BeautifulSoup
import re
import os
import csv


def product_page_scraping(url, category_title, image_folder):
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

    # ajout des différents éléments dans le fichier csv
    wanted_features.extend([upc, title, price_incl_tax, price_excl_tax, number_available, product_description,
                            category, review_rating, image_url])
    with open(category_title+'.csv', 'a', newline='', encoding='UTF-8') as f:
        writer = csv.writer(f)
        writer.writerow(wanted_features)

    #téléchargement de l'image dans le sous-dossier 'image'
    os.chdir(image_folder)
    img_dl = requests.get(image_url)
    with open(upc + '.jpg', 'wb') as img:
        img.write(img_dl.content)
    os.chdir('..')


def category_screening(link, category_title, page, image_folder):
    if 'index.html' in link:
        link = link.replace('index.html', page)
    else:
        link = link+page
    # récupération du code HTML de la page 'category' en UTF-8
    category_page = requests.get(link)
    category_page.encoding = 'UTF-8'
    category_page = category_page.text
    # parsing de la page 'category'
    soup = BeautifulSoup(category_page, 'html.parser')
    # isolement de la liste des livres
    book_list = soup.findAll('h3')
    for h3 in book_list:
        book_link = h3.a['href'].replace('../../..', 'http://books.toscrape.com/catalogue')
        print(book_link)
        product_page_scraping(book_link, category_title, image_folder)
    next_button = soup.find('li', class_='next')
    if next_button is not None:
        next_button = next_button.a['href']
        link = link.replace(page, '')
        category_screening(link, category_title, next_button, image_folder)
