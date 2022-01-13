import requests, os
import warnings 
warnings.filterwarnings("ignore")
from lxml import etree
import urllib
from urllib.request import urlopen
import re, time
 
def get_index_path(url):#获取主页链接
    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 8.0; Pixel 2 Build/OPD3.170816.012) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Mobile Safari/537.36 Edg/84.0.522.52'
    }
    res = requests.get(url, headers=headers, verify =False).text
    res = etree.HTML(res)
    index_path = res.xpath('/html/body/div[1]/div[1]/div/div[2]/div/li/a/@href')
    list = []
    for link in index_path:
        aurl = 'https://tuli.cc' + link
        list.append(aurl)
    del list[0]
    print('获取套图链接结束。。。')
    return list

def get_page(urls):#获取页数
    print('开始获取页数。。。')
    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 8.0; Pixel 2 Build/OPD3.170816.012) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Mobile Safari/537.36 Edg/84.0.522.52'
    }
    res = requests.get(urls, headers=headers, verify =False).text
    res = etree.HTML(res)
    page = re.findall(r"\d+?\d*", str(res.xpath('/html/body/div[1]/div[8]/div[3]/ul/li[8]/a/@href')))
    print('获取页数结束。。。')
    return page

def get_page_url(urls, page):#获取套图链接
    temp_page = urls
    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 8.0; Pixel 2 Build/OPD3.170816.012) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Mobile Safari/537.36 Edg/84.0.522.52'
    }
    i = 1
    url_list = []
    while i <= int(page[0]):

        if i != 1:
            temp_page = str(urls) + "list_" + str(i) + ".html"
        try:
            res = requests.get(temp_page, headers=headers, verify =False).text
        except BaseException:
            time.sleep(5)
            res = requests.get(temp_page, headers=headers, verify =False).text
        res = etree.HTML(res)
        data = res.xpath('/html/body/div[1]/div[8]/div[1]/div/a/@href')
        for j in range(len(data)):
            url_list.append("https://tuli.cc" + str(data[j]))
            
        i += 1
    url_list = sorted(set(url_list),key=url_list.index)
    return url_list

def get_image_page(urls):#获取图片页数
    print('开始获取图片页数。。。')
    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 8.0; Pixel 2 Build/OPD3.170816.012) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Mobile Safari/537.36 Edg/84.0.522.52'
    }
    
    res = requests.get(urls, headers=headers, verify =False).text
    res = etree.HTML(res)
    image_page = res.xpath('/html/body/div[1]/div[5]/div/div[1]/div[3]/div[3]/ul/li[last()-1]/a/text()')
    print('获取图片页数结束。。。')
    return image_page[0]
    

def get_image_url(url_list):#获取套图链接里面的图片
    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 8.0; Pixel 2 Build/OPD3.170816.012) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Mobile Safari/537.36 Edg/84.0.522.52'
    }
    for n in url_list:#url链接
        a = 0
        image_list = []
        temp_url = n

        fo = open("url.txt", "r")
        for aaa in fo.readlines():
            if aaa.strip() == n.strip():
                print("已经下载，忽略该链接")
                a = 1
                break
            
        if a == 1:
            continue
        
        fo.close()
        
        for k in range(int(get_image_page(n))):
            if k != 0:
                temp_url = n.replace(".html", "_" + str(k+1) + ".html");

            res = requests.get(temp_url, headers=headers, verify =False).text
            res = etree.HTML(res)
            data = res.xpath('/html/body/div[1]/div[5]/div/div[1]/div[3]/p/img/@src')
            if k == 0:
                title = res.xpath('/html/body/div[1]/div[5]/div/div[1]/h1/text()')[0].encode('ISO-8859-1').decode('UTF-8')
                title = re.sub('[\/:*?"<>|]','',title)
            for j in range(len(data)):
                image_list.append(str(data[j]))

        print(title)
        download_image(title, image_list, n)


def download_image(title, image_list, n):#下载图片
    path = './%s/' % title
    if not os.path.exists(path):  # 判断如果文件不存在,则创建
        os.makedirs(path)
        print("目录创建成功")
    else:
        print("目录已经存在")
    print('开始下载！！！')
    for i in range(len(image_list)):
        jpg_url = image_list[i]
        print(jpg_url)
        try:
            res = requests.get(jpg_url, verify =False).content
        except BaseException:
            continue
        with open('%s/%s.jpg' % (title, i), 'wb') as fp:
            fp.write(res)
            print('第' + str(i) + '张图片下载完成！')
            #time.sleep(2)
            
    url_txt = open('url.txt', 'a')
    url_txt.write(str(n))
    url_txt.write('\n')
    url_txt.close()
    

if __name__ == '__main__':
    print('准备开始工作了。。。')
    url = "https://www.tuli.cc"
    print('开始获取套图链接。。。')
    try:
        urls = get_index_path(url)
        for i in urls:
            page = get_page(i)
            
            url_list = get_page_url(i, page)

            get_image_url(url_list)
    except BaseException:
        urls = get_index_path(url)
        for i in urls:
            page = get_page(i)
            
            url_list = get_page_url(i, page)

            get_image_url(url_list)

