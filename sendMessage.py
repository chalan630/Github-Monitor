'''
Modify: chalan630
Date: 2021-07-20 17:02:43
LastEditTime: 2021-07-23 18:04:30
GitHub: https://github.com/JustYoomoon/CVEAP
Description: 发送信息函数
'''
from os import stat
import requests
import dingtalkchatbot.chatbot as cb


def mail(text, msg):
    try:
        import smtplib
        from email.mime.text import MIMEText
        from email.utils import formataddr
        my_sender = 'xxxxxx@xxx.com'  # 发件人邮箱账号
        my_pass = 'xxxxxx'  # 发件人邮箱授权码 / 腾讯企业邮箱请使用登陆密码
        recipients = 'xxxxxx@xxx.com'  # 收件人邮箱账号
        # 内容
        msg = MIMEText('{}\r\n{}'.format(text, msg), 'plain', 'utf-8')
        # [发件人邮箱昵称、发件人邮箱账号], 昵称随便
        msg['From'] = formataddr([text, my_sender])
        # [收件人邮箱昵称、收件人邮箱账号], 昵称随便
        msg['To'] = formataddr(["推送目标", recipients])

        # 邮件的主题、标题
        msg['Subject'] = "漏洞武器库该更新啦！！！"

        # 用的腾讯企业邮箱做的测试   如果要用其他邮箱的话
        # 用其他邮箱作为发件人的话,请将"smtp.exmail.qq.com" 修改为 "xxxxxxxxxx.xxxx.com"
        # 发件人邮箱中的SMTP服务器端口  我这里是腾讯企业邮箱465  请查看自己的SMTP服务器端口号
        server = smtplib.SMTP_SSL("smtp.exmail.qq.com", 465)
        server.login(my_sender, my_pass)
        server.sendmail(my_sender, recipients, msg.as_string())
        server.quit()  # 关闭连接
        print("邮件发送成功")
    except Exception as e:
        print("邮件发送失败: ", e)


# 钉钉
def dingding(text, msg):
    # 将此处换为钉钉机器人的api
    webhook = ''
    ding = cb.DingtalkChatbot(webhook, secret="")
    ding.send_text(msg='{}\n{}'.format(text, msg), is_at_all=False)


# server酱  http://sc.ftqq.com/?c=code
def server(text, msg):
    # 将 xxxx 换成自己的server SCKEY
    uri = 'https://sc.ftqq.com/xxxx.send?text={}&desp={}'.format(text, msg)
    requests.get(uri)


# 添加Telegram Bot推送支持
def tgbot(text, msg):
    import telegram
    # Your Telegram Bot Token
    bot = telegram.Bot(token='')
    group_id = ''
    bot.send_message(chat_id=group_id, text='{}\r\n{}'.format(text, msg))