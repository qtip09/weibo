import requests
from requests.exceptions import RequestException
from bs4 import BeautifulSoup
import re
import os
pattern=re.compile('//weibo.com/(.*)',re.S)
pattern_img=re.compile('(https://weibo.cn/mblog/picAll/.*)')


class Items():              #创建一个类表示所要获取的信息
    def __init__(self,title,author,creat_at,content,img):

        self.creat_at = creat_at
        self.content = content




def Get_Html(url,cookies):   #定义一个全局函数，用来获取网页源代码html
    try:
        headers ={
                'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'
        }
        response = requests.get(url = url,headers = headers,cookies = cookies)
        if response.status_code == 200:
            global encode_content
            encode_content = response.text
            if response.encoding == 'ISO-8859-1':
                encodings = response.utils.get_encodings_from_content(response.text)
                if encodings:
                    encodings = encodings[0]
                else:
                    encodings = response.apparent_encoding
                encode_content = response.text.decode(encodings,'replace')
            return encode_content
        return None
    except RequestException:
        return None
def Get_Img(url,cookies):
    try:
        headers ={
                'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'
        }
        response = requests.get(url = url,headers = headers,cookies = cookies)
        if response.status_code == 200:
            return response.content
        return None
    except RequestException:
        return None


def Search_Vertify(url,Cookies):    #定义一个
    html = Get_Html(url,Cookies)
    arr_url=[]
    arr_soup_vertify=[]

    soup_url = BeautifulSoup(html,"lxml").select('.avator a')
    #print(soup_url)
    for i in soup_url:
        arr_url.append(i.attrs['href'])

    soup_vertify = BeautifulSoup(html,"lxml").select('.name')
    for j in soup_vertify:
        name=j.get_text()
        arr_soup_vertify.append(name)
    #print(arr_soup_vertify)
    #print(len(arr_soup_vertify))



    select_dict = dict(zip(arr_soup_vertify,arr_url))
    count=1
    for n,m in select_dict.items():
        print(str(count)+"---"+"http:"+m+":"+n)
        count+=1
    #print(select_dict)
    print("请选择你要爬取的用户的认证信息")
    notes = input().strip()
    Url = select_dict[notes]
   
    return Url


class Get_Weibo_TextInfo(object):

    def __init__(self, url,cookies,nickname):
        self.url = url
        self.cookies=cookies
        self.nickname=nickname

        self.content_dict = {}
        self.Spider(self.url,self.cookies)

        self.WriteTextIntoFile(self.content_dict,self.nickname)

    def PageUrl(self,url,page):
        url=url+'?page='+str(page)
        return url


    def Spider(self,url,cookies):
        soup=BeautifulSoup(Get_Html(url,cookies),'lxml')
        text_1=soup.select('.c')
        creat=soup.select('.ct')
        arr_creat_at=[]
        for creat_at in creat:
            creat_at =creat_at.get_text()
            arr_creat_at.append(creat_at)
        arr_text=[]
        for text in text_1:
            text = text.get_text()
            arr_text.append(text)
        self.content_dict = dict(zip(arr_creat_at,arr_text))
        return self.content_dict



    def WriteTextIntoFile(self,content_dict,nickname):
        with open(nickname+'/'+nickname+".txt",'wb') as f:
            for key,value in content_dict.items():
                f.write(bytes(key,encoding='utf-8'))
                f.write(bytes(':\n',encoding='utf-8'))
                f.write(bytes(value,encoding='utf-8'))



class GetImgInfo():
    def __init__(self,url,cookies):
        self.url=url
        self.cookies=cookies
        self.img=[]
        self.spider(self.url,self.cookies)
        self.WriteImgToFile(self.img,self.cookies)


    def spider(self,url,cookies):
        soup_img=BeautifulSoup(Get_Html(url,cookies),'lxml').select('.c a')
        if soup_img!= None:
            for img_ in soup_img:
                src=img_.attrs['href']
                img_src=re.findall(pattern_img,src)
                for t in img_src:
                    if t!=None:
                        P=BeautifulSoup(Get_Html(url=t, cookies=cookies),'lxml').select('img')
                        print(P)
                        for pic in P:
                            self.img.append(pic.attrs['src'])
            return self.img


    def WriteImgToFile(self,img_src,cookies):
        count=1
        for img in img_src:
            with open(nickname+'/'+str(count)+"."+img[-3:],'wb') as f:
                f.write(Get_Img(img,cookies=cookies))
                count+=1


if  __name__ == '__main__':
    nickname=input("请输入要查找的用户昵称\n")
    url='https://s.weibo.com/user/'+nickname
    Cookies={'Cookies':'T_WM=e7be89faad27d0bede8b90cd570db089; WEIBOCN_FROM=1110006030; TMPTOKEN=lqPMlPf3n4dstKPyET0abNIqVG3jULkaHzhsCXnWjaPNQwtc3sMB5syOlrAJFCR0; SCF=AkiabZIltbwSEEOzBqgns_USmvOFFU2Yj_F1nVkBSiAtl9p6nsZRCcXPYEDqsvaENjO34BJyBHyj3kvNLs3A1NU.; SUB=_2A2520s-EDeRhGeRG4lEX8ifMzD2IHXVSPNHMrDV6PUJbkdANLWvVkW1NTeNujFBzLiWiD-KbW7necAoxI6gThC7U; SUHB=0cSnArq_6oSmHz; SSOLoginState=1540800469; MLOGIN=1; M_WEIBOCN_PARAMS=lfid%3D231583%26luicode%3D20000174%26uicode%3D20000174'}
    name=Search_Vertify(url,Cookies)
    name_=re.findall(pattern,name)
    URL='http://weibo.cn/'+"".join(name_)
    print(URL)
    path=os.path.abspath('.')+'/'+nickname
    if not os.path.exists(path):
        os.mkdir(path)

    txt=Get_Weibo_TextInfo(url=URL,cookies=Cookies,nickname=nickname)
    img=GetImgInfo(url=URL,cookies=Cookies)
