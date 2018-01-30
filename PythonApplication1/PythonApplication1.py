'''from urllib import request
import http.cookiejar
import re
url = 'http://jwc.zafu.edu.cn/'
#url = 'http://101.132.126.172'
#url = 'http://lijiajie.top'
#print('第一种方法:')
response1 = request.urlopen(url)
print(response1.getcode())
#print(len(response1.read()))
#print('第二种方法')
req = request.Request(url)
req.add_header('user-agent', 'Mozilla/5.0')
response2 = request.urlopen(req)
print(response2.getcode())
#print(len(response2.read()))
#print('第三种方法')
cj = http.cookiejar.CookieJar()
opener = request.build_opener(request.HTTPCookieProcessor(cj))
request.install_opener(opener)
response3 = request.urlopen(url)
print(response3.getcode())
print(cj)
#print(response3.read())
html_doc = response3.read()
from bs4 import BeautifulSoup
soup = BeautifulSoup(html_doc, "html.parser", from_encoding="gb2312")
print("获取所有链接：")
links = soup.find_all("a")
for link in links:
    print(link.name +"   "+ link['href'] +"   "+ link.get_text())
print("正则匹配")
link_node = soup.find('a',href = re.compile(r"default2"))
print(link_node.name +"   "+ link_node['href'] +"   "+ link_node.get_text())
print("获取p段落")
p_node = soup.find('p',class_ = 'title')
print(p_node.name +"   "+ p_node.get_text())
'''
import url_manager,html_parser,html_downloader,html_outputer
class SpiderMain(object):
    def __init__(self):
        self.urls = url_manager.UrlManager()
        self.downloader = html_downloader.HtmlDownloader()
        self.parser = html_parser.HtmlParser()
        self.outputer = html_outputer.HtmlOutputer()
    def craw(self, root_url):
        count = 1
        self.urls.add_new_url(root_url)
        while(self.urls.has_new_url()):
            try:
                new_url = self.urls.get_new_url()
                print("craw %d : %s"%(count, new_url))
                html_cont = self.downloader.download(new_url)
                new_urls, new_data = self.parser.parse(new_url, html_cont)
                self.urls.add_new_urls(new_urls)
                self.outputer.collect_data(new_data)
                if(count == 1000):
                    break
                count += 1
            except Exception as error:
                print(error)
        self.outputer.output_html()
if(__name__ == "__main__"):
    root_url = "https://baike.baidu.com/item/Python/407313?fr=aladdin"
    obj_spider = SpiderMain()
    obj_spider.craw(root_url)