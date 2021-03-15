# coding UTF-8
# fichier regroupant les différentes fonctions utilisées pour les 3 types d'analyse
from bs4 import BeautifulSoup
from datetime import datetime
import requests
import re
import os
import csv


# fonction création d'un dossier pour stocker les analyses
def main_directory_creation(main_folder_title):
    now = datetime.now()  # capture de date+heure à l'instant de l'éxécution de la ligne de code
    new_run_folder = main_folder_title + now.strftime("_%d-%m-%Y at %Hh%Mm%Ss")  # composition du titre du dossier
    os.mkdir(new_run_folder)  # création du nouveau dossier
    os.chdir(new_run_folder)  # placement dans le nouveau dossier


# fonction création du sous-dossier image + fichier.csv
def img_csv_creation(csv_title):
    image_folder = csv_title + '_images'  # création du titre du dossier
    os.mkdir(image_folder)  # création du sous-dossier 'image'

    # création du dossier csv avec ses titres de colonnes
    csv_headers_column = ['url', 'upc', 'title', 'price_incl_tax', 'price_excl_tax', 'number_available',
                          'product_description', 'category', 'review_rating', 'image_url']
    with open(csv_title + '.csv', 'w', newline='', encoding='UTF-8') as f:
        writer = csv.writer(f)
        writer.writerow(csv_headers_column)
    return image_folder  # pour réutilisation de l'objet image_folder dans une autre fonction


# fonction accédant au lien recherché + structuration du code HTML obtenu
def page_request_then_bs(url):
    response = requests.get(url)  # requête du lien
    response.encoding = 'UTF-8'  # conversion en UTF-8
    response = response.text  # accès au code HTML de la page
    soup = BeautifulSoup(response, 'html.parser')  # structuration du code HTML
    return soup


# isolement/transformation des éléments d'interêt d'une page produit via navigation dans arborescence du code HTML
def product_page_scraping(url, category_title, image_folder):
    soup = page_request_then_bs(url)

    # recherche et listing des différents éléments à isoler
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

    # ajout des différents éléments dans le fichier csv (mode append)
    with open(category_title + '.csv', 'a', newline='', encoding='UTF-8') as f:
        writer = csv.writer(f)
        writer.writerow([url, upc, title, price_incl_tax, price_excl_tax, number_available, product_description,
                        category, review_rating, image_url])

    # téléchargement de l'image dans le sous-dossier 'image'
    os.chdir(image_folder)
    img_dl = requests.get(image_url)
    with open(upc + '.jpg', 'wb') as img:
        img.write(img_dl.content)
    os.chdir('..')


# isolement/criblage des liens page_produit pour une catégorie donnée
def category_screening(link, category_title, page, image_folder):
    # construction du lien HTML quand plusieurs pages par catégorie
    if 'index.html' in link:
        link = link.replace('index.html', page)
    else:
        link = link+page

    soup = page_request_then_bs(link)

    book_list = soup.findAll('h3')  # isolement de la liste des livres
    for h3 in book_list:  # boucle de passant en revue chaque lien page produit
        book_link = h3.a['href'].replace('../../..', 'http://books.toscrape.com/catalogue')
        print(book_link)
        product_page_scraping(book_link, category_title, image_folder)  # Execution à chaque page produit
    next_button = soup.find('li', class_='next')  # Détection d'un ongler 'next'
    # construction du lien de la page suivante si 'next' est présent
    if next_button is not None:
        next_button = next_button.a['href']
        link = link.replace(page, '')
        category_screening(link, category_title, next_button, image_folder)  # rééxécution de la fonction


# fonction complète analyse d'une page produit unique
def page_product_analysis(book_title, link):
    main_directory_creation(book_title)
    image_folder = img_csv_creation(book_title)
    product_page_scraping(link, book_title, image_folder)


# fonction complète analyse d'une catégorie de livres
def category_page_analysis(category_title, link):
    page = ''
    main_directory_creation(category_title)
    image_folder = img_csv_creation(category_title)
    category_screening(link, category_title, page, image_folder)


# fonction complète analyse totale du site
def website_analysis():
    url_mainpage = 'http://books.toscrape.com/'
    main_folder_title = "bookstoscrape analysis"

    main_directory_creation(main_folder_title)
    soup = page_request_then_bs(url_mainpage)

    # isolement de la liste des catégories de livres
    category_list = soup.find('ul', class_='nav nav-list')
    category_list = category_list.find_next('ul')
    category_list = category_list.findAll('a', href=True)

    # criblage des liens categorie
    for category_link in category_list:
        csv_title = (category_link.text.strip())
        category_link = (url_mainpage + category_link['href'])
        print(category_link)
        image_folder = img_csv_creation(csv_title)
        page = ''
        category_screening(category_link, csv_title, page, image_folder)  # execution fonction analyse catégorie
