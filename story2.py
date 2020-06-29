"""
故事2:
1. BetRecord - 投注時間-上個月的1號結束日期:兩天前的時間
2. BetRecord - 投注時間-上個月的1號結束日期:兩天前的時間
3. 注單號碼查詢
5. 有效投注
6.派彩
"""
from locust import HttpUser, task, between
from connenction.HttpRequest import Master_Http
import json
from datetime import datetime, timedelta, date
import random

master_url = 'http://ma.jp777.net'
Post_Master_Headers = {'Content-Type': "application/json", 'X-Requested-With': "XMLHttpRequest"}


def json_format(data):  # json資料轉換
    json_data = json.dumps(data)
    return json_data


BeginDate = (date.today() - timedelta(7)).strftime("%Y/%m/%d")
EndTime = (datetime.now() + timedelta(hours = -20)).strftime("%Y/%m/%d %H:%M:%S")


class Master:
    def __init__(self):
        self.http = Master_Http()
        self.cookie = self.http.post(master_url + '/Account/ValidateAccount',
                                     {'account': 'sky', 'password': 'a123456'},
                                     Post_Master_Headers, {})
        self.connectionId = self.http.post(master_url + '/signalr/negotiate', {}, Post_Master_Headers, {})

    def Round(self):
        page = random.randint(2, 5)
        data = {"WagersTimeBegin": BeginDate, "GameCategories": ["Cq9Slot"],
                "connectionId": self.connectionId[1]['ConnectionId'], "pageIndex": page}
        response_data = self.http.post(master_url + '/BetRecord/Search', data, Post_Master_Headers, self.cookie[2])
        Id = random.randint(0, 8)
        get_RawData_Id = response_data[1]['PageData'][Id]['Id']  # 取得Id
        data = {"id": get_RawData_Id}
        response_data = self.http.post(master_url + '/BetRecord/GetRawData', data, Post_Master_Headers, self.cookie[2])
        Round_Id = response_data[1]['List'][1]['Value']
        return Round_Id


class WebsiteTasks(HttpUser):
    account = 'QA2'
    password = 'a123456'
    header = {'Content-Type': "application/json", 'X-Requested-With': "XMLHttpRequest"}
    wait_time = between(6, 10)

    def on_start(self):
        """ on_start is called when a Locust start before any task is scheduled """
        self.login(self.account, self.password)
        self.round = Master().Round()

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
    def story1(self):
        data = {"WagersTimeBegin": BeginDate, "WagersTimeEnd": EndTime, "PayoffTimeEnd": EndTime,
                "connectionId": self.info()}
        self.client.post("/BetRecord/Search", json_format(data), headers = self.header)

    @task
    def story2(self):
        data = {"PayoffTimeBegin": BeginDate, "PayoffTimeEnd": EndTime,
                "connectionId": self.info()}
        self.client.post("/BetRecord/Search", json_format(data), headers = self.header)

    @task
    def story3(self):
        data = {"PayoffTimeBegin": BeginDate, "PayoffTimeEnd": EndTime,
                "connectionId": self.info()}
        self.client.post("/BetRecord/Search", json_format(data), headers = self.header)

    @task
    def story4(self):
        commission_able = random.randint(1, 10)
        data = {"WagersTimeBegin": BeginDate, "CommissionableBegin": str(commission_able),
                "connectionId": self.info()}
        self.client.post("/BetRecord/Search", json_format(data), headers = self.header)

    @task
    def story5(self):
        commission_able = random.randint(1, 10)
        data = {"WagersTimeBegin": BeginDate, "PayoffBegin": str(commission_able),
                "connectionId": self.info()}
        self.client.post("/BetRecord/Search", json_format(data), headers = self.header)

    @task
    def story6(self):
        data = {"WagersTimeBegin": BeginDate, "GameCategories": ["Cq9Slot"], "Round": str(self.round),
                "connectionId": self.info()}
        self.client.post("/BetRecord/Search", json_format(data), headers = self.header)
