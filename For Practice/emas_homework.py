import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
# requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
from bs4 import BeautifulSoup
import lxml
import json


recruiting_unit = []
recruiting_major = []

def getHTMLtext(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.146 Safari/537.36'}
    r = requests.get(url = url, headers = headers, verify = False)
    r.encoding = "utf-8"
    soup = BeautifulSoup(r.text, 'lxml') # lxml HTML解析器、速度快、文檔容錯能力強、需要安裝C語言庫
    # print(soup.find_all('a', {"href" : "sszyml_list.asp?zydm=050101&zsnd=2020&yxdm=101  "}))
    # get [<a href="sszyml_list.asp?zydm=050101&amp;zsnd=2020&amp;yxdm=101  " target="_blank"><font face="����">(050101)����ѧ</font></a>]
    
    return [str(soup.find_all("a", {"href":"yxjj_detail.asp?yxdm=" + str(i) + "&zsnd=2020 "})) for i in range(101, 166)]

url = "https://yjszs.ecnu.edu.cn/system/sszszyml_list.asp"
h = getHTMLtext(url)

with open("homework.json","w",encoding = "UTF-8") as json_file:
    json.dump("招生單位： ", json_file, separators=(",",":"))
    json.dump(h,json_file, separators= (",",":"))