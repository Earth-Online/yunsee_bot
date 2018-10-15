from requests import get, post, RequestException
import time
import json
from bs4 import BeautifulSoup

domain = 'http://www.yunsee.cn'

headers = {
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Connection': 'keep-alive',
    'Host': 'www.yunsee.cn',
    'Referer': 'http://www.yunsee.cn/',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest'
}

class QueryException(Exception):
    pass


def start_requests():
    url = '{}/geetest?t={}'.format(domain, int(time.time()) * 1000)
    return get(url=url, headers=headers)


def parse_token(response):
    result = json.loads(response.text)
    gt = result['gt']
    challenge = result['challenge']
    url = 'http://www.yunsee.cn/finger.html'
    return get(url=url, headers=headers, data={'gt': gt, 'challenge': challenge})


# search_host = "python.org"


def request_query(response, search_host):
    soup = BeautifulSoup(response.text, 'lxml')
    token = soup.find('meta', {'name': 'csrf-token'})
    if token:
        headers.update({'X-CSRF-TOKEN': token['content']})
        url = 'http://www.yunsee.cn/finger.html'
        form = {
            'string': search_host,
            'http': '2',
            'level': '2',
            'code': 'd879af' + str((len(search_host) - 1) * (len(search_host) + 1) * 3) + 'g54df45',
        }
        return post(url=url, data=form, headers=headers)

    raise Exception("not find csrf token")


def parse_info(response):
    info = json.loads(response.text)
    if info["code"] != 2:
        raise QueryException("query error error info {}".format(info["mess"]))
    return info["res"]


def query(url):
    try:
        challenge = start_requests()
        token = parse_token(challenge)
        ret = request_query(token, url)
        return parse_info(ret)
    except RequestException as e:
        print("request error")
        print("error info")
        print(e)
        return None
