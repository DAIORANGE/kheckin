import requests
import json
import os

requests.packages.urllib3.disable_warnings()

# 用于发送通知的变量
SCKEY = os.environ.get('SCKEY')
TG_BOT_TOKEN = os.environ.get('TGBOT')
TG_USER_ID = os.environ.get('TGUSERID')

def checkin(email, password, base_url):
    email = email.split('@')
    email = email[0] + '%40' + email[1]
    session = requests.session()
    session.get(base_url, verify=False)
    login_url = base_url + '/auth/login'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/56.0.2924.87 Safari/537.36',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    }
    post_data = 'email=' + email + '&passwd=' + password + '&code='
    post_data = post_data.encode()
    response = session.post(login_url, post_data, headers=headers, verify=False)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/56.0.2924.87 Safari/537.36',
        'Referer': base_url + '/user'
    }
    response = session.post(base_url + '/user/checkin', headers=headers, verify=False)
    response = json.loads(response.text)
    print(response['msg'])
    return response['msg']

# 签到多个网站
sites = {
    'BASE_URL': ('EMAIL', 'PASSWORD'),
    'BASE_URL1': ('EMAIL1', 'PASSWORD1'),
    'BASE_URL2': ('EMAIL2', 'PASSWORD2'),
    # 可以继续添加更多的网站
}

for base_url, credentials in sites.items():
    email, password = credentials
    result = checkin(email, password, base_url)
    if SCKEY != '':
        sendurl = f'https://sctapi.ftqq.com/{SCKEY}.send?title=机场签到&desp={result}'
        requests.get(url=sendurl)
    if TG_USER_ID != '':
        sendurl = f'https://api.telegram.org/bot{TG_BOT_TOKEN}/sendMessage?chat_id={TG_USER_ID}&text={result}&disable_web_page_preview=True'
        requests.get(url=sendurl)
