from bs4 import BeautifulSoup
import requests
import time


BASE_URL = "https://www.dpreview.com/products/"

# Creamos una sesión de requests para reutilizar la conexión.
s = requests.Session()


def get_all_cameras():
    page = 1
    all_cameras = []
    page_res = get_camera_list(page)
    while page_res:
        all_cameras = all_cameras + page_res
        page = page+1
        page_res = get_camera_list(page)
        time.sleep(1)
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


def get_specs(camera_url):
    # camera: fujifilm/slrs/fujifilm_xs10
    # Miki
    specs = {}
    # https://www.dpreview.com/products/fujifilm/slrs/fujifilm_xs10/specifications
    url = camera_url+"/specifications"
    print("Obteniendo especificaciones..."+url)
    # page = s.get(url)
    # Parseo de HTML utilizando beautifulsoup
    return specs


def get_review(camera_url):
    # camera: fujifilm/slrs/fujifilm_xs1
    # Miki
    # https://www.dpreview.com/products/fujifilm/slrs/fujifilm_xs10/review
    review = {}
    url = camera_url+"/review"
    print("Obteniendo reviews..."+url)
    # page = s.get(url)
    # Parseo de HTML utilizando beautifulsoup

    return review


def save_data(camera_data, output_file):
    # Pablo
    return


def main():
    camera_list = get_all_cameras()
    for camera in camera_list:
        specs = get_specs(camera.get('link'))
        if camera.get('review_link'):
            review = get_review(camera.get('link'))


if __name__ == "__main__":
    main()
