from yplib.index import *
from bs4 import BeautifulSoup
import requests


# from requests.packages.urllib3.exceptions import InsecureRequestWarning


# 有关 http 的工具类

# 解析 html 中的数据
# file_path :   html 文件的路径
# html_data :   html 数据
# selector  :   选择器
def do_parser(file_path=None, html_data='', selector=None):
    if file_path is not None:
        html_str = ''.join(to_list(file_path))
    else:
        if isinstance(html_data, list):
            html_str = ''.join(html_data)
        else:
            html_str = str(html_data)
    return BeautifulSoup(html_str, 'html.parser').select(selector)


# div_list_content = do_parser(r'D:\notepad_file\202306\asfdf.html', selector='table.reference')[4].select('tr')
#
# for i in range(len(div_list_content) - 1):
#     td = div_list_content[i + 1].select('td')
#     num = td[0].text
#     fun_name = td[1].select('a')[0].text
#     fun_desc = td[1].text.replace(fun_name, '')
#     print(f'{num} : {fun_name} , {fun_desc}')


# get 类型的请求
# session : session , 默认 : requests.session()
# headers : headers
# cookie  : cookie
# auth    : auth
# verify  : verify
# r_json : 返回的数据是否是一个 json 类型的数据
def do_get(url=None,
           session=None,
           headers=None,
           cookie=None,
           auth=None,
           timeout=10,
           verify=False,
           r_json=False):
    if session is None:
        session = requests.session()
    requests.packages.urllib3.disable_warnings()
    response = session.get(url=url, headers=headers, auth=auth, timeout=timeout, verify=verify, cookies=cookie)
    response.encoding = 'utf-8'
    return json.loads(response.text.strip()) if r_json else response.text.strip()


# print(do_get('https://www.runoob.com/?s=sorted'))
# print(do_get('http://10.6.180.156:18000/login/need'))
# print(do_get('http://10.6.180.156:18000/login/need', r_json=True))


# get 类型的请求
# data         : data post 体中的数据
# is_form_data : 是否是 form 表单
# headers : headers
# cookie  : cookie
# auth    : auth
# verify  : verify
# r_json : 返回的数据是否是一个 json 类型的数据
def do_post(url=None,
            data=None,
            is_form_data=False,
            session=None,
            headers=None,
            cookie=None,
            auth=None,
            timeout=10,
            verify=False,
            r_json=False):
    # headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    # data = {}
    # data['appkey'] = APP_KEY
    # data['secretkey'] = SECRET_KEY
    # data['content'] = content
    # data['phone'] = obtainMobileIndonesia(mobile)
    # requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
    # response = requests.post(URL, headers=headers, verify=False, data=data)
    # response.encoding = 'utf-8'
    # text = response.text
    # text = text.replace('\n', '')
    # text = text.replace('\r', '')
    # return text
    if session is None:
        session = requests.session()
    requests.packages.urllib3.disable_warnings()
    d = data if is_form_data else json.dumps(data)
    response = session.post(url=url, data=d, headers=headers, auth=auth, timeout=timeout, verify=verify, cookies=cookie)
    response.encoding = 'utf-8'
    return json.loads(response.text.strip()) if r_json else response.text.strip()
