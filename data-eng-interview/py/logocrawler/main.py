import scrapy
import csv
import pandas as pd
import os

class Parser(scrapy.Spider):
    name = 'logo-favicon'

    def clean_url(self, url):
        url = url.replace("['", "")
        url = url.replace("']", "")
        url = url.lower()
        return url

    def start_requests(self):
        with open('websites.csv', 'r') as file:
            data = file.read()

        with open('result.csv', 'a+') as file:
            writer = csv.writer(file)
            writer.writerow(['website', 'logo', 'favicon'])
            file.close()

        urls = ['http://www.'+x for x in data.split('\n')]

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        ext_list = [".png", ".gif", ".jpg", ".tif", ".tiff", ".bmp", ".svg", ".ico"]

        res_url = str(response.url).lower()
        parts = len(res_url.split("/"))
        if len(res_url.split("/")[parts-1]) == 0:
            root_url = res_url.split("/")[parts-2]
        else:
            root_url = res_url.split("/")[parts - 1]

        brand = str(response.url).split('.')[1]
        img_url_list = []

        flag = False
        for tag_a in response.xpath('//a'):
            for tag_img in tag_a.xpath('.//img'):
                img_url = str(tag_img.xpath('@src').extract())
                img_url = self.clean_url(img_url)
                lfc = img_url.find('logo')
                if lfc > 0:
                    flag = True
                    img_url_list.append(img_url)

        if not flag:
            for tag_div in response.xpath('//div'):
                for tag_img in tag_div.xpath('.//img'):
                    img_url = str(tag_img.xpath('@src').extract())
                    img_url = self.clean_url(img_url)
                    lfc = img_url.find('logo')
                    if lfc > 0:
                        flag = True
                        img_url_list.append(img_url)

        if not flag:
            for tag_a in response.xpath('//a'):
                a_href = str(tag_a.xpath('@href').extract())
                a_href = self.clean_url(a_href)
                if a_href[:6] == str("index.") or a_href == root_url:
                    for tag_img in tag_a.xpath('.//img'):
                        img_url = str(tag_img.xpath('@src').extract())
                        img_url = self.clean_url(img_url)
                        img_name, img_ext = os.path.splitext(img_url)

                        tag_class = str(tag_img.xpath('@class').extract()).lower().strip()
                        title = str(tag_img.xpath('@title').extract()).lower().strip()
                        alt = str(tag_img.xpath('@alt').extract()).lower().strip()

                        if img_ext in ext_list or tag_class.find("logo") > 0 or title.find("logo") > 0 \
                                or title.find(brand) > 0 or alt.find("logo") > 0 or alt.find(brand) > 0 :
                            img_url_list.append(img_url)

        logo_url =''

        if len(img_url_list) == 1:
            logo_url = img_url_list[0]

        elif len(img_url_list) >1:
            for url in img_url_list:
                if url.find('logo') >0 or url.find(brand) > 0:
                    logo_url = url
                    break

        # Find Favicons from the page
        favicon_url = ''
        for link in response.xpath('//link'):
            link_href = str(link.xpath('@href').extract())
            link_href = self.clean_url(link_href)
            if link_href.find('ico') > 0:
                favicon_url = link_href
                break

        with open('result.csv','a+') as file:
            writer = csv.writer(file)
            writer.writerow([root_url, logo_url, favicon_url])
            file.close()

    def closed(self, reason):
        src = pd.read_csv('websites.csv').fillna(0)
        res = pd.read_csv('result.csv').fillna(0)
        ls = len(src) + 1
        lr = len(res)
        tl = len([x for x in list(res['logo']) if x != 0])
        tf = len([x for x in list(res['favicon']) if x != 0])

        logo_precision = (tl / lr) * 100  # TruePositives / (TruePositives + FalsePositives)
        logo_recall = tl / (tl + (ls - lr))  # TruePositives / (TruePositives + FalseNegatives)

        favicon_precision = (tf / lr) * 100  # TruePositives / (TruePositives + FalsePositives)
        favicon_recall = tf / (tf + (ls - lr))  # TruePositives / (TruePositives + FalseNegatives)

        l1 = str ('>>>>RESULT<<<<')
        l2 = str ('Response Found: ' + str(lr)+ ' Logo Found: '+ str(tl) + ' Favicon Found: '+ str(tf)+ ' Request Failed: '+ str(ls-lr))
        l3 = str ('Logo ->' + ' Precision: ' + str(logo_precision) + ' Recall: '+ str(logo_recall))
        l4 = str ('Favicon->' + ' Precision: ' + str(favicon_precision)+ ' Recall: '+ str(favicon_recall))

        with open('summery.txt','w') as file:
            file.write(l1 +'\n')
            file.write(l2 + '\n')
            file.write(l3 + '\n')
            file.write(l4 + '\n')
            file.close()

        print (l1)
        print (l2)
        print (l3)
        print (l4)


