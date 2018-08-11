# coding:utf-8
import os
import requests
from urllib import request
from lxml import etree
from multiprocessing.pool import Pool
from requests import RequestException
'''
url = 'http://sc.chinaz.com/biaoqing/'
header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36',
}
#
# req = request.Request(url,headers=header)
# resp = request.urlopen(req)
# if resp.status == 200 :
#     html = resp.read().decode()
#     print(html)
resp = requests.get(url,headers=header)
if resp.status_code == 200 :
    html = resp.content.decode()
    # 解析网页
    et = etree.HTML(html)
        imgs = et.xpath("//div[@class='right']//div[@class='num_1']//img/@src2")
        href = et.xpath("//div[@class='up']/div[@class='num_2']/a/@href")
        titles = et.xpath("//div[@class='up']/div[@class='num_2']/a/@title")
'''
def get_one_pag(url,header):
    try:
        resp = requests.get(url,headers=header)
        if resp.status_code == 200:
            return resp.content.decode()
        return None
    except RequestException:
        return None

def parse_one_page(html):
    et = etree.HTML(html)
    href = et.xpath("//div[@class='up']/div[@class='num_2']/a/@href")
    titles = et.xpath("//div[@class='up']/div[@class='num_2']/a/@title")
    for title in titles:
        os.mkdir(title)
        print(title,'创建成功')
        for hr in href:
            req = request.Request(hr)
            resp = request.urlopen(req)
            html = resp.read().decode(encoding='utf-8')
            et = etree.HTML(html)
            imgs = et.xpath("//div[@class='down_img']/div[3]/img/@src")
            for img in imgs:
                imgname = img.split('/')[-1]
                filename = './{}/{}'.format(title,imgname)
                request.urlretrieve(img,filename=filename)
def main(index):
    url = 'http://sc.chinaz.com/biaoqing/'+str(('index_{}.html').format(index))
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36',
    }
    html = get_one_pag(url,header)
    parse_one_page(html)

if __name__ == '__main__':
    pool = Pool()
    pool.map(main,[i for i in range(3,5)])