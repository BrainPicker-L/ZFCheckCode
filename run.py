from ZFCheckCode import recognizer
import requests

def identify():
    code = recognizer.recognize_checkcode('./checkcode.png')
    print(code)

def getCheckCode():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'
    }
    s = requests.session()
    r = s.get(url="http://jw2.ahu.cn/CheckCode.aspx",headers=headers)

    with open('checkcode.png', 'wb') as f:
        f.write(r.content)
    f.close()
    identify()

if __name__ == '__main__':
    getCheckCode()