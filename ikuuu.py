"""
代码请勿用于非法盈利,一切与本人无关,该代码仅用于学习交流,请阅览下载24小时内删除代码
# 注册地址 https://ikuuu.pw/auth/register?code=xLmV
new Env("ikuuu签到")
cron: 12 0 * * *
export ikuuu="[
    {
        'name':"备注",
        'email': '邮箱',
        'pwd':'密码'
    }
]"
"""
import requests
from bs4 import BeautifulSoup

from utils import notify, common


class TASK:
    def __init__(self, index, account):
        self.index = index
        self.name = account.get('name', "")
        self.email = account.get("email", None)
        self.pwd = account.get("pwd", None)
        self.host = "ikuuu.one"
        self.header = {
            'origin': self.host,
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
            # 'contentType': "application/x-www-form-urlencoded; charset=UTF-8"
        }
        self.session = requests.Session()
        self.msg = ""

    def login(self):
        data = {
            "email": self.email,
            "passwd": self.pwd,
            'host': "ikuuu.pw"
        }
        res = self.session.post(f'https://{self.host}/auth/login', headers=self.header, data=data)
        if res.status_code == 200:
            self.msg += f"登陆账户：{self.name}"
            self.msg += f"登陆结果：登陆成功🎉"
            print(f"登陆账户：{self.name}")
            print(f"登陆结果：登陆成功🎉")

    def check_in(self):
        res = self.session.post(f'https://{self.host}/user/checkin', headers=self.header)
        if res.status_code == 200:
            self.msg += f"签到结果：{res.json()['msg']}"
            print(f"签到结果：{res.json()['msg']}")

    def user_info(self):
        res = self.session.get(f'https://{self.host}/user', headers=self.header)
        if res.status_code == 200:
            soup = BeautifulSoup(res.text, 'html.parser')

            # 提取会员时长
            membership = soup.find('div', class_='card-header').find_next_sibling('div',
                                                                                  class_='card-body').text.strip()
            print(f"会员时长: {membership}")
            self.msg += f"会员时长: {membership}"

            # 提取剩余流量
            restTraffic = soup.find_all('span', class_='counter')[0].text  # 第一个 counter 是剩余流量
            restTrafficUnit = soup.find_all('div', class_='card-body')[1].text.strip().split()[-1]  # 提取 GB
            print(f"剩余流量: {restTraffic} {restTrafficUnit}")
            self.msg += f"剩余流量: {restTraffic} {restTrafficUnit}"

            # 提取在线设备数
            onlineDevices = soup.find_all('span', class_='counter')[1].text  # 第二个 counter 是在线设备数
            totalDevices = soup.find('span', class_='counterup').text  # 总设备数
            print(f"在线设备: {onlineDevices}/{totalDevices}")
            self.msg += f"在线设备: {onlineDevices}/{totalDevices}"

            # 提取钱包余额
            walletBalance = soup.find_all('span', class_='counter')[2].text  # 第三个 counter 是钱包余额
            print(f"钱包余额: ¥{walletBalance}")
            self.msg += f"钱包余额: ¥{walletBalance}"

    def run(self):
        print(f"{'*' * 10}IKUUU开启签到{'*' * 10}")
        self.login()
        self.check_in()
        self.user_info()
        return self.msg


if __name__ == '__main__':
    env_tips = """='[
        {
        "token":"",
        "ua":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 MicroMessenger/6.8.0(0x16080000) NetType/WIFI MiniProgramEnv/Mac MacWechat/WMPF MacWechat/3.8.7(0x13080709) XWEB/1181",
        "name":"ls",
        "drawNum": 0
        }
    ]' """
    accounts = common.getEnv("ikuuu", env_tips, 1.0)
    push_msg = [TASK(index, account).run() for index, account in enumerate(accounts, start=1)]
    notify.send("[{}]".format("ikuuu"), "".join(push_msg))
