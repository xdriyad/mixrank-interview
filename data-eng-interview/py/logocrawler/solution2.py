from bs4 import BeautifulSoup
import requests
import csv
import pandas as pd

def get_fav_logo(web):

    fav_url = ''
    logo_url = ''

    brand = web.split('.')[0]
    html = requests.get('http://www.'+web, allow_redirects=True, timeout=5)
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

with open('websites.csv', 'r') as file:
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
        with open('result2.csv', 'a+') as file:
            writer = csv.writer(file)
            writer.writerow([url, logo_url, favicon_url])
            file.close()
    except:
        print ('Got Error')

src = pd.read_csv('websites.csv').fillna(0)
res = pd.read_csv('result2.csv').fillna(0)
ls = len(src) + 1
lr = len(res)
tl = len([x for x in list(res['logo']) if x != 0])
tf = len([x for x in list(res['favicon']) if x != 0])

logo_precision = (tl / lr)   # TruePositives / (TruePositives + FalsePositives)
logo_recall = tl / (tl + (ls - lr))  # TruePositives / (TruePositives + FalseNegatives)

favicon_precision = (tf / lr)   # TruePositives / (TruePositives + FalsePositives)
favicon_recall = tf / (tf + (ls - lr))  # TruePositives / (TruePositives + FalseNegatives)

l1 = str ('>>>>RESULT<<<<')
l2 = str ('Response Found: ' + str(lr)+ ' Logo Found: '+ str(tl) + ' Favicon Found: '+ str(tf)+ ' Request Failed: '+ str(ls-lr))
l3 = str ('Logo ->' + ' Precision: ' + str(logo_precision) + ' Recall: '+ str(logo_recall))
l4 = str ('Favicon->' + ' Precision: ' + str(favicon_precision)+ ' Recall: '+ str(favicon_recall))

with open('summery2.txt','w') as file:
    file.write(l1 +'\n')
    file.write(l2 + '\n')
    file.write(l3 + '\n')
    file.write(l4 + '\n')
    file.close()

print (l1)
print (l2)
print (l3)
print (l4)