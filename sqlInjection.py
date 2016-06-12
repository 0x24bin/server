from urllib.parse import urlparse 
dic = {}
class attack_url():
    def __init__(self,www_path,param):
        self.www_path = www_path.lower()
        self.param = param #参数
    def __hash__(self):
        return hash(self.www_path)
def my_format(netloc,urlList):
    #print('正在检测',url)
    return_list = []
    dic = {}
    for i in urlList:
        url_seq = urlparse(i)
        str = [tuple(sorted(i.split('=')[0] for i in url_seq[4].split('&')))] #排好序的参数
        path = url_seq[1]+url_seq[2] #路径 应该取的路径:参数对
        if path in dic:
            for i in str:
                if i not in dic[path]:#应该取参数最多的那个
                    if len(str) > len(dic[path][1]):
                        dic[path].update = [str,i]
        else:
            dic[path] = [str,i]
        for i in dic:
            return_list.append(i+'/'+dic[i][1])
    return return_list
if __name__=='__main__':
    from bs4 import BeautifulSoup
    import requests    
    lis = []
    import pymongo
    client = pymongo.MongoClient('nofiht.ml')
    db = client.edu_cn
    for things in db.text.find().limit(10):
        resp = things['text']
        soup = BeautifulSoup(resp,'lxml')
        for i in soup.findAll(href=True):
            if '=' in i['href']:
                lis.append(i['href'])
        for i in my_format('www.sdu.edu.cn',lis):
            print(things['url'],'---->',i)