from bs4 import BeautifulSoup
import requests
import csv

web = 'google.com'
def get_fav_logo(web):

    fav_url = ''
    logo_url = ''

    brand = web.split('.')[0]
    html = requests.get('http://www.'+web)
    html_soup = BeautifulSoup(html.content, 'lxml')

    for link in html_soup.select('img'):
        src = link.get('src')
        if 'logo' in link or brand in src:
           logo_url = src
           break

    for link in html_soup.findAll('link', attrs={'rel':'icon'}):
        src = link.get('href')
        if 'ico' in link or brand in src or 'fav':
           fav_url = src
           break

    return logo_url, fav_url

with open('../../websites.csv', 'r') as file:
        data = file.read()

with open('result2.csv', 'a+') as file:
    writer = csv.writer(file)
    writer.writerow(['website', 'logo', 'favicon'])
    file.close()

urls =data.split('\n')

for url in urls:
    favicon_url = ''
    logo_url = ''
    try:
        print('getting info on: ', url)
        logo_url, favicon_url = get_fav_logo(url)
    except:
        print ('Got Error')
    with open('result2.csv', 'a+') as file:
        writer = csv.writer(file)
        writer.writerow([url, logo_url, favicon_url])
        file.close()