import unittest

from creeper.settings import DOWNLOAD_DIR
from creeper.spider import LiQuSpider


class Test(unittest.TestCase):

    download_dir = DOWNLOAD_DIR

    def liqu_spider(self):
        url = "https://www.liqucn.com/comment/28740.shtml"
        spider = LiQuSpider(url)
        spider.parse()
        spider.to_excel("test1")

    def test_all(self):
        self.liqu_spider()


if __name__ == "__main__":
    unittest.main()
