# -*-coding:utf-8-*-
import os
import re
from lxml import etree
import requests
import sys
import imp
from ZFCheckCode import recognizer
imp.reload(sys)


#评教
def identify():
    code = recognizer.recognize_checkcode('./code.png')
    print(code)
    return code
# 匹配正确评教链接
def myfilter(L):
    if (L.find('xsjxpj.aspx')):
        return False
    else:
        return True


def getInfor(response, xpath):
    content = response.content.decode('gb2312')  # 网页源码是gb2312要先解码
    selector = etree.HTML(content)
    infor = selector.xpath(xpath)
    return infor


# 评教并保存
def doEvaluate(response, index, head):
    print('正在评价' + li_kc_name[index] + '...')
    response = s.post('http://jw2.ahu.cn/' + li[index], data=None, headers=head)
    __VIEWSTATE = getInfor(response, '//*[@name="__VIEWSTATE"]/@value')
    __VIEWSTATEGENERATOR = getInfor(response, '//*[@name="__VIEWSTATEGENERATOR"]/@value')
    post_data = {
        '__EVENTTARGET': '',
        '__EVENTARGUMENT': '',
        '__VIEWSTATE': __VIEWSTATE,
        '__VIEWSTATEGENERATOR': __VIEWSTATEGENERATOR,
        'pjkc': xh[index][:-4],
        'pjxx': '',
        'txt1': '',
        'TextBox1': '0',
        'Button1': u'保  存'.encode('gb2312')
    }
    print(post_data['pjkc'])
    for i in range(2, 9):
        if i == 2:
            post_data.update({'DataGrid1:_ctl' + str(i) + ':JS1': u'良好'.encode('gb2312')})
        else:
            post_data.update({'DataGrid1:_ctl' + str(i) + ':JS1': u'优秀'.encode('gb2312')})
            post_data.update({'DataGrid1:_ctl' + str(i) + ':txtjs1': ''})
    response = s.post('http://jw2.ahu.cn/' + li[index], data=post_data, headers=head)



studentnumber = input('学号：')
password = input('密码：')
index = 0
s = requests.session()
url = "http://jw2.ahu.cn/default2.aspx"
userAgent = "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.110 Safari/537.36"
response = s.get(url)
# 使用xpath获取__VIEWSTATE，__VIEWSTATEGENERATOR
selector = etree.HTML(response.content)
__VIEWSTATE = selector.xpath('//*[@id="form1"]/input/@value')[0]
__VIEWSTATEGENERATOR = selector.xpath('//*[@id="form1"]/input/@value')[1]
# 获取验证码并下载到本地
imgUrl = "http://jw2.ahu.cn/CheckCode.aspx"
imgresponse = s.get(imgUrl, stream=True)
image = imgresponse.content
DstDir = os.getcwd() + "\\"

try:
    with open("./code.png", "wb") as jpg:
        jpg.write(image)
except IOError:
    print("IO Error\n")

# 手动输入验证码
code = identify()
# 构建post数据
RadioButtonList1 = u"学生".encode('gb2312', 'replace')
data = {
    "RadioButtonList1": RadioButtonList1,
    "__VIEWSTATE": __VIEWSTATE,
    "__VIEWSTATEGENERATOR": __VIEWSTATEGENERATOR,
    "txtUserName": studentnumber,
    "TextBox2": password,
    "txtSecretCode": code,
    "Button1": "",
    "lbLanguage": ""
}
headers = {
    "User-Agent": userAgent
}
# 登陆教务系统
response = s.post(url, data=data, headers=headers)
# 获取学生基本信息
try:
    text = getInfor(response, '//*[@id="xhxm"]/text()')[0]
except IndexError:
    print('验证码或密码错误！请重试')
    x = input('按任意键退出...')
if (text != None):
    studentname = text
    print('成功进入教务系统！')
    print(studentname)
# 获取评教链接及课程名
li = getInfor(response, '//*[@class="sub"]/li/a/@href')
li = li[4:]
li_kc_name = getInfor(response, '//*[@class="sub"]/li/a/text()')
li_kc_name = li_kc_name[4:]
li = list(filter(myfilter, li))
li_kc_name = li_kc_name[:len(li)]
xh = []
for i in range(len(li)):
    xh.append(li[i][17:50])
head = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.8',
    'Connection': 'keep - alive',
    'Host': 'jw2.ahu.cn',
    'Referer': 'http://jw2.ahu.cn/xs_main.aspx?xh=' + studentnumber,
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': userAgent
}
try:
    response = s.post('http://jw2.ahu.cn/' + li[0], data=None, headers=head)
except IndexError:
    print('已完成评教！无需评教')
    x = input('按任意键退出...')
# 根据课程数量进行评教并保存
for i in range(len(li)):
    doEvaluate(response, index, head)
    index = index + 1
# 提交
response = s.post('http://jw2.ahu.cn/' + li[index - 1], data=None, headers=head)
__VIEWSTATE = getInfor(response, '//*[@name="__VIEWSTATE"]/@value')
__VIEWSTATEGENERATOR = getInfor(response, '//*[@name="__VIEWSTATEGENERATOR"]/@value')
post_data = {
    '__EVENTTARGET': '',
    '__EVENTARGUMENT': '',
    '__VIEWSTATE': __VIEWSTATE,
    '__VIEWSTATEGENERATOR': __VIEWSTATEGENERATOR,
    'pjkc': xh[index - 1],
    'pjxx': '',
    'txt1': '',
    'TextBox1': '0',
    'Button2': u'提  交'.encode('gb2312')
}
response = s.post('http://jw2.ahu.cn/' + li[index - 1], data=post_data, headers=head)
print('评教完成！请登陆教务系统查看结果！')
print('        *********************感谢使用*********************')