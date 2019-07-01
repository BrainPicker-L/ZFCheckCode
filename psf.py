from ZFCheckCode import recognizer
import requests
import re
from lxml import etree
from urllib import parse
import base64

USER = input('username:')
PASSWORD = input('password:')
def identify():
    code = recognizer.recognize_checkcode('./checkcode.png')
    print(code)
    return code
def getCheckCode(s):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'
    }

    r = s.get(url="http://jw2.ahu.cn/CheckCode.aspx",headers=headers)
    with open('checkcode.png', 'wb') as f:
        f.write(r.content)
    f.close()
    return identify()

def login(s):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'
    }
    r1_html = s.get(url="http://jw2.ahu.cn/default2.aspx", headers=headers).content.decode('gb2312')
    data = {
        '__VIEWSTATE' : re.findall(r'name="__VIEWSTATE" value="(.*?)" />',r1_html)[0],
        '__VIEWSTATEGENERATOR':re.findall(r'name="__VIEWSTATEGENERATOR" value="(.*?)" />',r1_html)[0],
        'txtUserName': USER,
        'Textbox1':'',
        'TextBox2': PASSWORD,
        'txtSecretCode': getCheckCode(s),
        "Button1": "",

    }

    r2 = s.post(url="http://jw2.ahu.cn/default2.aspx",headers=headers,data=data)
    name_chs = re.findall(r'<span id="xhxm">(.*?)同学',r2.content.decode('gb2312'))[0]
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',
        'Referer': 'http://jw2.ahu.cn/xs_main.aspx?xh=%s'%USER,
    }
    r3 = s.get(url="http://jw2.ahu.cn/xscjcx.aspx?xh={xh}&xm={xm}&gnmkdm=N121605".format(xh=USER,xm=name_chs),headers=headers)
    data = {
        '__EVENTTARGET': '',
        '__EVENTARGUMENT': '',
        '__VIEWSTATE' : re.findall(r'name="__VIEWSTATE" value="(.*?)" />', r3.content.decode('gb2312'))[0],
        'hidLanguage':'',
        'ddlXN': '2018-2019',
        'ddlXQ': '1',
        'ddl_kcxz': '',
        'btn_zcj':'%C0%FA%C4%EA%B3%C9%BC%A8',
    }
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',
        'Referer': "http://jw2.ahu.cn/xscjcx.aspx?xh={xh}&xm={xm}&gnmkdm=N121605".format(xh=USER,xm=name_chs),
    }
    r4 = s.post(url="http://jw2.ahu.cn/xscjcx.aspx?xh={xh}&xm={xm}&gnmkdm=N121605".format(xh=USER,xm=name_chs),headers=headers,data=data).content.decode('gb2312')
    __VIEWSTATE = re.findall(r'name="__VIEWSTATE" value="(.*?)" />', r4)[0]
    dirty_data = re.sub('i<\d*>','',base64.b64decode(__VIEWSTATE).decode("utf8","ignore"))
    data = re.sub('.*DISPLAY:block','',dirty_data)
    data = re.sub(r'[;><]','',data)
    b = data.replace('\\',"").replace('tpplText', '').replace('&nbsp', '').replace(' ', '').replace('	', '').replace('pplText','').replace('ll','l').replace('ll', 'l').replace('ll', 'l')
    c = b.split('-20')[1:]
    name = re.findall(r'-\d\d\d\dtpplTextl\d+tpplTextl.*?tpplTextl(.*?)tpplTextl', data)
    for i in range(len(c)):
        d = re.findall(r'l.*?l\d\.\d\dl(.*?)l(.*?)l(.*?)(l.*?)?l0l', c[i])
        if d == []:
            daily_score = test_score = final_score = re.findall(r'l(\d+)l0l', c[i])[0]
        else:
            daily_score, test_score, final_score, extra = d[0]

        print(name[i], daily_score, test_score, final_score)

if __name__ == '__main__':
    s = requests.session()
    login(s)