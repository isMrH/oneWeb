import requests
from bs4 import BeautifulSoup
from exts import db
from models import Article
from sqlalchemy import or_, func
# 访问链接
dw_url = "http://www.zdfans.com/apk"

# 下载该url下的信息
def dw_page(url):    
    # 设置请求头 伪装浏览器
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'}
    # proxies = {
    #     'https':'121.30.109.112:80',
    #     'http':'27.10.232.26:8118',
    # }

    data = requests.get(url,headers=headers).content
    return data
# 用bs4解析网页
def parse_html(html):
    soup = BeautifulSoup(html,'lxml')
    software_list_soup = soup.find('ul',attrs={'class':'excerpt'})

    software_href_list = []
    # 遍历每一条信息
    for software_li in software_list_soup.find_all('li'):
        detail = software_li.find('a')
        
        software_href = detail['href']
        print(software_href )
        aid = db.session.query(func.count(Article.aId)).filter(Article.src==software_href).scalar()
        print(aid)
        if aid:
            return software_href_list, None
        else:
            software_href_list.append(software_href)
    current = soup.find('span',attrs={'class':'current'})


    # 判断是否还有下一页
    if current.next_sibling:
        page = int((current).getText())+1
        next_page = dw_url + "/page/" + str(page)
    else:
        next_page = None
    # 如果有下一页 返回下一页链接 否则返回 None
    if next_page:
        return software_href_list,next_page
    return software_href_list,None

def nextparse(href):

    soup = BeautifulSoup(href,'lxml')
    content = str(soup.find('div',attrs={'class':'entry'}))
    title = soup.find('h1',attrs={'class':'meta-tit'}).find('a').getText()
    date = soup.find('p', attrs={'class':'meta-info'}).getText()[1:11]
    print(date)

    return content, title, date
def content_main():
    content_list = []
    content_dict = {}
    url = dw_url
   # with codecs.open('software_href_list','wb',encoding='utf-8') as fp:
    while url:
        html = dw_page(url)
        href, url = parse_html(html)

        for h in href:
            content_page = dw_page(h)
            content, title, date = nextparse(content_page)

            content_dict = {'content': content, 'title': title, 'src': h, 'date': date, 'mid': '8'}
            content_list.append(content_dict)
    return content_list

            #fp.write(u'{href}\n'.format(href='\n'.join(href)))

if __name__ == '__main__':
    content_main()
