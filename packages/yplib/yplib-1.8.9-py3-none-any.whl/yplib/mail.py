from yplib.index import *
from yplib.mail_html import *
import smtplib
from email.mime.text import MIMEText


def send_mail(title,
              content,
              user='',
              password='',
              send='',
              send_port=0,
              receivers=None):
    message = MIMEText(content, 'html', 'utf-8')  # 内容, 格式, 编码
    message['From'] = "{}".format(user)
    message['To'] = ",".join(receivers)
    message['Subject'] = title
    smtpObj = smtplib.SMTP_SSL(send, send_port)  # 启用SSL发信, 端口一般是465
    # try:
    smtpObj.login(user, password)
    smtpObj.sendmail(user, receivers, message.as_string())
    # return True
    # except smtplib.SMTPException as e:
    #     print(e)
    #     return False
    # finally:
    smtpObj.close()


# 获得 邮件的内容信息
# 正常的数据
# data_obj = {
# 	title: "里面的一份小标题",
# 	type: "error",
# 	content: [
# 		{ "调用次数": 100, "成功次数": 50 },
# 		"总体还算可以的"
# 	]
# }
#
# data_obj = [
#         { "调用次数": 100, "成功次数": 50 },
#         { "查询次数": 200, "失败次数": 150 },
#         { value: 735, name: "Direct" },
# 		"总体还算可以的"
#       ]
# data_obj = [
# 	{
# 		title: "里面的一份小标题",
# 		type: "error",
# 		content: [
# 			{ "调用次数": 100, "成功次数": 50 },
# 			"总体还算可以的"
# 		]
# 	},
# 	{
# 		title: "里面的一份正常的标题",
# 		content: [
# 			{ "调用次数": 500, "成功次数": 500 },
# 			"总体不行的"
# 		]
# 	}
# ]
def get_mail_html(data_obj):
    # if isinstance(data, dict) or isinstance(data, list) or isinstance(data, tuple) or isinstance(data, set):
    html_list = []
    if isinstance(data_obj, list):
        for data_one in data_obj:
            print(data_one)
            html_list.append(get_mail_html_one(data_one))
    else:
        html_list.append(get_mail_html_one(data_obj))
    return ''.join(mail_html(html_list))


# 获得 邮件的内容信息
# 正常的数据
# data_obj = {
# 	title: "里面的一份小标题",
# 	type: "error",
# 	content: [
#       {"调用次数": 100, "成功次数": 50},
#       {"调用次数": 1020, "成功次数": 510},
#       {"调用次数": 1030, "成功次数": 550},
#       {"调用次数": 1090, "成功次数": 590},
# 		"总体还算可以的"
# 	]
# }
def get_mail_html_one(data_obj):
    title = data_obj['title'] if 'title' in data_obj else str(to_datetime())
    type = data_obj['type'] if 'type' in data_obj else 'normal'
    content = data_obj['content'] if 'content' in data_obj else data_obj
    stripe = True
    html_list = []
    for o_c in content:
        if isinstance(o_c, dict) or isinstance(o_c, tuple) or isinstance(o_c, set):
            for o_k in o_c:
                html_list.extend(mail_content_html(key=o_k, value=o_c[o_k], error=type == 'error', stripe=stripe))
                stripe = not stripe
        else:
            html_list.extend(mail_content_html(key=o_c, error=type == 'error', stripe=stripe))
            stripe = not stripe
    return ''.join(mail_title_html(title, html_list, type == 'error'))

# print('end')

#
# h = get_mail_html({
#     'title': "里面的一份小标题",
#     # 'type': "error",
#     'content': [
#         {"调用次数": 100, "成功次数": 50},
#         {"调用次数": 1020, "成功次数": 510},
#         {"调用次数": 1030, "成功次数": 550},
#         {"调用次数": 1090, "成功次数": 590},
#         "总体还算可以的"
#     ]
# })
#
# send_mail(str(to_datetime())[0:19] + ' 测试', h,
#           user='wantwaterfish@163.com',
#           password='CKGCCQTBIDQVIITZ',
#           send='smtp.163.com',
#           send_port=465,
#           receivers=['1547878995@qq.com'])
#
#
