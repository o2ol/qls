"""
代码请勿用于非法盈利,一切与本人无关,该代码仅用于学习交流,请阅览下载24小时内删除代码
# 注册地址 https://ikuuu.pw/auth/register?code=xLmV
new Env("x_途虎")
cron: 12 0 * * *
export x_tuhu="[
     {
        "token":"",
        "ua":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 MicroMessenger/6.8.0(0x16080000) NetType/WIFI MiniProgramEnv/Mac MacWechat/WMPF MacWechat/3.8.7(0x13080709) XWEB/1181",
        "name":"ls",
        }
]"
"""
import traceback

import requests

from utils import notify, common


class TASK:
    def __init__(self, index, account):
        self.blackbox = "lMPHJ1740990140UyG8i6SCIze"
        self.index = index
        self.token = account.get('token', "")
        self.name = account.get("name", None)
        self.ua = account.get("ua",
                              'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.40(0x1800282c) NetType/WIFI Language/zh_CN')
        self.headers = {
            'host': 'cl-gateway.tuhu.cn',
            'content-type': 'application/json',
            'channel': 'wechat-miniprogram',
            'api-level': '2',
            'platformSource': 'uni-app',
            'blackbox': self.blackbox,
            'user-agent': self.ua,
            'Authorization': self.token,
            'authType': 'oauth',
            'Content-Type': 'application/json'
        }
        self.session = requests.Session()
        self.msg = ""

    def user_info(self):
        try:
            res = requests.post(f"https://cl-gateway.tuhu.cn/cl-user-info-site/userAccount/getCurrentUserInfo",
                                headers=self.headers, json={})
            # print(f"res {res.text}")
            if res.status_code == 200:
                rj = res.json()
                if rj['code'] != 10000:
                    return False
                print(f"用户ID：{rj['data']['userId']}")
                print(f"用户昵称：{rj['data']['nickName']}")
                print(f"手机号码：{rj['data']['mobile'][0:3]+'****'+rj['data']['mobile'][-4:]}")
                return True
            else:
                return False
        except Exception as e:
            print(f"账号{self.index}签到失败，请检查网络{traceback.format_exc()}")
            return False

    def user_point(self):
        self.headers['host'] = "cl-gateway.tuhu.cn"
        url = "https://cl-gateway.tuhu.cn/cl-common-api/api/personalCenter/getPersonalProductInfo"
        try:
            res = requests.post(url, headers=self.headers, json={})
            # print(f"res {res.text}")
            if res.status_code == 200:
                rj = res.json()
                if rj['code'] != 10000:
                    return False
                print(f"------资产信息------")
                print(f"积分余额：{rj['data']['integralCount']}")
                print(f"优惠券：{rj['data']['couponCount']}")
                return True
            else:
                return False
        except Exception as e:
            print(f"账号{self.index}签到失败，请检查网络{traceback.format_exc()}")
            return False

    def user_grade(self):
        self.headers['host'] = "api.tuhu.cn"
        try:
            res = requests.post(f"https://api.tuhu.cn/User/SelectMemberGradePermissionList", headers=self.headers,
                                json={})
            # print(f"res {res.text}")
            if res.status_code == 200:
                rj = res.json()
                if rj['Code'] == '1':
                    print(f"会员等级:{rj['UserGradeInfo']['GradeCode']}{rj['UserGradeInfo']['GradeName']}")
                    return True
                return False
            else:
                return False
        except Exception as e:
            print(f"账号{self.index}签到失败，请检查网络{traceback.format_exc()}")
            return False

    def check_status(self):
        self.headers['host'] = "api.tuhu.cn"
        try:
            r = requests.get(url=f"https://api.tuhu.cn/User/GetMemberSignInInfoAsync?channel=wxapp",
                             headers=self.headers)
            # print(f"res {r.text}")
            rj = r.json()
            if rj['Code'] == '1':
                print(f"签到状态：{'未签到' if not rj['SignInStatus'] else '今日已签到'}")
                print(f"------签到日历📅-----：")
                for item in rj['Detail']:
                    print(f"第{item['ContinuousDays']}天：{'已签到✅' if item['IsSignedIn'] else '未签到'}")
                return rj['SignInStatus']
            else:
                return False
        except Exception as e:
            print(f"账号{self.index} 异常{traceback.format_exc()}")
            return False

    def check_in(self):
        self.headers['host'] = "cl-gateway.tuhu.cn"
        try:
            res = requests.post(f"https://cl-gateway.tuhu.cn/cl-common-api/api/dailyCheckIn/userCheckIn",
                                headers=self.headers, json={"channel": "wxapp"})
            print(f"res {res.text}")
            if res.status_code == 200:
                rj = res.json()
                print(f"签到结果：{rj['message']}")
                # acc['checkInResult'] = rj['message']
                if rj['code'] == 10000:
                    print(f"签到奖励：{rj['data']['rewardIntegral']}")
                    return True
                return False
            else:
                return False
        except Exception as e:
            print(f"账号{self.index}签到失败，请检查网络{traceback.format_exc()}")

    def run(self):
        print(f"====开始账号{self.index}：{self.name}====")
        self.msg = f"账号[{self.index}]：{self.name}"
        if self.user_info():
            self.user_grade()
            if not self.check_status():
                self.check_in()
            self.user_point()
        return self.msg


if __name__ == '__main__':
    env_tips = """='[
        {
        "token":"",
        "ua":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 MicroMessenger/6.8.0(0x16080000) NetType/WIFI MiniProgramEnv/Mac MacWechat/WMPF MacWechat/3.8.7(0x13080709) XWEB/1181",
        "name":"ls",
        }
    ]' """
    accounts = common.getEnv("x_tuhu", env_tips, 1.2)
    push_msg = [TASK(index, account).run() for index, account in enumerate(accounts, start=1)]
    notify.send("[{}]".format("ikuuu"), "".join(push_msg))
