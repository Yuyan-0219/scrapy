#傳入圖片文章連結網址與文章標題
def  _savepic(picurl,pictitle):     
    rqpic=requests.get(picurl,cookies=mycookies).text   #模擬送出cookies的驗證值
    bppic=BeautifulSoup(rqpic,'html5lib') 
    try:
        os.makedirs(pictitle)      #以文章標題為名稱建立一個子目錄用來存放文章內的圖片
    except FileExistsError:        #若目錄已存在則顯示目錄已經存在的訊息 
        print('目錄已經存在!!!')
       
    print('---------------------------------------------')    
    for pic in bppic.find(id='main-content').find_all('a'):
        try:             
            fullpath=pic['href']     #因為imgur網址不同所以我們先處理成相同網址結構https://i.imgur.com/xxxxxx.jpg
            if fullpath.split('//')[1].startswith('m.'):         #把m.改成i.
                fullpath=fullpath.replace('//m.','//i.')          
            if not fullpath.endswith('.jpg'):                    #把沒有.jpg的加上.jpg
                fullpath=fullpath+'.jpg'
            print(fullpath)    
            picname=fullpath.split('/')[-1]
            if os.path.isfile(pictitle+'\\'+picname):  #判斷圖片檔案是否已經存在，若不存在才做存檔的動作
                print('檔案已經存在!!!')
            else:
                urllib.request.urlretrieve(fullpath,pictitle+'\\'+picname)       #圖片存檔
        except:
            continue



#傳入的網址存放在url
def _beauty():           
    global time          #全域變數
    rq=requests.get(url,cookies=mycookies).text  #模擬送出cookies的驗證值
    bp=BeautifulSoup(rq,'html5lib')
    bbs=bp.find('div','r-list-container action-bar-margin bbs-screen')

    for i in bbs.find_all('div','r-ent'):                
        if i.find('div','date').text != d4:   #判斷文章日期是否不是今日
            time=time-1   #不是的話就把[timeS]減一
            if time==0:        #[time]為零時，傳回[None]
                return None
        else: 
            try:
                print('=='*30)
                print('日期: ',i.find('div','date').text)
                print(i.find('div','title').text.strip())
                print('https://www.ptt.cc'+i.find('div','title').a['href'])
                print('作者: ',i.find('div','author').text)
                theurl='https://www.ptt.cc'+i.find('div','title').a['href']
                tit=i.find('div','title').text.strip()
                _savepic(theurl,tit)     #自訂函式，用來圖片存檔
            except:
                continue    
            
    nexturl='https://www.ptt.cc/'+i.find('div','btn-group btn-group-paging').find_all('a')[1]['href']
    return nexturl



import requests
from bs4 import BeautifulSoup
import datetime   #載入[datetime]模組，協助處理日期問題
import os         #建立新資料夾與其他目錄相關的處理
import urllib     #存檔用

mycookies={'over18':'1'}
url='https://www.ptt.cc/bbs/Beauty/index.html'   #PTT Beauty板


#時間問題
time=10

d1=datetime.datetime.today()
d2=str(d1).split(' ')[0]       
d3=d2.split('-')[1:]            #d3是一個串列

if int(d3[0]) < 10:         #月份若為單位數，前面會有一個空格
    d4=' '+str(int(d3[0]))+'/'+d3[1]
else:   
    d4=d3[0]+'/'+d3[1]


#先判斷目錄是否存在，若不存在才建立新目錄
try:    
    os.makedirs(str(d2))    
except FileExistsError:    
    print('目錄已經存在!!!')

newdir=str(d2)+'/'
os.chdir(newdir)    #切換到新建的目錄底下


#使用迴圈來處理下一頁資料的問題，只要url不為空值就繼續抓下一頁的資料
while url: 
    nexturl=_beauty()   #_beauty()是自訂函式，用來處理網頁資料抓取


print('')
print('**'*10)    
print('今天是: ',d1)
print('圖片存放的目錄在: ',os.getcwd())     #顯示當前的目錄路徑
print('======================================')
print(os.listdir())     #顯示出此目錄下的所有子目錄名稱
print('**'*10)  
