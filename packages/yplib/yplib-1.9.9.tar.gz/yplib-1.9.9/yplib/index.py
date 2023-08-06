import hashlib
import json
import os
import random
import re
import time
import uuid
from datetime import datetime
from datetime import timedelta

import xlrd
import xlwt


# 记录日志, 如果是对象会转化为 json
def to_log(a1='tag', a2='', a3='', a4='', a5='', a6='', a7='', a8='', a9='', a10='', a11='', a12='',
           a13='', a14='', a15='', a16='', a17='', a18='', a19='', a20=''):
    l = [a1, a2, a3, a4, a5, a6, a7, a8, a9, a10,
         a11, a12, a13, a14, a15, a16, a17, a18, a19, a20]
    d = ''
    for one in l:
        if can_use_json(one):
            o = json.dumps(one)
        else:
            o = str(one)
        if o != '':
            d = d + ' ' + o
    lo = datetime.today().strftime('%Y-%m-%d %H:%M:%S') + d
    print(lo)
    return lo


# 将 log 数据, 写入到文件
def to_log_file(a1='tag', a2='', a3='', a4='', a5='', a6='', a7='', a8='', a9='', a10='', a11='', a12='',
                a13='', a14='', a15='', a16='', a17='', a18='', a19='', a20=''):
    lo = to_log(a1, a2, a3, a4, a5, a6, a7, a8, a9, a10, a11, a12, a13, a14, a15, a16, a17, a18, a19, a20)
    to_txt([lo], datetime.today().strftime('%Y-%m-%d'), 'log', True, '.log')


# 将 log 数据, 写入到固定文件中
def to_log_txt(file_name, a1='tag', a2='', a3='', a4='', a5='', a6='', a7='', a8='', a9='', a10='', a11='', a12='',
               a13='', a14='', a15='', a16='', a17='', a18='', a19='', a20=''):
    lo = to_log(a1, a2, a3, a4, a5, a6, a7, a8, a9, a10, a11, a12, a13, a14, a15, a16, a17, a18, a19, a20)
    to_txt([lo], file_name, 'log', True, '.txt')


# 将下划线命名转成驼峰命名
# 例如 : user_id -> userId
# 例如 : USER_ID -> userId
def to_hump(s=''):
    if s == '' or s is None:
        return s
    s = s.lower()
    s1 = s.split('_')
    r = ""
    for w in s1:
        r += w.capitalize()
    return r[0].lower() + r[1:]


def to_hump_more(a1='', a2='', a3='', a4='', a5=''):
    if a1 == '':
        return a1
    elif a2 == '':
        return to_hump(a1)
    elif a3 == '':
        return to_hump(a1), to_hump(a2)
    elif a4 == '':
        return to_hump(a1), to_hump(a2), to_hump(a3)
    elif a5 == '':
        return to_hump(a1), to_hump(a2), to_hump(a3), to_hump(a4)
    return to_hump(a1), to_hump(a2), to_hump(a3), to_hump(a4), to_hump(a5)


# 将驼峰命名转成下划线命名
# 例如 : userId -> user_id
def to_underline(s=''):
    if s == '' or s is None:
        return s
    r = ''
    for c in s:
        if c.isupper():
            r += '_' + c.lower()
        else:
            r += c
    return r


def to_underline_more(a1='', a2='', a3='', a4='', a5=''):
    if a1 == '':
        return a1
    elif a2 == '':
        return to_underline(a1)
    elif a3 == '':
        return to_underline(a1), to_underline(a2)
    elif a4 == '':
        return to_underline(a1), to_underline(a2), to_underline(a3)
    elif a5 == '':
        return to_underline(a1), to_underline(a2), to_underline(a3), to_underline(a4)
    return to_underline(a1), to_underline(a2), to_underline(a3), to_underline(a4), to_underline(a5)


# 是否能用 json
def can_use_json(data):
    if isinstance(data, dict) or isinstance(data, list) or isinstance(data, tuple) or isinstance(data, set):
        return True
    return False


# 检查文件夹是否存在,不存在,就创建新的
def check_file(file_name):
    if file_name is None or file_name == '':
        return
    for sep in ['\\', '/']:
        f_n = file_name.split(sep)
        for i in range(1, len(f_n) + 1):
            # C:\Users\yangpu\Desktop\study\p.t
            p_n = sep.join(f_n[0:i])
            if not os.path.exists(p_n):
                os.mkdir(p_n)


# 获得文件名称
def get_file_name(file_name, suffix='.txt'):
    [day, hour, minute, second, ss] = datetime.today().strftime('%d_%H_%M_%S_%f').split('_')
    return str(file_name) \
        + '_' + day + hour + minute \
        + '_' + second + ss[0] + random_int_str(1) \
        + suffix


# 获得文件名称
def file_is_empty(file_name=None):
    return file_name is None or file_name == '' or not os.path.exists(file_name)


def do_md5(data='do_md5'):
    return hashlib.md5(data.encode(encoding='UTF-8')).hexdigest()


def do_sha256(data='do_sha256'):
    h = hashlib.sha256()
    h.update(data.encode('utf-8'))
    return h.hexdigest()


def random_uuid(length=32):
    r = uuid.uuid4().hex
    while len(r) < length:
        r += uuid.uuid4().hex
    return r[0:length]


# 获得随机数
# length ：随机数长度
# start_str ：随机数开始的字符的位置,从 1 开始
# 包含 : start_str
# end_str ：随机数结束的字符的位置
# 不包含 : end_str
def random_str(length=64, start_str=1, end_str=62):
    c_s = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_'
    r = ''
    start_str = max(1, start_str)
    end_str = min(len(c_s), end_str)
    while len(r) < length:
        r += c_s[random.Random().randint(start_str, end_str) - 1]
    return r


def random_letter(length=10, is_upper=False):
    r = random_str(length=length, end_str=26)
    return r.upper() if is_upper else r


def random_int(length=10):
    return int(random_int_str(length=length))


def random_int_str(length=10):
    return random_str(length=length, start_str=53, end_str=62)


# 去掉 str 中的 非数字字符, 然后, 再转化为 int
def to_int(s):
    if s is None or s == '':
        return 0
    if isinstance(s, float):
        return int(s)
    s = ''.join(filter(lambda ch: ch in '0123456789', str(s)))
    return 0 if s == '' else int(s)


# 去掉 str 中的 非数字字符, 然后, 再转化为 float
def to_float(s):
    if s is None or s == '':
        return 0.0
    s = ''.join(filter(lambda ch: ch in '0123456789.', str(s)))
    return 0.0 if s == '' else float(s)


def to_datetime(s=None, r_str=False):
    if s is None or s == '':
        return str(datetime.today()) if r_str else datetime.today()
    s = str(s)
    r = None
    m_s = {
        "^\\d{4}$": "%Y",
        "^\\d{4}-\\d{1,2}$": "%Y-%m",
        "^\\d{4}-\\d{1,2}-\\d{1,2}$": "%Y-%m-%d",
        "^\\d{4}-\\d{1,2}-\\d{1,2} {1}\\d{1,2}$": "%Y-%m-%d %H",
        "^\\d{4}-\\d{1,2}-\\d{1,2} {1}\\d{1,2}:\\d{1,2}$": "%Y-%m-%d %H:%M",
        "^\\d{4}-\\d{1,2}-\\d{1,2} {1}\\d{1,2}:\\d{1,2}:\\d{1,2}$": "%Y-%m-%d %H:%M:%S",
        "^\\d{4}-\\d{1,2}-\\d{1,2} {1}\\d{1,2}:\\d{1,2}:\\d{1,2}.\\d{1,9}$": "%Y-%m-%d %H:%M:%S",
    }
    for m in m_s:
        if re.match(m, s):
            r = datetime.strptime(s.split('.')[0], m_s[m])
    if r is None and re.match("^\\d{1,13}$", s):
        s_int = int(s)
        if len(s) > 10:
            s_int = int(s_int / 1000)
        time_arr = time.localtime(s_int)
        time_str = time.strftime("%Y-%m-%d %H:%M:%S", time_arr)
        r = datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S")
    if r is None:
        r = datetime.today()
    return str(r) if r_str else r


# 时间加几天
def to_datetime_add(s=None, days=0, seconds=0, microseconds=0, milliseconds=0, minutes=0, hours=0, weeks=0):
    return to_datetime(s) + timedelta(days=days, seconds=seconds, microseconds=microseconds,
                                      milliseconds=milliseconds, minutes=minutes, hours=hours,
                                      weeks=weeks)


def to_date(s=None):
    return str(to_datetime(s))[0:10]


def to_date_add(s=None, days=0, seconds=0, microseconds=0, milliseconds=0, minutes=0, hours=0, weeks=0):
    return str(to_datetime_add(s=s, days=days, seconds=seconds, microseconds=microseconds,
                               milliseconds=milliseconds, minutes=minutes, hours=hours, weeks=weeks))[0:10]


# 将 list 中的数据以 json 或者基本类型的形式写入到文件中
# data_list : 数组数据, 也可以不是数组
# file_name : 文件名 , 当文件名是 C:\Users\yangpu\Desktop\study\abc\d\e\f\a.txt 这种类型的时候, 可以直接创建文件夹,
# fixed_name : 是否固定文件名
# file_path : 文件路径
def to_txt(data_list, file_name='txt', file_path='txt', fixed_name=False, suffix='.txt'):
    file_name = str(file_name)
    for sep in ['\\', '/']:
        f_n = file_name.split(sep)
        if len(f_n) > 1:
            file_name = f_n[-1]
            file_path = sep.join(f_n[0:-1])
            if '.' in file_name:
                suffix = '.' + file_name.split('.')[-1]
                file_name = file_name[0:file_name.find('.')]
                fixed_name = True

    # 检查路径 file_path
    while file_path.endswith('/'):
        file_path = file_path[0:-1]
    check_file(file_path)
    # 生成 file_name
    if fixed_name:
        file_name = file_name + suffix
    else:
        file_name = get_file_name(file_name, suffix)
    # 文件路径
    file_name_path = file_name
    if file_path != '':
        file_name_path = file_path + '/' + file_name
    # 写入文件
    text_file = open(file_name_path, 'a', encoding='utf-8')
    if not isinstance(data_list, list):
        text_file.write(to_str(data_list) + '\n')
    else:
        for one in data_list:
            text_file.write(to_str(one) + '\n')
    text_file.close()
    return file_name_path


# 将 list 中的数据写入到固定的文件中,自己设置文件后缀
def to_txt_data(data_list, file_name='data'):
    return to_txt(data_list, file_name, 'data', True)


def to_str(data):
    if can_use_json(data):
        s = json.dumps(data)
    else:
        s = str(data)
    return s


# 根据json的key排序,用于签名
# 按照 key 排序, 按照 key=value 然后再 & 连接, 如果数据中有 list, 使用 , 连接 list 中的数据, 然后拼接成 str 返回
# sep : 分隔符 , 默认 &
# join      : 连接符 , 默认 =
# join_list : list 数据 连接符 , 默认 ,
def sort_by_json_key(data_obj, sep='&', join='=', join_list=','):
    if isinstance(data_obj, list) or isinstance(data_obj, tuple) or isinstance(data_obj, set):
        return join_list.join(list(map(lambda x: f'{x}', data_obj)))
    if not isinstance(data_obj, dict):
        return str(data_obj)
    data_list = sorted(data_obj.items(), key=lambda x: x[0])
    r_l = []
    for one in data_list:
        value_one = one[1]
        if can_use_json(value_one):
            s = sort_by_json_key(data_obj=value_one, sep=sep, join=join, join_list=join_list)
        else:
            s = str(value_one)
        r_l.append(f'{one[0]}{join}{s}')
    return sep.join(r_l)


# data = {}
# data['merchantId'] = "merchantId"
# data['currency'] = "IDR"
# data['accType'] = "payout"
# data['version'] = "1.0"
# data['b'] = {
#     'a': 1,
#     'c': 'c',
#     'b': 'po',
# }
# b = [2, 3, 8, 4, "yp"]
# data['c'] = b
# sign = sort_by_json_key(data)
# print(sign)


# 当读取 txt 之类的文件的时候
# 将 txt 文件读取到 list 中, 每一行自动过滤掉行前行后的特殊字符
# sep : 是否对每一行进行分割,如果存在这个字段,就分割
# sep_all : 将文件转化成一个字符串,然后对这个字符串,再次总体分割
# start_index : 从这个地方开始读取,从1开始标号 , 包含这一行
# start_line :  从这个地方开始读取,从第一行开始找到这个字符串开始标记 , 包含这一行
# end_index :   读取到这个地方结束,从1开始标号 , 不包含这一行
# end_line :    读取到这个地方结束,从第一行开始找到这个字符串开始标记 , 不包含这一行
# count :       读取指定的行数
################################################
# 当读取 excel 之类的文件的时候
# 将 excel 文件读取到 list 中, 可以指定 sheet, 也可以指定列 column_index(列) ,自动过滤掉每个单元格前后的特殊字符
# sheet : 从 1 开始编号,
# column_index : 从 1 开始编号, 指定列
# column_index : 如果是指定值, 这个时候返回的是一个 list, 没有嵌套 list
# column_index : 如果是 '1,2,3,4'   [1,2,3,4], 返回的是一个嵌套 list[list]
# column_date : 指定日期格式的列,规则与 column_index 一样
# column_datetime : 指定日期格式的列,规则与 column_index 一样
# 返回的数据一定是一个 list
def to_list(file_name='a.txt',
            sep=None,
            sep_all=None,
            start_index=None,
            start_line=None,
            end_index=None,
            end_line=None,
            count=None,
            sheet_index=1,
            column_index=None,
            column_date=None,
            column_datetime=None):
    if file_name.endswith('.xls') or file_name.endswith('.xlsx'):
        return to_list_from_excel(file_name=file_name,
                                  sheet_index=sheet_index,
                                  column_index=column_index,
                                  column_date=column_date,
                                  column_datetime=column_datetime)
    return to_list_from_txt(file_name=file_name,
                            sep=sep,
                            sep_all=sep_all,
                            start_index=start_index,
                            start_line=start_line,
                            end_index=end_index,
                            end_line=end_line,
                            count=count)


# 当读取 excel 之类的文件的时候
# 将 excel 文件读取到 list 中, 可以指定 sheet, 也可以指定列 column_index(列) ,自动过滤掉每个单元格前后的特殊字符
# sheet_index  : 从 1 开始编号,
# column_index : 从 1 开始编号, 指定列, 如果是指定值是一个, 这个时候返回的是一个 list, 没有嵌套 list
#                如果是 '1,2,3,4'   [1,2,3,4], 返回的是一个嵌套 list[list]
# column_date :  指定日期格式的列,规则与 column_index 一样
# column_datetime : 指定日期格式的列,规则与 column_index 一样
def to_list_from_excel(file_name='a.xls',
                       sheet_index=1,
                       column_index=None,
                       column_date=None,
                       column_datetime=None):
    if file_is_empty(file_name):
        return []
    data_list = list()
    # excel 表格解析成 list 数据
    list_index = []
    for one_index in [column_index, column_date, column_datetime]:
        list_index_one = None
        if one_index is not None:
            list_index_one = []
            if isinstance(one_index, int):
                list_index_one.append(one_index)
            if isinstance(one_index, str):
                i_list = one_index.split(',')
                for i in i_list:
                    list_index_one.append(int(i))
            if isinstance(one_index, list):
                for i in one_index:
                    list_index_one.append(int(i))
        list_index.append(list_index_one)
    list_all = []
    for one_list in list_index:
        if one_list is not None:
            for o in one_list:
                list_all.append(o)
    if len(list_all) > 0 and list_index[0] is not None:
        list_index[0] = list_all
    # 是否是单 list 类型的数据
    list_only_one = False
    if list_index[0] is not None and len(list_index[0]) == 1:
        list_only_one = True
    book = xlrd.open_workbook(file_name)  # 打开一个excel
    sheet = book.sheet_by_index(sheet_index - 1)  # 根据顺序获取sheet
    for i in range(sheet.nrows):  # 0 1 2 3 4 5
        rows = sheet.row_values(i)
        row_data = []
        for j in range(len(rows)):
            cell_data = str(rows[j]).strip()
            is_date = False
            is_datetime = False
            # 日期格式的列
            if list_index[1] is not None and j + 1 in list_index[1]:
                cell_data = to_date(xlrd.xldate_as_datetime(to_int(rows[j]), 0))
                is_date = True
                row_data.append(cell_data)
                if list_only_one:
                    row_data = cell_data
            # 日期时间格式的列
            if not is_date and list_index[2] is not None and j + 1 in list_index[2]:
                cell_data = to_datetime(xlrd.xldate_as_datetime(to_int(rows[j]), 0))
                is_datetime = True
                row_data.append(cell_data)
                if list_only_one:
                    row_data = cell_data
            # 指定需要的列
            if not is_date and not is_datetime:
                if list_index[0] is None:
                    row_data.append(cell_data)
                else:
                    # 指定需要的列
                    if j + 1 in list_index[0]:
                        row_data.append(cell_data)
                        if list_only_one:
                            row_data = cell_data
        data_list.append(row_data)
    return data_list


# 当读取 txt 之类的文件的时候
# 将 txt 文件读取到 list 中, 每一行自动过滤掉行前行后的特殊字符
# sep : 是否对每一行进行分割,如果存在这个字段,就分割
# sep_all : 将文件转化成一个字符串,然后对这个字符串,再次总体分割
# start_index : 从这个地方开始读取,从1开始标号 , 包含这一行
# start_line :  从这个地方开始读取,从第一行开始找到这个字符串开始标记 , 包含这一行
# end_index :   读取到这个地方结束,从1开始标号 , 不包含这一行
# end_line :    读取到这个地方结束,从第一行开始找到这个字符串开始标记 , 不包含这一行
# count :       读取指定的行数
def to_list_from_txt(file_name='a.txt',
                     sep=None,
                     sep_all=None,
                     start_index=None,
                     start_line=None,
                     end_index=None,
                     end_line=None,
                     count=None):
    if file_is_empty(file_name=file_name):
        return []
    data_list = list()
    # 普通文件的解析
    d_list = open(file_name, 'r', encoding='utf-8').readlines()
    c = 0
    start_flag = None
    end_flag = None
    if start_line is not None:
        start_flag = False
    if end_line is not None:
        end_flag = False
    for i in range(len(d_list)):
        line = d_list[i].strip()
        # 判断开始位置
        if start_index is not None and i + 1 < to_int(start_index):
            continue
        # 判断结束位置
        if end_index is not None and i + 1 >= to_int(end_index):
            continue
        # 判断数量
        if count is not None and c >= to_int(count):
            continue
        # 开始标记位
        if start_flag is not None and not start_flag and line.find(start_line) > -1:
            start_flag = True
        # 开始标记位
        if end_flag is not None and not end_flag and line.find(end_line) > -1:
            end_flag = True
        if start_flag is not None and not start_flag:
            continue
        elif end_flag is not None and end_flag:
            continue
        c += 1
        if sep is not None:
            data_list.append(line.split(str(sep)))
        else:
            data_list.append(line)
    if sep_all is not None:
        data_list = ''.join(data_list).split(str(sep_all))
    return data_list


# 在 to_list 方法上再嵌套一层,
# r_str : 返回的数据是否是一个 字符串, ''.join(list)
# r_json : 返回的数据是否是一个 json 类型的数据
def to_list_data(file_name='a.txt',
                 sep=None,
                 sep_all=None,
                 start_index=None,
                 start_line=None,
                 end_index=None,
                 end_line=None,
                 count=None,
                 sheet_index=1,
                 column_index=None,
                 column_date=None,
                 column_datetime=None,
                 r_json=False,
                 r_str=False):
    d = to_list(file_name=file_name,
                sep=sep,
                sep_all=sep_all,
                start_index=start_index,
                start_line=start_line,
                end_index=end_index,
                end_line=end_line,
                count=count,
                sheet_index=sheet_index,
                column_index=column_index,
                column_date=column_date,
                column_datetime=column_datetime)
    return ''.join(d) if r_str else json.loads(''.join(d)) if r_json else d


def to_excel(data_list, file_name, file_path='excel'):
    file_name = str(file_name)
    while file_path.endswith('/'):
        file_path = file_path[0:-1]
    check_file(file_path)
    # 2. 创建Excel工作薄
    w_b = xlwt.Workbook()
    # 3. 添加Excel工作表
    sh = w_b.add_sheet(str(file_name))
    # 4. 写入数据
    # myStyle = xlwt.easyxf('font: name Times New Roman, color-index red, bold on')  # 数据格式
    m = 0
    for one_data in data_list:
        n = 0
        if isinstance(one_data, list):
            for one in one_data:
                # mySheet.write(n, m, one)  # 写入A3，数值等于1
                if isinstance(one, dict) or isinstance(one, list):
                    s = json.dumps(one)
                else:
                    s = str(one)
                sh.write(m, n, s)  # 写入A3，数值等于1
                n += 1
        else:
            if can_use_json(one_data):
                s = json.dumps(one_data)
            else:
                s = str(one_data)
            sh.write(m, n, s)  # 写入A3，数值等于1
        m += 1
    # 5. 保存
    # myWorkbook.save('5002200.xls')
    w_b.save(file_path + '/' + get_file_name(file_name, '.xls'))

# print('start')
# to_txt([1, 2, 3], r'C:\Users\yangpu\Desktop\study\abc\d\e\f\a.txt')
# to_txt([1, 2, 3], r'C:\Users\yangpu\Desktop\study\abc\d\e\f')
# to_txt([1, 2, 3], r'C:\Users\yangpu\Desktop\study\p.t')
# to_txt([1, 2, 3], 'C:/Users/yangpu/Desktop/study/p.t')
# to_txt_file_name([1,2,3], 'p')
#
#
# li = to_list('D:\code\python3\packaging_tutorial\yplib\data\p_20230612_095450_34779.txt')
#
# to_log()
#
# to_log()
# to_log(1)
# to_log(1, 2)
# to_log(1, 2, [1, 2])
# to_log_file(1, 2, [{'a': 2}])
# to_log_txt('1.txt', 1, 2, [{'a': 2}])
# to_txt([{'a': 2}])
# to_txt_data('yangpu', 1)
# to_txt_data('yangpu1', 1)
# to_txt_data('yangpu12', 1)
#
# x_list = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
# y_list = json.loads(
#     '[{"name":"Email","data":[120,132,101,134,90,230,210]},{"name":"Union Ads","data":[220,182,191,234,290,330,310]},{"name":"Video Ads","data":[150,232,201,154,190,330,410]},{"name":"Direct","data":[320,332,301,334,390,330,320]},{"name":"Search Engine","data":[820,932,901,934,1290,1330,1320]}]')
#

# # 将 list 转化成 图表的例子
# x_list = []
# y_list = []
# # x 轴有 100 个
# # 100 个横坐标
# for i in range(100):
#     x_list.append(i)
#
# # 有 10 条线
# for i in range(10):  # 0 1 2 3 4 55
#     n = {}
#     n['name'] = str(int(random.uniform(0, 1000)))
#     data = []
#     # 每条线有 100 个纵坐标, 与 x_list 中的对应起来
#     for i in range(100):
#         data.append(int(random.uniform(0, 1000)))
#     n['data'] = data
#     y_list.append(n)
# #
# to_chart(x_list, y_list)
#
# to_txt_data(x_list, 'operate')
# to_txt_data(y_list, 'operate')

# to_log_file(1)
# log_to_file(12)
# log_to_file('yangpu')
# print(str_to_int('yan123gpu'))
# print(str_to_float('yan123gpu'))
# print(str_to_float('yan123g.12pu'))

#
# print(to_hump('user_id'))
# print(to_hump('USER_ID'))
# print(to_hump('userId'))
# print(to_hump('user'))
# print(to_hump(''))

# print(to_hump_more('userId'))

# print(to_underline('userId'))


# print(uuid_random(5))
# print(uuid_random(10))
# print(uuid_random())
# print(uuid_random(32))
# print(uuid_random(64))
# print(uuid_random(128))
# print(uuid_random(127))
# print(uuid_random(129))


# print(to_int('a'))
# print(to_int(2))
# print(to_int(2.2))
# print(to_int(2.2))

# print(to_float('a'))
# print(to_float(2))
# print(to_float(2.2))
# print(to_float(2.24))

# print(to_date('2019-09'))
# print(to_date('2019-09-08'))
# print(to_date('2019-09-08 12'))
# print(to_date('2019-09-08 12:13'))
# print(to_datetime('2019-09-08 12:13:14'))
# print(to_datetime('2019-09-08 12:13:14.789'))
# print(to_datetime(1686537485))
# print(to_datetime(1686537484467))
# print(to_datetime(datetime.today()))
#
# print(do_md5())
# print(do_md5())
# print(do_md5('yangpu'))
# print(do_md5('yangpu12'))
#
# log_msg = ''
# headers = {'Content-Type': 'application/json;charset=utf-8'}
# data = {}
# data['merchantId'] = "merchantId"
# data['currency'] = "IDR"
# data['accType'] = "payout"
# data['version'] = "1.0"
# sign = sort_by_json_key(data)
# print(sign)
# hash = hashlib.sha256()
# hash.update(sign.encode('utf-8'))
# data['sign'] = hash.hexdigest()
#
# print(data)


# print(get_file_data_line(r'D:\notepad_file\202306\fasdfsadfaf.txt', 'payout', from_last=False))

# get_file_data_line(r'D:\notepad_file\202306', 'a')
# get_file_by_content(r'D:\notepad_file\202306', 'a')
# print(get_file(r'D:\notepad_file\202306', 'a'))
# print(get_file(r'D:\notepad_file\202306'))
# print(get_file())
# print(os.path.abspath('.'))

# print('end')
# for i in range(100):
#     print(get_file_name('a'))
#     # print(random_int(i))

# print(get_file_name('a'))

# print(to_list(r'D:\notepad_file\202306\asfdf.html', start_index=1285, end_index=1288))
# print(to_list(r'D:\notepad_file\202306\asfdf.html', start_index=1285, count=3))
# print(to_list(r'D:\notepad_file\202306\asfdf.html', start_line='<h2>Unicode 字符串</h2>', count=1))
# print(to_list(r'D:\notepad_file\202306\asfdf.html', start_line='<h2>Unicode 字符串</h2>', end_line='所有的字符串都是Unicode字符串'))
# print(to_list(r'D:\notepad_file\202306\asfdf.html', start_line='<h2>Unicode 字符串</h2>', end_line='所有的字符串都是Unicode字符串'))

#
# print(not False)
# print(not True)
# print(datetime.now())
# print(datetime.today())
# print(datetime.today().strftime('%m%d%H%M_%S_%f'))
# print(get_file_name('1'))
#
# for i in range(100):
#     print(get_file_name('a'))
#     # print(random_int(i))


# print(json.dumps(to_list(r'C:\Users\yangpu\Desktop\study\12.xls')))
