import requests, os
import warnings 
warnings.filterwarnings("ignore")
from lxml import etree
import urllib
from urllib.request import urlopen
import re, time
 
def geturl(classification):
    global list
    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 8.0; Pixel 2 Build/OPD3.170816.012) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Mobile Safari/537.36 Edg/84.0.522.52'
    }
    
    req = urllib.request.Request("https://ligui.org/" + classification, headers=headers)
    print('1、正在打开网址...' + "https://ligui.org/" + classification)
    website = urlopen(req,timeout=120)
    html = website.read().decode('utf8')
    website.close()
    print('2、正在查找符合条件的图片网址...')
    links = re.findall(r'/' + classification + '/.*?.html',html)
    #links = sorted(set(links),key=links.index)
    list = []
    print('3、开始准备图片网址列表内容。。。')
    for link in links:
        aurl = 'https://ligui.org' + link
        list.append(aurl)


    res = requests.get("https://ligui.org/" + classification, headers=headers, verify =False).text
    res = etree.HTML(res)
    page = re.findall(r"\d+?\d*", str(res.xpath('/html/body/div[1]/div[8]/div[3]/ul/li[8]/a/@href')))[1]

    if classification == 'beautyleg':
        num = "1"
    elif classification == 'iess':
        num = "2"
    elif classification == 'ligui':
        num = "3"
    elif classification == 'simu':
        num = "5"

    i = 2
    while i < int(page)+1:
        res = requests.get(url="https://ligui.org/" + classification + "/" + num + "_" + str(i) + ".html", headers=headers, verify =False).text
        res = etree.HTML(res)
        data = res.xpath('/html/body/div[1]/div[8]/div[1]/div/a/@href')
        for j in range(len(data)):
            list.append('https://ligui.org' + str(data[j]))
        i += 1
        
    list = sorted(set(list),key=list.index)
    print('列表内容准备完毕，下面开始下载图片。。。')
    return list
        

 
def downimg(imgurl):
    newcount = len(list)
    h = 1
    while h < newcount:
        a = 0
        url = list[h]
        print(url)
        fo = open("url.txt", "r")
        for url_list in fo.readlines():
            if url_list.strip() == url.strip():
                print("已经下载，忽略该链接")
                h += 1
                a = 1
                break
            
        if a == 1:
            continue
        
        fo.close()
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Linux; Android 8.0; Pixel 2 Build/OPD3.170816.012) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Mobile Safari/537.36 Edg/84.0.522.52'
        }
        list1 = []
        res = requests.get(url, headers=headers, verify =False, stream=True).text
        res = etree.HTML(res)
        try:
            title = res.xpath('/html/body/div[1]/div[5]/div/div[1]/h1/text()')[0].encode('ISO-8859-1').decode('UTF-8')
            title = re.sub('[\/:*?"<>|]','',title)
        except BaseException:
            h += 1
            error_url_txt = open('error_url.txt', 'a')
            error_url_txt.write(str(url))
            error_url_txt.write('\n')
            error_url_txt.close()
            continue
        page = re.findall(r"\d+\.?\d*", str(res.xpath('/html/body/div[1]/div[5]/div/div[1]/div[3]/div[4]/ul/li[1]/a/text()')[0]))
        data = res.xpath('/html/body/div[1]/div[5]/div/div[1]/div[3]/div[1]/a/img/@src')
        for j in range(len(data)):
            list1.append(data[j])
 
        i = 2
        while i < int(page[0])+1:
            urls = url.replace(".html", "_" + str(i) + ".html");
            res = requests.get(url=urls, headers=headers, verify =False, stream=True).text
            res = etree.HTML(res)
            data = res.xpath('/html/body/div[1]/div[5]/div/div[1]/div[3]/div[1]/a/img/@src')
            for j in range(len(data)):
                list1.append(data[j])
            i += 1
 
        path = './%s/' % title
        if not os.path.exists(path):  # 判断如果文件不存在,则创建
            os.makedirs(path)
            print("目录创建成功")
        else:
            print("目录已经存在")
        print('开始下载！！！')
        for i in range(len(list1)):
            jpg_url = list1[i]
            print(jpg_url)
            try:
                res = requests.get(jpg_url, verify =False, stream=True).content
            except BaseException:
                continue
            with open('%s/%s.jpg' % (title, i), 'wb') as fp:
                fp.write(res)
                print('第' + str(i) + '张图片下载完成！')
                #time.sleep(2)
        print('第' + str(h) + '个图片网址下载完成！！！')
        url_txt = open('url.txt', 'a')
        url_txt.write(str(url))
        url_txt.write('\n')
        url_txt.close()
        h += 1

if __name__ == '__main__':
    print('准备开始工作了。。。')
    classification = ['beautyleg', 'iess', 'ligui', 'simu']
    
    for i in range(len(classification)):
        geturl(classification[i])
        downimg(list)
