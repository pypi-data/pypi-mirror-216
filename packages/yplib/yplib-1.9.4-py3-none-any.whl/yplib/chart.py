from yplib.chart_html import *
from yplib.index import *


# 将 html 中的占位符 替换成数据
# 并且 导出 生成后的 html 文件
def insert_data_to_chart(html_data,
                         name=None,
                         x_list=None,
                         y_list=None,
                         legend=None,
                         series=None,
                         smooth=0):
    p_list = [
        'chart_name', 'name', 'x_list', 'y_list', 'legend', 'series', 'smooth'
    ]
    p_data_list = [
        name, name, x_list, y_list, legend, series, smooth
    ]
    h_r = []
    for html_line in html_data:
        for index in range(len(p_list)):
            one_p = p_list[index]
            one_data = p_data_list[index]
            if one_data is None:
                continue
            one_p = f'-{one_p}-'
            if one_p in html_line:
                html_line = html_line.replace(one_p, str(one_data))
        h_r.append(html_line)
    to_txt(data_list=h_r,
           file_name=str(name),
           file_path='html',
           fixed_name=False,
           suffix='.html')
    # current_path = os.path.abspath(__file__)
    # html_list = open(current_path[0:current_path.find('__init__')] + 'line-stack-temp.html', 'r', encoding='utf-8').readlines()


# 将数据整理成折线图
#  x轴数据 : x_list = [
#       ['x轴的数据', 'line1', 'line2', 'line3'],
#       ['2020-01-01', 120, 132, 101],
#       ['2020-01-02', 100, 102, 131],
#       ['2020-01-03', 123, 165, 157],
#       ['2020-01-04', 126, 109, 189],
#       ['2020-01-05', 150, 156, 128],
#       ['2020-01-06', 178, 134, 140],
#       ['2020-01-07', 157, 148, 161],
#  ]
#  --- 以上这种情况,当 y_list 为空的时候,就说明有可能是这种情况
#  --- 以上这种情况,数据与 excel 中的数据对齐
#  --- 以下是第二种情况的 api
# x轴数据 : x_list = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
# y轴数据 : y_list = [
#             {
#                 name: 'Email',
#                 hide: True,
#                 smooth: True,
#                 data: [120, 132, 101, 134, 90, 230, 210],
#             },
#             {
#                 name: 'Union Ads',
#                 hide: 1,
#                 smooth: 1,
#                 data: [220, 182, 191, 234, 290, 330, 310],
#             },
#             {
#                 name: 'Video Ads',
#                 data: [150, 232, 201, 154, 190, 330, 410],
#             },
#             {
#                 name: 'Direct',
#                 data: [320, 332, 301, 334, 390, 330, 320],
#             },
#             {
#                 name: 'Search Engine',
#                 data: [820, 932, 901, 934, 1290, 1330, 1320],
#             },
#         ]
#  name : 文件名称,折线图的名称
#  name_raw : 用原始的名字,不用带上属性 line_stack
def to_chart(x_list,
             y_list=None,
             name=None,
             name_raw=False):
    # 当 y_list 没有的话, 需要整理出 y_list 的数据
    if y_list is None:
        data_list = x_list
        x_list = []
        y_list = []
        for index in range(len(data_list)):
            line_one = data_list[index]
            if index > 0:
                x_list.append(line_one[0])
            # 第一行数据
            if index == 0:
                for y in range(1, len(line_one)):
                    y_list.append({'name': line_one[y], 'data': []})
            # 第二行开始的数据
            if index > 0:
                for y in range(1, len(line_one)):
                    y_list[y - 1]['data'].append(line_one[y])
    legend_data = []
    legend_selected = {}
    for y_one in y_list:
        name_one = y_one['name']
        legend_data.append(name_one)
        if 'hide' in y_one and y_one['hide']:
            legend_selected[name_one] = 0
    legend = 'data: ' + str(legend_data) + ',\n            selected: ' + str(legend_selected)
    # {
    #     name: 'Email',
    #     type: 'line',
    #     stack: 'Total',
    #     data: [120, 132, 101, 134, 90, 230, 210],
    # }
    series = []
    for y_one in y_list:
        if len(y_list) == 1:
            del y_one['name']
        y_one['type'] = 'line'
        y_one['stack'] = 'Total'
        if 'smooth' in y_one and y_one['smooth']:
            y_one['smooth'] = 1
        else:
            y_one['smooth'] = 0
        series.append(y_one)

    if not name_raw:
        name = 'line_stack' if name is None else name + '_line_stack'
    insert_data_to_chart(html_data=line_stack_html(),
                         name=name,
                         x_list=x_list,
                         legend=legend,
                         series=series)


# print(str([1, 2, 3]))
# print(str(['a', 'b', 'c']))
# print(str(map(['a', 'b', 'c'])))
# print(str(list(map(lambda x: {str(x): 0}, [1, 2, 3, 4]))))

# 将数据整理成折线图
# 一条折线
# 数据 : data_list = [
#             ['2020-01-01', 132],
#             ['2021-01-01', 181],
#             ['2022-01-01', 147]
#         ]
# x_index : x 轴数据的下标
# y_index : y 轴数据的下标
# 或者
# 数据 : data = [
#        {name: "Search Engine", value: 1048 },
#        {name: "Direct", value: 735 },
#        {name: "Email", value:580 },
#        {name: "Union Ads", value:484 },
#        {name: "Video Ads", value:300 }
#       }]
#  x_key : 当元素为对象的时候, x 的 key
#  y_key : 当元素为对象的时候, y 的 key
# is_area : 是否使用 area 图
# smooth : 曲线是否平滑
def to_chart_one(data_list,
                 name=None,
                 x_index=0,
                 x_key='name',
                 y_index=1,
                 y_key='value',
                 is_area=False,
                 smooth=False):
    x_list = []
    y_list = []
    name = 'line' if name is None else name + '_line'
    name = name + '_smooth' if smooth else name
    name = name + '_area' if is_area else name
    sm = 1 if smooth else 0
    for d_one in data_list:
        if isinstance(d_one, list):
            x = d_one[x_index]
            y = d_one[y_index]
        else:
            x = d_one[x_key]
            y = d_one[y_key]
        x_list.append(x)
        y_list.append(y)
    if is_area:
        insert_data_to_chart(html_data=line_area_html(),
                             name=name,
                             x_list=x_list,
                             y_list=y_list,
                             smooth=sm)
    else:
        to_chart(x_list=x_list,
                 y_list=[{'name': name, 'data': y_list, 'smooth': sm}],
                 name=name,
                 name_raw=True)


# 将数据整理成饼状图
# 数据 : data = [
#         { value: 1048, name: "Search Engine" },
#         { value: 735, name: "Direct" },
#         { value: 580, name: "Email" },
#         { value: 484, name: "Union Ads" },
#         { value: 300, name: "Video Ads" }
#       ]
#  name_key : 当元素为对象的时候, x 的 key
#  value_key : 当元素为对象的时候, y 的 key
# 或者
# 数据 : data = [
#         [ "Search Engine", 1048 ],
#         [ "Direct", 735 ],
#         [ "Email",580 ],
#         [ "Union Ads",484 ],
#         [ "Video Ads",300 ]
#       ]
#  name_index : 当元素为数组的时候, name 的下标
#  value_index : 当元素为数组的时候, value 的下标
def to_chart_pie(data_list,
                 name=None,
                 name_index=0,
                 name_key='name',
                 value_index=1,
                 value_key='value'):
    x_list = []
    name = 'pie' if name is None else name + '_pie'
    for one_data in data_list:
        if isinstance(one_data, list):
            x = one_data[name_index]
            y = one_data[value_index]
        else:
            x = one_data[name_key]
            y = one_data[value_key]
        x_list.append({'name': x, 'value': y})
    insert_data_to_chart(html_data=pie_html(),
                         name=name,
                         x_list=x_list)


# 将数据整理成柱状图
# 数据 : data = [
#         { value: 1048, name: "Search Engine" },
#         { value: 735, name: "Direct" },
#         { value: 580, name: "Email" },
#         { value: 484, name: "Union Ads" },
#         { value: 300, name: "Video Ads" }
#       ]
#  name_key : 当元素为对象的时候, x 的 key
#  value_key : 当元素为对象的时候, y 的 key
# 或者
# 数据 : data = [
#         [ "Search Engine", 1048 ],
#         [ "Direct", 735 ],
#         [ "Email",580 ],
#         [ "Union Ads",484 ],
#         [ "Video Ads",300 ]
#       ]
#  name_index : 当元素为数组的时候, name 的下标
#  value_index : 当元素为数组的时候, value 的下标
def to_chart_bar(data_list,
                 name=None,
                 name_index=0,
                 name_key='name',
                 value_index=1,
                 value_key='value'):
    x_list = []
    y_list = []
    name = 'bar' if name is None else name + '_bar'
    for one_data in data_list:
        if isinstance(one_data, list):
            x = one_data[name_index]
            y = one_data[value_index]
        else:
            x = one_data[name_key]
            y = one_data[value_key]
        x_list.append(x)
        y_list.append(y)
    insert_data_to_chart(html_data=bar_html(),
                         name=name,
                         x_list=x_list,
                         y_list=y_list)


# test_list = []
# # for i in range(10):
# #     data.append([uuid_random(), int(random.uniform(0, 1000))])
# for i in range(10):
#     one = {}
#     one['name'] = random_uuid()
#     one['value'] = int(random.uniform(0, 1000))
#     test_list.append(one)
#
# to_chart_bar(test_list)

#
#
# test_list = []
# for i in range(10):
#     test_list.append([random_uuid(), int(random.uniform(0, 1000))])
#
# to_chart_pie(test_list)
# to_chart_pie(data, 'yp')

# x_list = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
# y_list = json.loads(
#     '[{"name":"Email","data":[120,132,101,134,90,230,210]},{"name":"Union Ads","data":[220,182,191,234,290,330,310]},{"name":"Video Ads","data":[150,232,201,154,190,330,410]},{"name":"Direct","data":[320,332,301,334,390,330,320]},{"name":"Search Engine","data":[820,932,901,934,1290,1330,1320]}]')
#

# # # 将 list 转化成 图表的例子
# x_list = []
# y_list = []
# # # x 轴有 100 个
# # # 100 个横坐标
# for i in range(1000):
#     x_list.append(i)
# #
# # 有 10 条线
# for i in range(10):  # 0 1 2 3 4 55
#     n = {}
#     n['name'] = str(int(random.uniform(0, 1000)))
#     data = []
#     # 每条线有 100 个纵坐标, 与 x_list 中的对应起来
#     for i in range(100):
#         data.append(int(random.uniform(0, 1000)))
#     n['data'] = data
#     # n['hide'] = '1'
#     y_list.append(n)
# #
# to_chart(x_list, y_list)
#
#
# test_list = []
# for i in range(50):
#     test_list.append([i, int(random_int(4))])
#     test_list.append({'name': i, 'value': int(random_int(4))})
#
# to_chart_one(test_list, name='yp')
# to_chart_one(test_list, name='yp', smooth=True)
# to_chart_one(test_list, name='yp', is_area=True)
# to_chart_one(test_list, name='yp', is_area=True, smooth=True)
#
# data_list =
#
# to_chart(data_list)

# to_chart(to_list(r'C:\Users\yangpu\Desktop\study\12.xls'))

# to_chart(to_list(r'C:\Users\yangpu\Desktop\study\12.xls', column_date=1), name='yp')

#
# print('end')
