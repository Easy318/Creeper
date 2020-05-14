from creeper.spider import LiQuSpider

url = "https://www.liqucn.com/comment/28740.shtml"
spider = LiQuSpider(url)
spider.parse()
# 参数为保存的文件名
spider.to_excel("同程旅游App评论")
