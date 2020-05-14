# I am Spider Man!!!
import abc

import pandas as pd
import requests
from bs4 import BeautifulSoup
# from multiprocessing import Pool
from colorama import Fore, init

from creeper.settings import DOWNLOAD_DIR


class Spider(metaclass=abc.ABCMeta):

    def __init__(self, target_url: str, color: bool = True):

        init(autoreset=color)
        self.url = target_url  # 需要爬取的url
        self.html: str = None  # 等待解析的html数据
        self.data = None

    def get_one_page(self, url: str):
        '''get page source html'''
        # 设置代理
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 SE 2.X MetaSr 1.0'
        }

        try:
            response = requests.get(url, headers=headers)
            assert response.status_code == 200, "没有返回正确的状态码"
            self.html = response.content.decode('utf-8', 'ignore')
            self.soup = BeautifulSoup(self.html, 'lxml')
        except ConnectionError:
            print('Error occurred')
            return None
        return self.html

    def save(self, filename: str, data: str):
        '''保存为txt文本数据

        Arguments:
            filename {str} -- 文件名
            data {str} -- 文本数据
        '''

        download_dir = DOWNLOAD_DIR
        file_path = download_dir / f"{filename}.txt"
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(self.data)

    @abc.abstractclassmethod
    def parse(self):
        '''数据清理
        '''
        return None


class LiQuSpider(Spider):
    '''爬取历趣网app评论滴滴滴滴爬虫
    '''

    def parse(self):

        self.get_one_page(self.url)
        # 获取评论页数
        _, comments_page = self.soup.find(
            'div', "page").a.get("href").split("=")
        # 因为包含当前页
        comments_page = int(comments_page) + 1
        cache_data = list()
        for i in range(comments_page, 0, -1):
            new_url = f"{self.url}?page={i}"
            self.get_one_page(new_url)
            comments_box = self.soup.find(id="pl_list").find_all('li')
            for li in comments_box:
                cache_data.append(list(li.stripped_strings))
            print(Fore.BLUE + f"url:{new_url},已成功爬取")
        cache_data = list(zip(*cache_data))
        # 很随意的代码,不要这么用
        data = {
            "时间": pd.Series(cache_data[0]),
            "用户": pd.Series(cache_data[1]),
            "评论": pd.Series(cache_data[2])
        }
        data = pd.DataFrame(data)
        self.data = data.set_index(['时间'])

    def to_excel(self, filename: str):

        download_dir = DOWNLOAD_DIR
        file_path = download_dir / f"{filename}.xlsx"
        assert self.data is not None, "data 数据为空"
        self.data.to_excel(file_path)
        print(Fore.YELLOW + "保存成功")
