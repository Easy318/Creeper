# 爬取100+个小故事

**运行:**

```python
# 已失效
python creep_start.py
```

~~就可以爬取到目标站点100+小故事,默认放在fiction_data目录下,以后可能会有扩展~~

## 更新

更新时间: 2018年12月22日13:03:05

- 理论上可以爬取历趣网下所有app的评论
- 优化了爬虫框架结构,更方便修改
- 增加了测试
- 删除了 creep_start.py模块
- 如果爬取失败,请检查网络连接并重新尝试或联系作者
- 爬取100个小故事已失效

## 使用

第一次使用请先运行:

```python
# pip 安装慢的请换成国内镜像源
# 第一步
pip install -r requirements.txt
# 第二步
python addProject.py
```

爬取历趣网app评论:

```python
# 先打开想要爬取的app评论网页
# 复制该网页
# 替换url
# 数据默认会保存在 ./download文件夹下

from creeper.spider import LiQuSpider

url = "https://www.liqucn.com/comment/28740.shtml"
spider = LiQuSpider(url)
spider.parse()
# 参数为保存的文件名
spider.to_excel("同程旅游App评论")
```
