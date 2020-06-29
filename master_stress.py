from locust import HttpUser, task, between
import json
import random
import time
import datetime
import calendar
from datetime import date, timedelta


# 執行指令:  locust -H http://master.fnjtd.com -f locust_example.py
# 使用方式: 1.Master部分必須要帶 get，post所需的request headers
#          2.先執行完指令後，在開啟本機的locust，輸入你需要壓測的參數

def json_format(data):  # json資料轉換
    json_data = json.dumps(data)
    # print(type(json_data))
    return json_data


def betRecord_start():
    # 投注紀錄查詢 -- 取得上個月一號的日期
    WagersTimeBegin = (date.today().replace(day = 1) - timedelta(1)).replace(day = 1).strftime("%Y/%m/%d")
    return WagersTimeBegin


def get_first_day():
    """ 當月的第一天 到 最後一天"""
    time = datetime.datetime.now()  # 年，月，日  # 年，月，日
    # 求該月第一天
    first_day = datetime.datetime(time.year, time.month, 1)
    days_num = calendar.monthrange(first_day.year, first_day.month)[1]  # 獲取一個月有多少天
    first_day_of_month = first_day + datetime.timedelta(days = days_num - 1)  # 當月的最後一天只需要days_num-1即可
    return first_day, first_day_of_month


class WebsiteTasks(HttpUser):
    account = 'sky'
    password = 'a123456'
    header = {'Content-Type': "application/json", 'X-Requested-With': "XMLHttpRequest"}
    wait_time = between(5, 9)
    first_day = get_first_day()[0]
    today = get_first_day()[1]

    def on_start(self):
        """ on_start is called when a Locust start before any task is scheduled """
        self.login(self.account, self.password)

    def on_stop(self):
        """ on_stop is called when the TaskSet is stopping """
        self.logout()

    def login(self, account, password):
        data = {'account': account, 'password': password}
        data = json.dumps(data)
        self.client.post("/Account/ValidateAccount", data, headers = self.header)

    def info(self):  # 取得connectionId資訊
        data = {}
        response_data = self.client.post('/signalr/negotiate', data, headers = self.header)
        connectionId = response_data.json()
        return connectionId['ConnectionId']

    def memberTransaction(self):
        data = {}
        response_data = self.client.post('/MemberTransaction/QueryInit', data, headers = self.header)
        types = response_data.json()  # 取得交易類型
        rnd = random.randint(0, 9)  # 亂數交易類型
        data = {"Types": [types['Types'][rnd]['Key']]}
        self.client.post('/MemberTransaction/Search', json_format(data), headers = self.header)  # 交易查詢
        self.client.post('/MemberTransaction/Export', json_format(data), headers = self.header)  # 交易紀錄匯出

    def ThirdPartyPayment(self):
        rnd = random.randint(1, 5)
        data = {"count": 25,
                "query": {"search": "true", "_": int(time.time()), "States": [rnd], "IsCheckStates": 'true',
                          "isDTPP": 'true'}}  # 亂數以狀態做查詢
        response_data = self.client.post('/ThirdPartyPayment/LoadNew', json_format(data),
                                         headers = self.header)  # 線上存款查詢
        max_id = response_data.json()
        # print(max_id)
        data = {"search": "true", "_": int(time.time()), "States": [rnd], "IsCheckStates": 'true', "isDTPP": 'true',
                "maxId": max_id['Data'][0]['Id']}
        self.client.post('/ThirdPartyPayment/Export', json_format(data), headers = self.header)  # 線上存款匯出

    def VerifyDeposit(self):
        rnd = random.randint(0, 2)
        data = {"count": 100, "query": {"search": "true", "_": int(time.time()), "States": [rnd],
                                        "IsCheckStates": 'true'}}  # 亂數以狀態做查詢
        response_data = self.client.post('/ThirdPartyPayment/LoadNew', json_format(data),
                                         headers = self.header)  # 公司入款查詢
        max_id = response_data.json()
        # print(max_id)
        data = {"search": "true", "_": int(time.time()), "States": [rnd], "IsCheckStates": 'true', "isDTPP": 'true',
                "maxId": max_id['Data'][0]['Id']}
        self.client.post('/VerifyDeposit/Export', json_format(data), headers = self.header)  # 公司入款匯出

    def VerifyWithdraw(self):
        rnd = random.randint(1, 4)
        data = {"count": 100,
                "query": {"search": "true", "_": int(time.time()), "States": 1, "IsCheckStates": 'true'}}
        response_data = self.client.post('/VerifyWithdraw/Load', json_format(data), headers = self.header)  # 線上取款查詢
        max_id = response_data.json()
        # print(max_id)
        data = {"search": "true", "_": int(time.time()), "States": [rnd], "IsCheckStates": 'true', "maxId": max_id}
        time.sleep(7)
        self.client.post('/VerifyWithdraw/Load', json_format(data), headers = self.header)  # 線上取款查詢
        deny_id = response_data.json()
        # print(deny_id)
        for i in range(10):
            data = {"id": deny_id['Data'][i]['Id']}
            self.client.post('/VerifyWithdraw/Deny', json_format(data), headers = self.header)  # 退回

    def game_type(self, rnd):  # 亂數取得娛樂廳種類
        data = {}
        response_data = self.client.post('/BetRecord/GetKindCategories', data, headers = self.header)
        response_data = response_data.json()
        get_list = response_data[rnd]['Categories']
        kind_list = list()
        for i in range(len(get_list)):
            kind_list.append(get_list[i]['PropertyName'])
        return kind_list

    def BetRecord(self):
        connectionId = self.info()
        rnd = random.randint(0, 5)
        game_list = self.game_type(rnd)
        gameCategories = game_list.pop()
        data = {'Agent':"QA_4","WagersTimeBegin": betRecord_start(), "GameCategories": [gameCategories],
                "connectionId": connectionId}
        self.client.post('/BetRecord/Search', json_format(data), headers = self.header)  # 投注記錄查詢
        data = {"WagersTimeBegin": self.first_day, "GameCategories": [gameCategories]}
        self.client.post('/BetRecord/Export', json_format(data), headers = self.header)  # 投注記錄匯出
        data = {"searchParams": {"WagersTimeBegin": self.first_day, "WagersTimeEnd": self.today,
                                 "GameCategories": [gameCategories]}, "pageSize": 100}
        self.client.post('/BetRecord/AdvancedLoadV2', json_format(data), headers = self.header)  # 進階投注紀錄查詢
        data = {
            "searchParams": {"WagersTimeBegin": self.first_day, "WagersTimeEnd": self.today,
                             "GameCategories": [gameCategories]}, "category": gameCategories}
        self.client.post('/BetRecord/AdvancedExportV2', json_format(data), headers = self.header)  # 進階投注匯出

    def SendMail(self):
        data = {"SendMailType": 4,
                "MailRecievers": " ",
                "BatchParam": " ",
                "SearchParam": " ",
                "SuperSearchRequest": " ",
                "ResendMailID": " ",
                "Subject": "測試站內信(發送對象--全站)",
                "MailBody": "<p>"
                            "測試批次站內信測試批次站內信測試批次站內信"
                            "測試批次站內信測試批次站內信測試批次站內信"
                            "測試批次站內信測試批次站內信測試批次站內信"
                            "測試批次站內信測試批次站內信測試批次站內信"
                            "測試批次站內信測試批次站內信測試批次站內信"
                            "測試批次站內信測試批次站內信測試批次站內信"
                            "測試批次站內信測試批次站內信測試批次站內信"
                            "</p>\n",
                "ExcelFilePath": " "}
        self.client.post('/SiteMail/SendMail', json_format(data), headers = self.header)  # 全站寄信

    def MemberLogin(self, member):
        data = {"search": {"Account": member}, "pageIndex": "", "pageSize": 10}
        self.client.post('/MemberLogin/SearchV2', json_format(data), headers = self.header)  # 登入紀錄
        data = {"search": {}}
        self.client.post('/MemberLogin/Export', json_format(data), headers = self.header)  # 登入紀錄匯出

    # -----------------------------------------------------------------------------------------------------------------------------#
    @task(80)
    def A_first_Mission(self):
        connectionId = self.info()
        data = {"connectionId": connectionId}
        data = json.dumps(data)
        self.client.post("/Member/Search", data, headers = self.header)
        self.ThirdPartyPayment()

    @task(4)
    def B_second_Mission(self):
        connectionId = self.info()
        data = {"connectionId": connectionId}
        data = json.dumps(data)
        self.client.post("/Member/Search", data, headers = self.header)
        self.SendMail()

    @task(40)
    def C_second_Mission(self):
        connectionId = self.info()
        data = {"connectionId": connectionId}
        data = json.dumps(data)
        self.client.post("/Member/Search", data, headers = self.header)
        self.ThirdPartyPayment()

    @task(40)
    def D_second_Mission(self):
        connectionId = self.info()
        data = {"connectionId": connectionId}
        data = json.dumps(data)
        self.client.post("/Member/Search", data, headers = self.header)
        self.VerifyDeposit()

    @task(40)
    def E_second_Mission(self):
        connectionId = self.info()
        data = {"connectionId": connectionId}
        data = json.dumps(data)
        self.client.post("/Member/Search", data, headers = self.header)
        self.memberTransaction()

    @task(40)
    def F_second_Mission(self):
        connectionId = self.info()
        data = {"connectionId": connectionId}
        data = json.dumps(data)
        self.client.post("/Member/Search", data, headers = self.header)
        self.VerifyWithdraw()

    @task(140)
    def G_second_Mission(self):
        connectionId = self.info()
        data = {"connectionId": connectionId}
        data = json.dumps(data)
        self.client.post("/Member/Search", data, headers = self.header)
        self. VerifyDeposit()

    @task(40)
    def H_second_Mission(self):
        connectionId = self.info()
        data = {"connectionId": connectionId}
        data = json.dumps(data)
        self.client.post("/Member/Search", data, headers = self.header)
        # self.VerifyWithdraw()
        self.BetRecord()

    def logout(self):
        self.client.post("/Account/SignOut")
