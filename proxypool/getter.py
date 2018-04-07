from .utils import get_page
from pyquery import PyQuery as pq
import re
import time


class ProxyMetaclass(type):
    """
        元类，在FreeProxyGetter类中加入
        __CrawlFunc__和__CrawlFuncCount__
        两个参数，分别表示爬虫函数，和爬虫函数的数量。
    """

    def __new__(cls, name, bases, attrs):
        count = 0
        attrs['__CrawlFunc__'] = []
        for k, v in attrs.items():
            if 'crawl_' in k:
                attrs['__CrawlFunc__'].append(k)
                count += 1
        attrs['__CrawlFuncCount__'] = count
        return type.__new__(cls, name, bases, attrs)


class FreeProxyGetter(object, metaclass=ProxyMetaclass):
    def get_raw_proxies(self, callback):
        proxies = []
        print('Callback', callback)
        for proxy in eval("self.{}()".format(callback)):
            print('Getting', proxy, 'from', callback)
            proxies.append(proxy)
        return proxies

    def crawl_data5u(self):
        for i in ['gngn', 'gnpt']:
            time.sleep(1)
            start_url = 'http://www.data5u.com/free/{}/index.shtml'.format(i)
            html = get_page(start_url)
            ip_adress = re.compile('<ul class="l2">.*?span><li>(.*?)</li></span>.*?"port.*?">(.*?)</li></span>.*?</ul>',
                                   re.S)
            # \s * 匹配空格，起到换行作用
            re_ip_adress = ip_adress.findall(html)
            for ip in re_ip_adress:
                result = ':'.join(ip)
                yield result.replace(' ', '')

    def crawl_ip181(self):
        start_url = 'http://www.ip181.com/'
        html = get_page(start_url)
        ip_adress =re.compile('{.*?"port".*?"(.*?)".*?"ip".*?"(.*?)".*?}',re.S)
        re_ip_adress = ip_adress.findall(html)
        for ip in re_ip_adress:
            result = ':'.join(ip[::-1])
            yield result.replace(' ', '')

    def crawl_kuaidaili(self):
        for page in range(1, 4):
            time.sleep(1)
            # 国内高匿代理
            start_url = 'https://www.kuaidaili.com/free/inha/{}/'.format(page)
            html = get_page(start_url)
            ip_adress =re.compile('"IP">(.*?)</td>.*?"PORT">(.*?)</td>', re.S)
            re_ip_adress = ip_adress.findall(str(html))
            for ip in re_ip_adress:
                result = ':'.join(ip).strip()
                # import requests
                # proxies = {"http": "http://"+result, }
                # headers = {
                #     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
                # }
                # try:
                #     r=requests.get('http://www.baidu.com',proxies=proxies,headers=headers)
                #     print(r)
                # except:pass
                yield result.replace(' ', '')

    def crawl_xicidaili(self):
        for page in range(1, 4):
            time.sleep(1)
            start_url = 'http://www.xicidaili.com/wt/{}'.format(page)
            html = get_page(start_url)
            ip_adress = re.compile('<tr class.*?country">.*?<td>(.*?)</td>.*?<td>(.*?)</td>.*?</tr>',re.S)
            # \s* 匹配空格，起到换行作用
            re_ip_adress = ip_adress.findall(str(html))
            for ip in re_ip_adress:
                result = ':'.join(ip).strip()
                yield result.replace(' ', '')

    def crawl_daili66(self, page_count=4):
        start_url = 'http://www.66ip.cn/{}.html'
        urls = [start_url.format(page) for page in range(1, page_count + 1)]
        for url in urls:
            time.sleep(1)
            print('Crawling', url)
            html = get_page(url)
            if html:
                doc = pq(html)
                trs = doc('.containerbox table tr:gt(0)').items()
                for tr in trs:
                    ip = tr.find('td:nth-child(1)').text()
                    port = tr.find('td:nth-child(2)').text()
                    yield ':'.join([ip, port])



