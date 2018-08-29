# -*- coding: utf-8 -*-

import requests
try:
    import cookielib
except:
    import http.cookiejar as cookielib
import re
import base64

agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0"
header = {
    "HOST": "www.zhihu.com",
    "Referer": "https://www.zhihu.com",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36"
}
session = requests.session()
session.cookies = cookielib.LWPCookieJar(filename='cookies.txt')


def get_xsrf():
    # 获取 xsrf code
    response = session.get("https://www.zhihu.com", headers=header)
    xsrf = re.compile('.*xsrf&quot;:&quot;(.*?)&quot;.*').findall(response.text)
    match_obj = xsrf
    if match_obj:
        return match_obj[0]
    else:
        print("No")
        return None


def get_captcha():
    import base64
    import json
    captcha_text = session.put("https://www.zhihu.com/api/v3/oauth/captcha?", data={"lang":"en"}, headers=header)
    print(captcha_text)
    #show_captcha = json.loads(captcha_text.text)['show_captcha']
    if captcha_text:
        captcha_img = re.compile('.*src="data:image/jpg;base64,(.*)".*').findall(captcha_text.text)
        print(captcha_img)
        with open('captcha.jpg', 'wb') as f:
            #f.write(captcha_img)
            f.close()
        try:
            im = Image.open('captcha.jpg')
            im.show()
            im.close()
        except:
            print(u'请到 %s 目录找到captcha.jpg 手动输入' % os.path.abspath('captcha.jpg'))
        captcha = input("please input the captcha\n>")
    else:
        print("None")
        captcha = ''

    return captcha

def zhihu_login(account, password):
    # 知乎登录
    if re.match("^1\d{10}", account):
        print("手机号码登录")
        post_url = 'https://www.zhihu.com/api/v3/oauth/sign_in'
        post_data = {
            "_xsrf": get_xsrf(),
            "username": account,
            "password": password,
            "client_id": "c3cef7c66a1843f8b3a9e6a1e3160e20",
            "grant_type": "password",
            "timestamp": "1516001567637",
            "source": "com.zhihu.web",
            "signature": "ce5a775d8b8e09a0e22a31e9c21d33072f251736",
            "captcha": get_captcha(),
            "ref_source": "homepage",
            "utm_source": "",
            "lang": "en",
            }
        response_text = session.post(post_url, data=post_data, headers=header)
        session.cookies.save()

get_captcha()
zhihu_login("18912015081", "zhiperfect26")
