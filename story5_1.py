"""
故事5:
1. 新增會員 - 更新會員銀行資料
2. 批次會員 - 修改標籤
"""
from file.member_list import member
from locust import HttpUser, task, between
import json
import time

master_url = 'http://ma.jp777.net'
Post_Master_Headers = {'Content-Type': "application/json", 'X-Requested-With': "XMLHttpRequest"}
Get_Mater_Headers = {'X-Requested-With': "XMLHttpRequest"}
upload_Mater_Headers = {'X-Requested-With': "XMLHttpRequest"}


def json_format(data):  # json資料轉換
    json_data = json.dumps(data)
    print(type(json_data))
    return json_data


class WebsiteTasks(HttpUser):
    account = 'jackson'
    password = 'a123456'
    header = {'Content-Type': "application/json", 'X-Requested-With': "XMLHttpRequest"}
    wait_time = between(3, 5)

    def on_start(self):
        """ on_start is called when a Locust start before any task is scheduled """
        self.login(self.account, self.password)

    def login(self, account, password):
        data = {'account': account, 'password': password}
        data = json.dumps(data)
        self.client.post("/Account/ValidateAccount", data, headers = self.header)

    def info(self):  # 取得connectionId資訊
        data = {}
        response_data = self.client.post('/signalr/negotiate', data, headers = self.header)
        connectionId = response_data.json()
        return connectionId['ConnectionId']

    @task
    def update_bank(self):
        memberAccount = member.pop()
        data = {"memberAccount": memberAccount, "GroupBankId": 1, "Province": str(int(time.time())),
                "City": str(int(time.time())),
                "Account": str(int(time.time())), "Memo": str(int(time.time())), "AlipayAccount": str(int(time.time())),
                "AlipayNickName": str(int(time.time())),
                "AlipayMemo": str(int(time.time())), "ForceUpdate": 'false'}
        self.client.post('/Member/UpdateBankAccount', json_format(data), headers = self.header)  # 更新銀行帳號
