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


def get_all_cameras(init_page=1, end_page=100):
    page = init_page
    all_cameras = []
    page_res = get_camera_list(page)
    while page_res and page < end_page:
        all_cameras = all_cameras + page_res
        page = page+1
        page_res = get_camera_list(page)
        time.sleep(SLEEP_TIME)
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


def get_overview(camera):
    # https://www.dpreview.com/products/leica/compacts/leica_q2_monochrom/overview
    overview = {}
    labels = []
    scores = []
    url = camera.get('link')+"/overview"
    print("Obteniendo overview..."+url)
    page = s.get(url)
    if page.status_code == 200:
        soup = BeautifulSoup(page.content, 'html.parser')
        if soup.find('div', attrs={'class': 'scoring'}):
            scoring_tag = soup.find('div', attrs={'class': 'scoring'})
            for label in scoring_tag.find_all(class_="label"):
                labels.append(label.text)
                # headers.append(items.find_next_sibling().text)
            for score in scoring_tag.find_all(class_="gauge"):
                scores.append(float(re.search('width: (\d.+)\%\;',
                              score.get('style')).group(1)))
        overview = dict(zip(labels, scores))
        breadcrumbs = soup.find(
            'div', attrs={'class': 'breadcrumbs'}).find_all()
        overview['brand'] = breadcrumbs[2].text.strip()
        overview['brand_camera_family'] = breadcrumbs[4].text.strip()
        gear_list = soup.find('table', {'id': 'productOverviewGearList'}).find(
            'tr', {'class': 'values'}).find_all('td')
        overview['own_gear'] = int(gear_list[0].text.strip())
        overview['want_gear'] = int(gear_list[2].text.strip())
        overview['had_gear'] = int(gear_list[4].text.strip())

    return overview


def get_specs(camera):
    # camera: fujifilm/slrs/fujifilm_xs10
    # Miki
    specs = {}
    labels = []
    values = []
    # https://www.dpreview.com/products/fujifilm/slrs/fujifilm_xs10/specifications
    url = camera.get('link')+"/specifications"
    print("Obteniendo especificaciones..."+url)
    page = s.get(url)
    if page.status_code == 200:
        soup = BeautifulSoup(page.content, 'html.parser')
        if soup.find('table', attrs={'class': 'specsTable compact'}):
            specs_tag = soup.find(
                'table', attrs={'class': 'specsTable compact'})
            for label in specs_tag.find_all(class_="label"):
                labels.append(label.text.strip())
                # headers.append(items.find_next_sibling().text)
            for value in specs_tag.find_all(class_="value"):
                values.append(value.text.strip())
        specs = dict(zip(labels, values))
    return specs


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
    # get_overview(
    #    {'link': 'https://www.dpreview.com/products/fujifilm/slrs/fujifilm_xs10'})
    # return
    # camera_list = get_all_cameras(init_page=1, end_page=2)
    camera_list = get_all_cameras()
    camera_list_enriched = []
    for camera in camera_list:
        overview = get_overview(camera)
        specs = get_specs(camera)
        user_review = get_user_review(camera)
        # unimos los dict de cada tipo
        enriched_camera = {**camera, **overview, **specs, **user_review}
        camera_list_enriched.append(enriched_camera)
    save_data(camera_list_enriched)


if __name__ == "__main__":
    main()
