from bs4 import BeautifulSoup
import requests


BASE_URL = "https://www.dpreview.com/products/"


def get_camera_list(pageList=None):
    # Pablo
    # https://www.dpreview.com/products/cameras/all?view=list
    # https://www.dpreview.com/products/cameras/all?view=list&page=2
    page = requests.get(BASE_URL+"/cameras/all?view=list")

    for camera in cameraList:
        specs = get_specs(camera)


def get_specs(camera):
    # camera: fujifilm/slrs/fujifilm_xs10
    # Miki
    specs = {}
    # https://www.dpreview.com/products/fujifilm/slrs/fujifilm_xs10/specifications
    url = BASE_URL + "/"+camera+"/specifications"
    page = requests.get(url)
    # Parseo de HTML utilizando beautifulsoup

    return specs


def get_review(camera):
    # camera: fujifilm/slrs/fujifilm_xs1
    # Miki
    # https://www.dpreview.com/products/fujifilm/slrs/fujifilm_xs10/review
    review = {}
    url = BASE_URL + "/"+camera+"/review"
    page = requests.get(url)
    # Parseo de HTML utilizando beautifulsoup

    return review


def save_data(camera_data, output_file):
    # Pablo
    return


def main():
    camera_list = get_camera_list()
    for camera in camera_list:


if __name__ == "__main__":
    main()

page = requests.get(BASE_URL)

#soup = BeautifulSoup(page.content)
soup = BeautifulSoup(page.content, 'html.parser')
# print(soup.prettify())
years = soup.select(
    "combinedProductList>div>table>thead:nth-child(1)>tr>th")

#years = soup.find_all("tr", {"class": "groupLabel"})
# combinedProductList > div > table > thead:nth-child(1) > tr > th
# https://blog.jonmassey.co.uk/posts/chrome-beautifulsoup-scraping/
# https://stackoverflow.com/questions/58136906/how-do-i-convert-css-selector-path-copied-from-chrome-to-beautifulsoup-obejct

productList = soup.select("table.productList")
print(productList)
# for year in productList.select()
# for year_group in soup.select("tr.productList"):
#    year = year_group.select("tr>th")
#    print(year)
