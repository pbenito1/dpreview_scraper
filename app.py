from bs4 import BeautifulSoup
import requests
import pandas as pd
import time
import re
import csv


BASE_URL = "https://www.dpreview.com/products/"
SLEEP_TIME = 0.5

# Creamos una sesión de requests para reutilizar la conexión.
s = requests.Session()


def get_all_cameras(init_page=1):
    page = init_page
    all_cameras = []
    page_res = get_camera_list(page)
    while page_res:
        all_cameras = all_cameras + page_res
        page = page+1
        page_res = get_camera_list(page)
        # time.sleep(SLEEP_TIME)
    return all_cameras


def get_camera_list(pagenum=1):
    # Pablo
    # https://www.dpreview.com/products/cameras/all?view=list
    # https://www.dpreview.com/products/cameras/all?view=list&page=2

    camera_list = []
    page = s.get(BASE_URL+"/cameras/all?view=list&page="+str(pagenum))
    print("Procesando "+BASE_URL+"/cameras/all?view=list&page="+str(pagenum))
    soup = BeautifulSoup(page.content, 'html.parser')
    # print(soup.prettify())
    # cameras = soup.select("tr.product")
    cameras = soup.find_all('tr', attrs={'class': 'product'})
    for c in cameras:
        current_camera = {}
        current_camera['image'] = c.td.div.a.img.get('src')
        current_camera['name'] = c.find(
            'div', attrs={'class': 'name'}).a.get_text()
        current_camera['link'] = c.find(
            'div', attrs={'class': 'name'}).a.get('href')

        if c.find('div', attrs={'class': 'announcementDate'}):
            current_camera['announcement_date'] = c.find(
                'div', attrs={'class': 'announcementDate'}).get_text()

        if c.find('div', attrs={'class': 'specs'}):
            current_camera['quick_specs'] = c.find(
                'div', attrs={'class': 'specs'}).get_text()

        # Comprobamos si tiene review
        if c.find('td', attrs={'class': 'review'}).get_text():
            current_camera['review_link'] = c.find(
                'td', attrs={'class': 'review'}).find('a').get('href')
            current_camera['review_value'] = c.find('td', attrs={'class': 'review'}).find(
                'span', attrs={'class': 'value'}).get_text()
            current_camera['review_award'] = c.find('td', attrs={'class': 'review'}).find(
                'span', attrs={'class': 'text'}).get_text()
        camera_list.append(current_camera)

    # if camera_list:
    #    camera_list.append(get_camera_list(pagenum+1))

    return camera_list


def get_specs(camera):
    # camera: fujifilm/slrs/fujifilm_xs10
    # Miki
    specs = {}
    # https://www.dpreview.com/products/fujifilm/slrs/fujifilm_xs10/specifications
    url = camera.get('link')+"/specifications"
    print("Obteniendo especificaciones..."+url)
    page = s.get(url)
    if page.status_code == 200:
        soup = BeautifulSoup(page.content, 'html.poars')
    return specs


def get_review(camera):
    # camera: fujifilm/slrs/fujifilm_xs1
    # Miki
    # https://www.dpreview.com/products/fujifilm/slrs/fujifilm_xs10/review
    review = {}
    headers = []
    scores = []
    url = camera.get('link')+"/review"
    print("Obteniendo reviews..."+url)
    page = s.get(url)
    soup = BeautifulSoup(page.content, 'html.poars')
    if soup.find('div', attrs={'class': 'scoring'}):    
        if soup.find('div', attrs={'class': 'scoring'}):
            scoring_tag = soup.find('div', attrs={'class': 'scoring'})
            for items in scoring_tag.find_all(class_= "label"):
                headers.append(items.find_next_sibling().text)
            for items in scoring_tag.find_all(class_= "gauge"):
                scores.append(re.search('width: (\d.+)\%\;', items.find_next_sibling().text))
        review = dict(zip(headers, scores))
    return review


def get_user_review(camera):
    # Pablo
    # https://www.dpreview.com/prodsucts/sony/compacts/sony_dscrx100m7/user-reviews
    user_review = {}

    url = camera.get('link')+"/user-reviews"
    print("Obteniendo reviews de usuario.."+url)
    page = s.get(url)
    if page.status_code == 200:
        # Parseo de HTML utilizando beautifulsoup
        soup = BeautifulSoup(page.content, 'html.parser')
        if soup.find('div', attrs={'class': 'starsForeground large'}):
            review_tag = soup.find(
                'div', attrs={'class': 'starsForeground large'}).get('style')
            # Extraemos cifra mediante expresión regular:
            # Ejemplo: width: 85.00000%;
            user_review['review_score'] = re.search(
                'width: (\d.+)\%\;', review_tag).group(1)
            user_review['review_count'] = soup.find(
                'div', attrs={'class': 'reviewCount'}).get_text()

    return user_review


def save_data(camera_data):
    # Pablo
    # Obtenemos todas la claves disponibles
    keys = set().union(*(d.keys() for d in camera_data))
    # Guardamos en formato CSV
    with open('dpreview.csv', 'w', newline='') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        # Escribimos la cabecera
        dict_writer.writeheader()
        dict_writer.writerows(camera_data)


def main():
    # get_user_review(
    #    {'link': 'https://www.dpreview.com/products/sony/compacts/sony_dscrx100m7'})
    # return
    camera_list = get_all_cameras()
    camera_list_enriched = []
    for camera in camera_list:
        specs = get_specs(camera)
        review = get_review(camera)
        user_review = get_user_review(camera)
        # unimos los dict de cada tipo
        enriched_camera = {**camera, **specs, **review, **user_review}
        camera_list_enriched.append(enriched_camera)
    save_data(camera_list_enriched)


if __name__ == "__main__":
    main()
