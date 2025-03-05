"""
cron: 30 9 * * *
new Env('小程序-霸王茶姬');

# 仅供学习交流，请在下载后的24小时内完全删除 请勿将任何内容用于商业或非法目的，否则后果自负。
# 抓包域名：https://webapi.qmai.cn任意请求中的请求头【qm-user-token】
# 小程序-霸王茶姬 变量
export hook_bwcj='[
    {
     "name":"ls",
     "drawNum":这里写抽奖次数1：抽奖1次, 0 不抽奖，
     "token":"KsZCd6TDWtHDuG6wHun_acSIfuo3eAd6Nu9LPPpu_C6k26Xp7nA1t_NJy1MdI7ys",
     "ua":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 MicroMessenger/6.8.0(0x16080000) NetType/WIFI MiniProgramEnv/Mac MacWechat/WMPF MacWechat/3.8.7(0x13080709) XWEB/1181"
    }
]'
"""
import json
from datetime import datetime

import requests

from utils import notify, common


class TASK:
    def __init__(self, i, ck):
        self.usedPointsLimitTimes = 0
        self.todayUsedPointsTimes = 0
        self.token = ck['token']
        self.name = ck['name']
        self.drawNum = ck.get("drawNum", 0)
        self.level = 0
        self.totalPoints = 0
        self.id = None
        self.index = i + 1
        if ck['ua']:
            self.ua = ck['ua']
        self.ua = 'Mozilla/5.0 (iPhone; CPU iPhone OS 15_4_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.33(0x18002129) NetType/WIFI Language/zh_CN"'
        self.headers = {
            'qm-user-token': self.token,
            'User-Agent': self.ua,
            'qm-from': 'wechat',
            "qm-from-type": "catering",
            'Content-Type': 'application/json',
            'Accept': 'v=1.0',
            'Cache-Control': 'no-cache',
            'Host': 'webapi.qmai.cn',
            'Connection': 'keep-alive',
            "referer": "https://servicewechat.com/wxafec6f8422cb357b/148/page-frame.html"
        }
        self.ss = requests.session()
        self.dateStr = datetime.now().strftime('%Y-%m-%d')
        self.timeStr = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.msg = ""

    def log(self, method=None, msg=None):
        if method:
            print(f"{datetime.now().strftime('%H:%M:%S')} 用户{self.index}【{self.name}】：【{method}】- {msg}")
        else:
            print(f"{datetime.now().strftime('%H:%M:%S')} 用户{self.index}【{self.name}】：{msg}")

    def getUserInfo(self):
        # 获取openid
        url = "https://webapi.qmai.cn/web/catering/crm/customer-center?appid=wxafec6f8422cb357b"
        response = self.ss.get(url=url, headers=self.headers)
        if response.status_code == 200:
            res = response.json()
            if res['code'] == "0":
                self.level = res['data']["customerCenterCardLevelInfo"]["level"]
                self.log(None, f"等级：Level {self.level}")
                self.msg += f"\n【用户{self.index}】等级：Level {self.level}"
                return True
            else:
                return False
        return False

    def getUserPoint(self):
        # 获取openid
        url = "https://webapi.qmai.cn/web/catering/crm/points-info"
        data = {
            "appid": "wxafec6f8422cb357b"
        }
        response = self.ss.post(url=url, headers=self.headers, data=json.dumps(data))
        if response.status_code == 200:
            res = response.json()
            if res['code'] == "0":
                self.totalPoints = res["data"]["totalPoints"]
                self.log(None, f"积分：{self.totalPoints}")
                self.msg += f"\n【用户{self.index}】积分：{self.totalPoints}"

    def getSignInfo(self):
        url = "https://webapi.qmai.cn/web/cmk-center/sign/userSignStatistics"
        data = {
            "activityId": "947079313798000641",
            "bizScene": 1,
            "appid": "wxafec6f8422cb357b"
        }
        response = self.ss.post(url=url, headers=self.headers, data=json.dumps(data))
        if response.status_code == 200:
            res = response.json()
            if res['message'] == "ok":
                self.log(None, f"连续签到📅：{res['data']['signDays']} 天")
                self.msg += f"\n【用户{self.index}】连续签到📅：{res['data']['signDays']} 天"
                if res['data']['signStatus'] == 2:
                    self.doSign()
                else:
                    self.log(None, f"签到：{res['message']}")

    def doSign(self):
        url = "https://webapi.qmai.cn/web/cmk-center/sign/takePartInSign"
        data = {
            "activityId": "947079313798000641",
            "appid": "wxafec6f8422cb357b"
        }
        response = self.ss.post(url=url, headers=self.headers, data=json.dumps(data))
        if response.status_code == 200:
            res = response.json()
            if res['code'] == 0 and res['status']:
                self.log(None, f"签到：签到成功！")
                self.msg += f"\n【用户{self.index}】签到：签到成功"
                return True
            else:
                self.log(None, f"签到：失败{res['message']}")
                self.msg += f"\n【用户{self.index}】签到：签到失败"
        return False

    def userLotteryTimes(self):
        url = "https://webapi.qmai.cn/web/cmk-center/lottery/userLotteryTimes"
        data = {
            "activityId": "969970382172651521",
            "appid": "wxafec6f8422cb357b"
        }
        response = self.ss.post(url=url, headers=self.headers, data=json.dumps(data))
        if response.status_code == 200:
            res = response.json()
            if res['code'] == 0 and res['status']:
                self.todayUsedPointsTimes = res['data']['todayUsedPointsTimes']
                self.usedPointsLimitTimes = res['data']['usedPointsLimitTimes']
            else:
                self.log(None, f"签到：失败{res['message']}")
                self.msg += f"\n【用户{self.index}】签到：签到失败"
        return False

    def userReward(self):
        url = "https://webapi.qmai.cn/web/cmk-center/lottery/userReward"
        data = {
            "activityId": "969970382172651521",
            "pageNo": 1,
            "pageSize": 10,
            "appid": "wxafec6f8422cb357b"
        }
        response = self.ss.post(url=url, headers=self.headers, data=json.dumps(data))
        self.log(None, f"------奖品记录------")
        if response.status_code == 200:
            res = response.json()
            if res['code'] == 0 and res['status']:
                rewards = res['data']['list']
                for reward in rewards:
                    self.log(None, f"{reward['date']} 抽中 {reward['customerRewardName']}")
                return True
            else:
                pass
        return False

    def lottery(self):
        url = "https://webapi.qmai.cn/web/cmk-center/lottery/takePartInLottery"
        data = {
            "activityId": "969970382172651521",
            "appid": "wxafec6f8422cb357b"
        }
        response = self.ss.post(url=url, headers=self.headers, data=json.dumps(data))
        if response.status_code == 200:
            res = response.json()
            if res['code'] == 0 and res['status']:
                customerRewardName = res['data']['clientRewardVo']['customerRewardName']
                self.log(None, f"第{self.todayUsedPointsTimes + 1}次抽到奖品：{customerRewardName}")
                self.msg += f"\n【用户{self.index}】第{self.todayUsedPointsTimes + 1}抽到奖品：{customerRewardName}"
                return True
            else:
                self.log(None, f"第{self.todayUsedPointsTimes + 1}抽奖失败：{res['message']}")
                self.msg += f"\n【用户{self.index}】第{self.todayUsedPointsTimes + 1}抽奖失败：{res['message']}"
        return False

    def run(self):
        print(f"*********开始第{self.index}个用户*********")
        msg = f"\n*********第{self.index}用户*********"
        msg += f"\n【用户{self.index}】备注：{self.name}"
        if self.getUserInfo():
            self.getUserPoint()
            self.getSignInfo()
            self.userLotteryTimes()
            self.log(None, f"------开始抽奖------")
            if self.drawNum <= 0:
                self.log(None, f"设置了抽奖次数 0，跳过抽奖！")
            else:
                self.log(None, f"今日抽奖次数：{self.todayUsedPointsTimes}/{self.usedPointsLimitTimes}")
                for userLotteryTime in range(self.usedPointsLimitTimes):
                    if self.todayUsedPointsTimes < self.usedPointsLimitTimes and self.todayUsedPointsTimes <= self.drawNum:
                        if not self.lottery():
                            break
                        self.userLotteryTimes()
                self.userReward()
        else:
            self.log(f"token 失效")
            self.msg += f"\n【用户{self.index}】token 失效"
        return self.msg


if __name__ == "__main__":
    env_tips = """='[
        {
        "token":"",
        "ua":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 MicroMessenger/6.8.0(0x16080000) NetType/WIFI MiniProgramEnv/Mac MacWechat/WMPF MacWechat/3.8.7(0x13080709) XWEB/1181",
        "name":"ls",
        "drawNum": 0
        }
    ]' """
    accounts = common.getEnv("x_bwcj", env_tips, 1.0)
    push_msg = [TASK(index, account).run() for index, account in enumerate(accounts)]
    notify.send("【小程序_霸王茶姬】", "".join(push_msg))
