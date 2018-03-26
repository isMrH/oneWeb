import requests
from bs4 import BeautifulSoup
import re
def laod_news():
    content = []
    for page in range(1,23):
        urls = 'https://laod.cn/news/page/'+str(page)
        res = requests.get(urls)
        text = res.text
        soup = BeautifulSoup(text,"lxml")
        list2 = soup.find_all('article',class_=('wow'))
        for href in list2:
            a_href = href.find('a')
            url = a_href['href']
            content_dict = contentparse(url)
            content.append(content_dict)

    return content
def contentparse(url):
    res = requests.get(url)
    text = res.text
    soup = BeautifulSoup(text,'lxml')
    title = soup.find('h1',attrs={'class':'entry-title'}).getText()
    reg = '([0-9]{4})-([0-9]{2})-([0-9]{2})'
    time = soup.find('ul',attrs={'class':'spostinfo'}).getText()
    date = re.search(reg,time).group()
    print(url)
    context = str(soup.find('div',attrs={'class':'single-content'}))
    content = re.sub('<a(.*?)>', "",context.replace('>\n', '>').replace('single-content', 'entry').replace('</a>', ''))


    content_dict = {'title': title, 'date': date, 'content': content, 'src': url, 'mid': '5'}
    return content_dict
if __name__ == '__main__':
    laod_news()






