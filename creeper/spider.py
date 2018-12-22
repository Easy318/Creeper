# I am Spider Man!!!
import requests
import re
# import time
from bs4 import BeautifulSoup
# from multiprocessing import Pool
from colorama import init, Fore
from . import settings
from collections import defaultdict
import pandas as pd


class Spider:

    def __init__(self, target_url, color=True):

        init(autoreset=color)
        self.url = target_url  # 需要爬取的url
        self.html: str = None  # 等待解析的html数据
        self.result: str = None  # 保存结果
        self.data = None

    def get_one_page(self):
        '''get page source html'''
        # 设置代理
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 SE 2.X MetaSr 1.0'
        }

        try:
            response = requests.get(self.url, headers=headers)
            assert response.status_code == 200, "没有返回正确的状态码"
            self.html = response.content.decode('utf-8', 'ignore')
        except ConnectionError:
            print('Error occurred')
            return None

    def save(self, filename: str):
        '''保存数据

        Arguments:
            filename {str} -- [所要保存数据的文件名]
        '''

        download_dir = settings.DOWNLOAD_DIR
        file_path = download_dir / f"{filename}.txt"
        assert self.result is not None, f"result is not data"
        with open(file_path, "a+", encoding="utf-8") as f:
            f.write(self.result)

    def parse_html(self)->str:
        '''解析策略

        Returns:
            str -- [解析后清理过的数据]
        '''

        return None

    def run(self):
        '''执行爬虫
        '''

        self.get_one_page()
        assert self.html is not None, "未能正确抓取到html页面"
        self.parse_html()
        # print(result)


class FictionSpider(Spider):
    '''爬取小说滴滴滴滴爬虫
    '''

    def parse_html(self):

        soup = BeautifulSoup(self.html, 'lxml')
        fiction_info = soup.find('div', "readAreaBox content")
        title = fiction_info.find('h1').get_text(strip=True)
        content = fiction_info.find('div', "p").get_text("\n  ", strip=True)
        result = f"\n\n{title}\n\n  {content}"
        if result:
            pattern = re.compile('(.*?)本书首发来自17K小说网(.*?)', re.S)
            result = re.search(pattern, result).group(1)
            if result:
                # self.save(result)
                print(Fore.BLUE + f"STATUS: 成功爬取并保存 URL: {self.url} ")
                return result
            else:
                print(Fore.RED + f"STATUS: 爬取失败 URL: {self.url}")
        else:
            print(Fore.RED + f"STATUS: 解析失败 URL: {self.url}")


class LiQuSpider(Spider):
    '''爬取历趣网app评论滴滴滴滴爬虫
    '''

    __data = defaultdict(list)

    def parse_html(self):

        soup = BeautifulSoup(self.html, 'lxml')

        # print(cache_data)

        # 获取评论页数
        _, comments_page = soup.find('div', "page").a.get("href").split("=")
        # 因为包含当前页
        comments_page = int(comments_page) + 1
        cache_data = list()
        url_cache = self.url
        for i in range(comments_page, 0, -1):
            self.url = f"{url_cache}?page={i}"
            self.get_one_page()
            comments_box = soup.find(id="pl_list").find_all('li')
            for li in comments_box:
                cache_data.append(list(li.stripped_strings))
            print(Fore.BLUE + f"url:{self.url},已成功爬取")
        cache_data = list(zip(*cache_data))

        # 很随意的代码,不要这么用
        data = {
            "时间": pd.Series(cache_data[0]),
            "用户": pd.Series(cache_data[1]),
            "评论": pd.Series(cache_data[2])
        }
        self.data = pd.DataFrame(data)

    def to_excel(self, filename: str):

        download_dir = settings.DOWNLOAD_DIR
        file_path = download_dir / f"{filename}.xlsx"
        assert self.data is not None, "data 数据为空"
        self.data.to_excel(file_path)
        print(Fore.YELLOW + "保存成功")
