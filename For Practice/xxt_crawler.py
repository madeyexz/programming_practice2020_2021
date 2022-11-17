from bs4 import BeautifulSoup
import requests
import re




def make_page_lst():
    # page_lst = ['http://news.ustb.edu.cn/xinwendaodu/']
    page_lst = []
    for i in range(2,860):
        page_lst.append('http://news.ustb.edu.cn/xinwendaodu/index_'+ str(i) + '.html')
    return page_lst

def make_url_lst(page_lst):
    url_lst = []
    for i in page_lst:
        response = requests.get(i)
        soup = BeautifulSoup(response.text, 'lxml')
        semi_html = soup.findall('div',class_='bkrw_centent').findall('a', href = re.compile('/xinwendaodu/.*html/'))
        for j in semi_html:
            url_lst.append('http://news.ustb.edu.cn/' + j)
    return url_lst

page_lst = make_page_lst()
url_lst = make_url_lst(page_lst)

# for i in url_lst:
#     response = requests.get(i)
#     soup = BeautifulSoup(response.text,'lxml')

print(url_lst)


# 標題
# 點次數
# 時間
