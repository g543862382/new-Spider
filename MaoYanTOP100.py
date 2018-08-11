import json
import re
from multiprocessing.pool import Pool

import requests
from requests import RequestException
from urllib import request
'''使用request和re抓取猫眼电影Top100
    url = http://maoyan.com/board/4?
    urls = http://maoyan.com/board/4?offset=0
'''
# def get_one_peg(url):
#     resp = request.urlopen(url)
#     return resp.read().decode('utf-8')
def get_one_peg(url,header):
    # 请求目标网站使用 try 方式请求的时候出现一些 304 404 500 问题导致程序停止
    # 可以使用 urllib中 request 和 requests 来请求目标网站
    # requests 的时候 要设置请求头
    # 注意编码问题
    try:
        resp = requests.get(url,headers=header)
        if resp.status_code == 200:
            print('-----get success------')
            return resp.text
        return None
    except RequestException:
        return None
def parse_one_pag(html):
    # 通过re 来对目标网站进行抓取  住： re 并不太好用
    # 建议使用xpaht 或者 BeatifulSoup 来进行抓取
    # 爬虫中建议多使用迭代器 减小内存的消耗
    pattern = re.compile('<dd>.*?board-index.*?>(\d+)</i>.*?data-src="(.*?)".*?name"><a.*?>(.*?)</a>.*?stat">(.*?)</p>.*?releasetime">(.*?)</p>.*?integer">(.*?)</i>.*?fraction">(.*?)</i>.*?</dd>',re.S)
    items = re.findall(pattern,html)
    for itme in items:
        yield {
            'index':itme[0],
            'image':itme[1],
            'title':itme[2],
            'actor':itme[3].strip()[3:],# strip() 方法用于移除字符串头尾指定的字符
            'time':itme[4].strip()[5:],
            'score':itme[5]+itme[6],
        }
def write_to_file(content):
    with open('result.txt','a',encoding='utf-8') as f:
        f.write(json.dumps(content,ensure_ascii=False)+'\n')
        f.close()
def main(offset):
    header = {
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding':'gzip, deflate',
        'Accept-Language':'zh-CN,zh;q=0.9',
        'Connection':'keep-alive',
        'Cookie':'__mta=174431901.1533965877318.1533968206245.1533968448700.13"; uuid_n_v=v1; uuid=B31090609D2811E89404A3B091453017177162ECF25B4658B8BB963718F54C03; _csrf=1621b1ab3ea61953bd3e817e90928cda5ec77e1b4198472c3aefaa1dceec4b1c; _lx_utm=utm_source%3DBaidu%26utm_medium%3Dorganic; _lxsdk_cuid=165277dbfffc8-08075a5cc97fa6-47e1137-100200-165277dbfffc8; _lxsdk=B31090609D2811E89404A3B091453017177162ECF25B4658B8BB963718F54C03; __mta=174431901.1533965877318.1533965877318.1533965879604.2"; _lxsdk_s=%7C%7C0',
        'Host':'maoyan.com',
        'Upgrade-Insecure-Requests':'1',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36',
    }
    url = 'http://maoyan.com/board/4?offset='+str(offset)
    html = get_one_peg(url,header)
    for item in parse_one_pag(html):
        print(item)
        write_to_file(item)

if __name__ == '__main__':
    # 采用多进行可以提高抓取的速度
    pool = Pool()
    pool.map(main,[i*10 for i in range(10)])
