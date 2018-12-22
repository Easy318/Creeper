import unittest
from creeper import settings
from creeper.spider import FictionSpider, LiQuSpider


class Test(unittest.TestCase):

    download_dir = settings.DOWNLOAD_DIR

    def test_all(self):
        # self.fiction_spider()
        self.liqu_spider()
        pass

    def fiction_spider(self):

        url = "http://www.17k.com/chapter/271047/6336386.html"
        spider = FictionSpider(url)
        spider.run()

    def liqu_spider(self):

        url = "https://www.liqucn.com/comment/28740.shtml"
        # url = "https://www.liqucn.com/comment/20799.shtml"
        spider = LiQuSpider(url)
        spider.run()
        spider.to_excel("test1")


if __name__ == "__main__":
    unittest.main()
